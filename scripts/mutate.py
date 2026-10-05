"""Mutation pass: break every defence on purpose, confirm a test notices.

Passing tests prove nothing on their own. Each entry below is a small edit to
the contract that removes a defence. The suite must fail for every one of them,
and this script records WHICH test caught it, so the table in the README is
measured rather than claimed.

    python scripts/mutate.py            # run them all, print what caught what
    python scripts/mutate.py --md       # emit the markdown table for the README

An escaping mutation is a finding, not a nuisance: either a missing test, or a
later defence strict enough that an earlier test can no longer fail. The script
exits non-zero if anything escapes, and refuses to run on a red baseline.

Three rules keep the harness honest:

  * the unmutated suite must be green before anything is mutated;
  * a find string that is missing, or matches more than once, is a failure of
    the harness, never a skip, so refactoring cannot quietly turn a row off;
  * scripts/lift.py runs inside every mutated copy before the suite, so the lib
    parity test can never stand in for the behavioural test a mutation deserves.
"""

import argparse
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).absolute().parent.parent
TARGET = "tender.py"

FENCE = '    return str(raw).replace("<", "(").replace(">", ")").replace("[", "(").replace("]", ")")'
CLOSED_IN_ASSESS = ('        if str(t.status) != OPEN:\n            raise gl.vm.UserError(f"{ERR_EXPECTED} this tender is closed")\n'
                    '        if str(b.verdict) != "":')

MUTATIONS = [
    # -- reading the answer
    ("an option past the list is accepted", '    if k < 0 or k >= n:\n        return ""', '    if k < 0:\n        return ""'),
    ("an answer in words is read as a number",
     '    if s == "" or any(ch not in "0123456789" for ch in s) or len(s) > 2:', '    if s == "":'),

    # -- the two orders
    ("the second pass is asked in the forward order",
     "            rev, _ = ask(title, reqs, proposal, REVERSED)", "            rev, _ = ask(title, reqs, proposal, FORWARD)"),
    ("the reversed order is not reversed", "REVERSED = [FAILS, MEETS]", "REVERSED = [MEETS, FAILS]"),
    ("a disagreement between the orders keeps the forward verdict",
     "    return forward if forward == reverse else FAILS", "    return forward"),
    ("a disagreement between the orders is meets",
     "    return forward if forward == reverse else FAILS", "    return forward if forward == reverse else MEETS"),
    ("an answer is not read back through its order", "    return order[int(choice)]", "    return FORWARD[int(choice)]"),

    # -- reading the model
    ("an unusable answer is not retried",
     "    for _ in range(2):\n        raw = gl.nondet.exec_prompt(", "    for _ in range(1):\n        raw = gl.nondet.exec_prompt("),
    ("an unusable answer is read as fails",
     '    raise gl.vm.UserError(f"{ERR_LLM} the model named neither option")', '    return FAILS, ""'),
    ("an answer that is not an object crashes the block",
     "        if isinstance(raw, dict):\n            choice = normalise_choice", "        if True:\n            choice = normalise_choice"),

    # -- the validator
    ("the free structural layer is skipped",
     "            if not verdict_sound(proposed):\n                return False\n            try:", "            try:"),
    ("a validator agrees with a leader that raised",
     "                # An [LLM_ERROR] is never agreed with.\n                return False",
     "                # An [LLM_ERROR] is never agreed with.\n                return True"),
    ("a validator trusts the leader", '            return tender_agrees(mine["verdict"], proposed)', "            return True"),
    ("a validator whose own model failed agrees",
     "            except gl.vm.UserError:\n                return False", "            except gl.vm.UserError:\n                return True"),
    ("unassessed is a sound verdict", "    return verdict == MEETS or verdict == FAILS", '    return verdict != ""'),
    ("agreement is not exact", "and str(mine) == str(theirs)", "and str(mine) != '' "),
    ("the agreed verdict is not checked again before it is stored",
     "        if not verdict_sound(verdict):", "        if False:"),

    # -- before the model
    ("anyone may ask for an assessment",
     '        if sender != t.buyer and int(self.bid_of.get(f"{tid}:{sender.as_hex}", u256(0))) == 0:', "        if False:"),
    ("only the buyer may ask for an assessment",
     '        if sender != t.buyer and int(self.bid_of.get(f"{tid}:{sender.as_hex}", u256(0))) == 0:',
     "        if sender != t.buyer:"),
    ("an assessment is taken before bids close", "        if now <= int(t.bids_close):\n            raise gl.vm.UserError(f\"{ERR_EXPECTED} assessments open",
     "        if False:\n            raise gl.vm.UserError(f\"{ERR_EXPECTED} assessments open"),
    ("an assessment is taken after assessments close", "        if now > int(t.assess_close):", "        if False:"),
    ("an assessment on the last second is refused", "        if now > int(t.assess_close):", "        if now >= int(t.assess_close):"),
    ("a bid is assessed twice", '        if str(b.verdict) != "":', "        if False:"),
    ("an assessment is taken on a decided tender", CLOSED_IN_ASSESS,
     CLOSED_IN_ASSESS.replace("        if str(t.status) != OPEN:", "        if False:", 1)),
    ("a bid of another tender is assessed here",
     "        if i < 0 or i >= len(self.bids) or int(self.bids[i].tender_id) != int(tender_id):",
     "        if i < 0 or i >= len(self.bids):"),
    ("an assessment is not counted", "        t.n_assessed = u256(int(t.n_assessed) + 1)", "        pass"),

    # -- bidding
    ("the buyer may bid on its own tender", "        if sender == t.buyer:", "        if False:"),
    ("bids are taken after bids close", "        if self._now() > int(t.bids_close):", "        if False:"),
    ("a bid on the last second is refused", "        if self._now() > int(t.bids_close):", "        if self._now() >= int(t.bids_close):"),
    ("a supplier may bid any number of times", '        if int(self.bid_of.get(key, u256(0))) > 0:', "        if False:"),
    ("a bid is not remembered against its supplier", "        self.bid_of[key] = u256(bid_id + 1)", "        pass"),
    ("a tender takes any number of bids", "        if int(t.n_bids) >= MAX_BIDS:", "        if False:"),
    ("a price of zero is accepted", "        if p < 1 or p > MAX_PRICE:", "        if p > MAX_PRICE:"),
    ("the proposal is unbounded", "        if len(body) < MIN_PROPOSAL or len(body) > MAX_PROPOSAL:", "        if False:"),
    ("bids are not linked", "            self.bids[int(t.last_bid)].next = u256(bid_id)", "            pass"),

    # -- the award
    ("the award is made while bids are open", "        if now <= int(t.bids_close):\n            raise gl.vm.UserError(f\"{ERR_EXPECTED} bids are open",
     "        if False:\n            raise gl.vm.UserError(f\"{ERR_EXPECTED} bids are open"),
    ("an unassessed bid does not hold the award", "                if not late:", "                if False:"),
    ("an unassessed bid is never marked", "                b.verdict = UNASSESSED", "                pass"),
    ("a tender is decided twice",
     '        if str(t.status) != OPEN:\n            raise gl.vm.UserError(f"{ERR_EXPECTED} this tender was already decided',
     '        if False:\n            raise gl.vm.UserError(f"{ERR_EXPECTED} this tender was already decided'),
    ("a bid that fails can win", "        if verdicts[k] != MEETS:\n            continue", "        if verdicts[k] == UNASSESSED:\n            continue"),
    ("an unassessed bid can win", "        if verdicts[k] != MEETS:\n            continue", "        if verdicts[k] == FAILS:\n            continue"),
    ("the highest price wins", "        if best < 0 or int(prices[k]) < int(prices[best]):", "        if best < 0 or int(prices[k]) > int(prices[best]):"),
    ("a tie goes to the latest bid", "        if best < 0 or int(prices[k]) < int(prices[best]):", "        if best < 0 or int(prices[k]) <= int(prices[best]):"),
    ("no award still names a winner", "        if k < 0:\n            t.status = NO_AWARD\n            return", "        if k < 0:\n            t.status = NO_AWARD"),
    ("the winner is not recorded", "        t.winning_bid = u256(ids[k] + 1)", "        pass"),
    ("the winner is off by one", "        t.winning_bid = u256(ids[k] + 1)", "        t.winning_bid = u256(ids[k])"),

    # -- opening
    ("the requirements refusal is ignored", '        if refusal != "":', "        if False:"),
    ("an empty list of requirements is accepted",
     '    if len(reqs) == 0 or (len(reqs) == 1 and reqs[0] == ""):', "    if False:"),
    ("more than six requirements are accepted", "    if len(reqs) > MAX_REQUIREMENTS:", "    if False:"),
    ("a requirement of any length is accepted", "        if len(r) < MIN_REQUIREMENT or len(r) > MAX_REQUIREMENT:", "        if False:"),
    ("two requirements with the same wording are accepted",
     "    if len(set(r.lower() for r in reqs)) != len(reqs):", "    if False:"),
    ("a missing requirement is dropped and the rest renumbered",
     '    return [clean_text(part) for part in str(text).split("|")]',
     '    return [clean_text(part) for part in str(text).split("|") if clean_text(part)]'),
    ("the windows are unbounded",
     "        if bw < MIN_WINDOW or bw > MAX_WINDOW or aw < MIN_WINDOW or aw > MAX_WINDOW:", "        if False:"),
    ("the assessment window is unbounded",
     "        if bw < MIN_WINDOW or bw > MAX_WINDOW or aw < MIN_WINDOW or aw > MAX_WINDOW:",
     "        if bw < MIN_WINDOW or bw > MAX_WINDOW:"),
    ("assessments close with the bids", "assess_close=u256(now + bw + aw)", "assess_close=u256(now + bw)"),
    ("the title is unbounded", "        if len(t) < MIN_TITLE or len(t) > MAX_TITLE:", "        if False:"),

    # -- the prompt boundary
    ("the fence is removed", FENCE, "    return str(raw)"),
    ("the fence leaves square brackets", FENCE, '    return str(raw).replace("<", "(").replace(">", ")")'),
    ("the proposal reaches the prompt unfenced", "{fence(proposal)}", "{proposal}"),
    ("the requirements reach the prompt unfenced", 'f"[R{k}] {fence(reqs[k])}"', 'f"[R{k}] {reqs[k]}"'),
    ("the title reaches the prompt unfenced", "{fence(title)}", "{title}"),
    ("the prompt no longer says vague is not met",
     "them; one it does not address, or addresses only vaguely, is not met.", "them."),
    ("the prompt asks about value for money",
     "Do not\njudge whether the proposal is good value, persuasive or likely to be honoured,\nonly what it commits to.",
     "Judge\nwhether the proposal is good value."),
    ("a leader's reason is stored as sent", '        b.why = sanitise_reason(res.get("because", ""))', '        b.why = str(res.get("because", ""))'),
    ("a leader's reason is stored uncapped", '    return " ".join("".join(out).split())[:limit]', '    return " ".join("".join(out).split())'),
    ("control characters are stored", '            out.append(" ")\n        else:', "            out.append(ch)\n        else:"),
]


PYTEST = [sys.executable, "-m", "pytest", "tests/", "-x", "-q", "--no-header", "-p", "no:cacheprovider"]


def copy_repo(tmp):
    dst = pathlib.Path(tmp) / "repo"
    shutil.copytree(ROOT, dst, ignore=shutil.ignore_patterns(
        "__pycache__", ".pytest_cache", ".git", "artifacts", "*.pyc"))
    return dst


def run_one(label, find, replace):
    with tempfile.TemporaryDirectory() as tmp:
        dst = copy_repo(tmp)
        target = dst / "contracts" / TARGET
        src = target.read_text(encoding="utf-8")
        hits = src.count(find)
        if hits == 0:
            return "PATTERN NOT FOUND", None
        if hits > 1:
            return "PATTERN NOT UNIQUE", None
        target.write_text(src.replace(find, replace, 1), encoding="utf-8", newline="\n")
        subprocess.run([sys.executable, "scripts/lift.py"], cwd=dst, capture_output=True)
        proc = subprocess.run(PYTEST, cwd=dst, capture_output=True, text=True)
        if proc.returncode == 0:
            return "ESCAPED", None
        text = proc.stdout + proc.stderr
        m = re.search(r"^(?:FAILED|ERROR) (\S+?)::(\S+?)(?:\[|\s|$)", text, re.M)
        if m:
            return "caught", m.group(2).split("::")[-1]
        m = re.search(r"^E\s+(\w*(?:Error|Exception))", text, re.M)
        if m:
            return "caught", m.group(1) + " at import"
        return "caught", "unnamed failure"


def baseline_is_green():
    with tempfile.TemporaryDirectory() as tmp:
        dst = copy_repo(tmp)
        proc = subprocess.run(PYTEST, cwd=dst, capture_output=True, text=True)
        return proc.returncode == 0, (proc.stdout + proc.stderr)[-2000:]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--md", action="store_true", help="emit the README table")
    args = ap.parse_args()

    green, tail = baseline_is_green()
    if not green:
        print("the unmutated suite is not green; every mutation would look caught:\n" + tail, file=sys.stderr)
        return 2

    rows, escaped = [], []
    for label, find, replace in MUTATIONS:
        status, test = run_one(label, find, replace)
        if status == "caught":
            rows.append((label, test))
            if not args.md:
                print("  caught   %-70s %s" % (label, test), flush=True)
        else:
            escaped.append((label, status))
            print("  %-8s %s" % (status, label), file=sys.stderr, flush=True)

    if args.md:
        print("| Mutation | Caught by |")
        print("|---|---|")
        for label, test in rows:
            print("| %s | `%s` |" % (label, test))
    else:
        print()
        print("  %d mutations, %d caught, %d escaped" % (len(MUTATIONS), len(rows), len(escaped)))
    return 1 if escaped else 0


if __name__ == "__main__":
    sys.exit(main())

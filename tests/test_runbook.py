"""
The demo, replayed offline.

scripts/demo.py puts the demo on StudioNet from scripts/demo_data.py (STEPS).
This file replays the same steps against the real contract in the simulator,
so a demo that could not succeed is caught before a single transaction is
spent on it.

When deployments/studionet.json exists, the replay goes further: it feeds the
simulator the verdicts the validators actually agreed on, and checks that the
contract in this repository awards exactly what the deployed one did, and
refuses exactly where it refused.

    pytest tests/test_runbook.py -v
"""

import hashlib
import importlib.util
import json
import pathlib

import pytest

import glsim as S

CONTRACT_PATH = "contracts/tender.py"
M = S.load_contract(CONTRACT_PATH)
RECORD = pathlib.Path("deployments/studionet.json")

_spec = importlib.util.spec_from_file_location("demo_data", "scripts/demo_data.py")
D = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(D)

WHO = {"buyer": "0x" + "a1" * 20, "ann": "0x" + "b2" * 20, "ben": "0x" + "c3" * 20,
       "cal": "0x" + "d4" * 20, "dev": "0x" + "e5" * 20, "stranger": "0x" + "f6" * 20}
T0 = 1_790_000_000

# the bid each ok assessment is about, in order
ASSESSED = [s[2][1] for s in D.STEPS if s[1] == "assess" and s[3] == "ok"]


def replay(verdicts):
    """Run STEPS. `verdicts` are what the ok assessments come back with, in order."""
    c = S.deploy(CONTRACT_PATH)
    queue = list(verdicts)
    outcomes = []
    clock = T0
    for step in D.STEPS:
        actor, method, spec, expect, label = step[:5]
        clock += 30
        if "after_bids" in step[5:]:
            clock = max(clock, M.seconds(c.tender(0)["bids_close"]) + 20)
        if "after_assess" in step[5:]:
            clock = max(clock, M.seconds(c.tender(0)["assess_close"]) + 20)
        S.set_time(M.iso(clock))
        S.set_mocks()
        if method == "open":
            title, reqs, bw, aw = spec
            args = [title, D.joined(reqs), bw, aw]
        else:
            args = list(spec)
        if method == "assess" and expect == "ok":
            want = queue.pop(0)
            S.set_mocks(leader_prompts={"[0] meets:": {"option": str(M.FORWARD.index(want)), "because": "replayed"},
                                        "[0] fails:": {"option": str(M.REVERSED.index(want)), "because": "replayed"}})
        S.set_sender(WHO[actor])
        try:
            S.call(c, method, *args)
            outcomes.append(("ok", ""))
        except S.UserError as e:
            outcomes.append(("refused", e.message))
    return c, outcomes


class TestDemoData:
    def test_every_value_the_demo_sends_passes_the_bounds(self):
        assert M.requirements_refusal(M.split_list(D.joined(D.REQUIREMENTS))) == ""
        assert M.MIN_TITLE <= len(D.TITLE) <= M.MAX_TITLE
        for w in (D.BID_WINDOW, D.ASSESS_WINDOW):
            assert M.MIN_WINDOW <= w <= M.MAX_WINDOW
        for text in (D.ANN, D.BEN, D.CAL, D.DEV, D.LATE):
            assert M.MIN_PROPOSAL <= len(M.clean_text(text)) <= M.MAX_PROPOSAL

    def test_each_bid_changes_one_thing(self):
        assert D.BEN_PRICE < D.DEV_PRICE < D.ANN_PRICE < D.CAL_PRICE          # the winner is not the cheapest
        assert "virgin-fibre" in D.BEN and "recycled" not in D.BEN.lower()    # Ben misses requirement 0
        assert "20 November" in D.DEV                                          # Dev would miss requirement 1 too
        for text in (D.ANN, D.CAL):
            assert "recycled" in text and "A5" in text and "saddle stitched" in text

    def test_the_windows_outlast_the_steps_meant_to_land_inside_them(self):
        """Seven transactions after open are meant to find bids open, and six
        after bids close are meant to find assessments open; at up to 60 s a
        transaction (90 s for an assessment) they land inside both windows."""
        assert D.BID_WINDOW >= 7 * 60
        assert D.ASSESS_WINDOW >= 3 * 90 + 3 * 60


class TestReplay:
    def test_the_demo_succeeds_and_refuses_exactly_where_it_says(self):
        _, outcomes = replay(D.EXPECTED_VERDICTS)
        assert [o for o, _ in outcomes] == [s[3] for s in D.STEPS]

    def test_the_refusals_say_why(self):
        _, outcomes = replay(D.EXPECTED_VERDICTS)
        msgs = [m for o, m in outcomes if o == "refused"]
        wants = ["the buyer cannot bid", "bids once per tender", "assessments open when bids close",
                 "bids closed at", "only the buyer or a bidder", "bid 3 is waiting for its assessment",
                 "assessments closed at"]
        assert len(msgs) == len(wants)
        for msg, want in zip(msgs, wants):
            assert want in msg, (want, msg)

    def test_the_expected_verdicts_award_ann_not_the_cheapest(self):
        c, _ = replay(D.EXPECTED_VERDICTS)
        assert [(b["by"], b["verdict"]) for b in c.bids_of(0)["bids"]] == [
            (WHO["ann"], "meets"), (WHO["ben"], "fails"), (WHO["cal"], "meets"), (WHO["dev"], "unassessed")]
        t = c.tender(0)
        assert (t["status"], t["winning_bid"], t["winning_price"], t["winner"]) == ("awarded", 0, "1180", WHO["ann"])


@pytest.mark.skipif(not RECORD.exists(), reason="no deployment recorded yet: python scripts/demo.py")
class TestTheRecord:
    """The live run, checked against this repository."""

    def _record(self):
        return json.loads(RECORD.read_text(encoding="utf-8"))

    def test_the_record_is_of_this_source(self):
        here = hashlib.sha256(pathlib.Path(CONTRACT_PATH).read_bytes().replace(b"\r\n", b"\n")).hexdigest()
        assert self._record()["source_sha256"] == here, "the deployed contract is not this file; redeploy"

    def test_every_step_on_chain_did_what_the_demo_expected(self):
        steps = [s for s in self._record()["steps"] if s["step"] != "deploy"]
        assert [("ok" if s["ok"] else "refused") for s in steps] == [s[3] for s in D.STEPS]

    def test_this_contract_awards_what_the_deployed_one_awarded(self):
        rec = self._record()
        by_id = {b["id"]: b for b in rec["tenders"][0]["bids"]}
        c, outcomes = replay([by_id[i]["verdict"] for i in ASSESSED])
        assert [o for o, _ in outcomes] == [s[3] for s in D.STEPS]
        assert [b["verdict"] for b in c.bids_of(0)["bids"]] == [b["verdict"] for b in rec["tenders"][0]["bids"]]
        mine, theirs = c.tender(0), rec["tenders"][0]["tender"]
        for field in ("status", "winning_bid", "winning_price"):
            assert str(mine[field]) == str(theirs[field]), field

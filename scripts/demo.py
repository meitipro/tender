"""Deploy Tender to StudioNet and put every path on the explorer.

    pip install genlayer-py==0.18.0
    python scripts/demo.py

The run deploys contracts/tender.py exactly as it is in this repository, then
sends the steps in scripts/demo_data.py (STEPS), including the ones that end in
a refusal, and writes what happened to deployments/studionet.json: every
transaction hash, its status, the refusal sentence where there was one, and the
tender, its requirements and every bid as the chain holds them. Nothing in that
file is typed by hand.

Six accounts act, each in one role: the buyer, four suppliers and a stranger.
They are made in memory for this run and never written to disk. Nothing in
this contract is payable, and StudioNet is gasless, so none of them is funded.
"""

import datetime
import hashlib
import json
import pathlib
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).absolute().parent))
import demo_data as D                                       # noqa: E402
from studio import EXPLORER, Studio                         # noqa: E402

ROOT = pathlib.Path(__file__).absolute().parent.parent
SOURCE = ROOT / "contracts" / "tender.py"
OUT = ROOT / "deployments" / "studionet.json"


def utc_seconds(iso):
    t = datetime.datetime.fromisoformat(iso.replace("Z", "+00:00"))
    return int(t.timestamp())


def wait_past(iso, label):
    """Sleep until the chain clock has passed `iso`, with a margin, because
    the contract compares against the time of the transaction that arrives."""
    target = utc_seconds(iso) + 20
    left = target - int(time.time())
    if left > 0:
        print(f"  waiting {left}s for {label} ({iso})")
        time.sleep(left)


def args_for(method, spec):
    if method == "open":
        title, reqs, bw, aw = spec
        return [title, D.joined(reqs), bw, aw]
    return list(spec)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    code = SOURCE.read_text(encoding="utf-8")
    s = Studio()

    print("\naccounts (in memory, nothing to fund: StudioNet is gasless and nothing here is payable)")
    who = {name: s.account(name) for name in ("buyer", "ann", "ben", "cal", "dev", "stranger")}

    print("\ndeploy")
    address = s.deploy(who["buyer"], code, [])

    print("\nthe demo")
    for step in D.STEPS:
        actor, method, spec, expect, label = step[:5]
        if "after_bids" in step[5:]:
            wait_past(s.read(address, "tender", [0])["bids_close"], "bids to close")
        if "after_assess" in step[5:]:
            wait_past(s.read(address, "tender", [0])["assess_close"], "assessments to close")
        s.write(who[actor], address, method, args_for(method, spec), step=label, expect=expect)

    n = int(s.read(address, "count"))
    tenders = [{
        "tender": s.read(address, "tender", [k]),
        "requirements": s.read(address, "requirements_of", [k])["requirements"],
        "bids": s.read(address, "bids_of", [k])["bids"],
        "winner": s.read(address, "winner_of", [k]),
    } for k in range(n)]
    record = {
        "network": "studionet",
        "chain_id": 61999,
        "contract": address,
        "explorer": f"{EXPLORER}/address/{address}",
        "source_sha256": hashlib.sha256(SOURCE.read_bytes().replace(b"\r\n", b"\n")).hexdigest(),
        "constructor": {},
        "accounts": {name: a.address for name, a in who.items()},
        "steps": s.log,
        "tenders": tenders,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(record, indent=2, default=str) + "\n", encoding="utf-8", newline="\n")

    print(f"\n  contract   {address}")
    print(f"  explorer   {EXPLORER}/address/{address}")
    for k, t in enumerate(tenders):
        print(f"  tender {k}  {t['tender']['status']:<9} winning bid {t['tender']['winning_bid']} at "
              f"{t['tender']['winning_price']}  verdicts {[(b['id'], b['price'], b['verdict']) for b in t['bids']]}")
    print(f"  written    {OUT.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()

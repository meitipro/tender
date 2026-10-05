# Deploying Tender

Everything here runs on StudioNet. It is gasless, and nothing in this contract
is payable, so no account needs funding. Nothing needs a private key in a file.

## 1 - Check the contract

```bash
pip install -r requirements-dev.txt
pytest tests/ -q
python scripts/schema_check.py contracts/tender.py
GENVM_VERSION=v0.3.0-rc7 genvm-lint check contracts/tender.py
```

`schema_check.py` runs the file through the live studionet runtime with
`gen_getContractSchemaForCode`, without deploying it. On Windows, set
`PYTHONIOENCODING=utf-8` first, or the linter dies printing its own tick.

## 2 - Run the demo

```bash
python scripts/demo.py
```

It makes six accounts in memory (`buyer`, `ann`, `ben`, `cal`, `dev`,
`stranger`) and deploys `contracts/tender.py` exactly as it is in this
repository. The data and the steps are in
[`scripts/demo_data.py`](scripts/demo_data.py); the same list drives the demo
and `tests/test_runbook.py`.

The tender: 400 programmes for a builders' day, prices in euros, bids open for
eight minutes and assessments for ten after that. Its requirements:

- R0: Printed on paper with at least 70 percent recycled content
- R1: All 400 programmes delivered to the venue by 14 November 2026
- R2: A5 size, full colour on every page, saddle stitched

The writes, in order:

| # | From | Call | Expected |
|---|---|---|---|
| 1 | buyer | `open(programmes, 3 requirements, 480, 600)` | ok: tender 0 |
| 2 | buyer | `bid(0, 1180, ...)` | refused: the buyer cannot bid |
| 3 | ann | `bid(0, 1180, <recycled, 12 November, A5 full colour stitched>)` | ok: bid 0 |
| 4 | ben | `bid(0, 950, <glossy virgin-fibre paper>)` | ok: bid 1, the cheapest |
| 5 | cal | `bid(0, 1240, <80 percent recycled, 13 November>)` | ok: bid 2 |
| 6 | dev | `bid(0, 1090, <delivery on 20 November>)` | ok: bid 3 |
| 7 | ann | `bid(0, 999, ...)` | refused: one bid per supplier |
| 8 | ann | `assess(0, 0)` | refused: assessments open when bids close |
| 9 | stranger | `bid(0, 800, ...)` after bids close | refused: bids closed |
| 10 | stranger | `assess(0, 1)` | refused: only the buyer or a bidder |
| 11 | buyer | `assess(0, 1)` | ok: **fails** (not recycled) |
| 12 | ann | `assess(0, 0)` | ok: **meets** |
| 13 | cal | `assess(0, 2)` | ok: **meets** |
| 14 | stranger | `award(0)` | refused: bid 3 waits for its assessment |
| 15 | dev | `assess(0, 3)` after assessments close | refused: assessments closed |
| 16 | stranger | `award(0)` | ok: **awarded to Ann at 1180**; bid 3 is unassessed |

The script waits for bids to close before step 9 and for assessments to close
before step 15, and stops at the first step that does not do what the table
says, because the demo claims whatever it records.

It writes [`deployments/studionet.json`](deployments/studionet.json): every
transaction hash, its sender and status, each refusal's sentence, and the
tender, its requirements and every bid as the chain holds them. Then:

```bash
pytest tests/test_runbook.py -v
```

`TestTheRecord` replays the verdicts the validators agreed on through this
repository's contract and fails unless it awards exactly what the deployed one
did, and refuses exactly where it refused.

## 3 - Reads - free, no transaction

```bash
genlayer network set studionet
genlayer call <address> count
genlayer call <address> tender --args 0
genlayer call <address> requirements_of --args 0
genlayer call <address> bids_of --args 0
genlayer call <address> winner_of --args 0
```

## 4 - Before the portal

```bash
python scripts/verify_deployment.py <address>
python scripts/measure.py --write
```

The first reads the deployed source back off chain, compares it with
`contracts/tender.py` and lints the deployed bytes. The second runs the suite
and the mutation pass and writes the measured numbers and the live record into
README.md. Neither writes anything unless every check passes.

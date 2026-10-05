# Submission

One submission, under **Builder -> Intelligent Contracts**. This repository is
one standalone primitive.

---

## Before you submit, in order

1. **Measure, do not estimate.**

   ```bash
   python scripts/measure.py --write
   ```

   Runs the suite and the full mutation pass, renders the live record, and
   writes all three into README.md. It refuses to write anything if the suite
   is red, a mutation escapes, or the record is of a different contract file.

2. **Prove the address is evidence for this repository.**

   ```bash
   python scripts/verify_deployment.py <address>
   ```

   Reads the source back off chain, compares it with `contracts/tender.py` and
   runs `genvm-lint check` on those bytes.

3. **Open the explorer page and check it.** It must show the deploy, the four
   bids, the three assessments with a consensus result beside them, the award,
   and the seven refusals, each with its reason.

---

## On chain

The address, every transaction, every assessment and the award are in the
[README](README.md#it-is-live-and-every-path-is-on-chain), rendered from
[`deployments/studionet.json`](deployments/studionet.json), and every
transaction with the wallet that sent it is in [EVIDENCE.md](EVIDENCE.md).

## What to say in the portal

**What it does.** Tender is a procurement round with its requirements written
in before any bid exists. The buyer freezes a list of mandatory requirements
and two windows. Suppliers bid a price and a proposal, once each. After bidding
closes, validators decide per bid whether the proposal meets every
requirement, in both option orders and without ever seeing a price, and the
contract awards the lowest price among the bids that meet them. A bid nobody
assessed before assessments closed cannot win.

**Why it needs GenLayer.** Whether "glossy virgin-fibre paper" meets "at least
70 percent recycled content", and whether "delivery on 20 November" meets "by
14 November", is a judgment in natural language, and the buyer who picks the
winner is the one party who cannot be trusted to make it. Independent
validators must agree on compliance, and the buyer cannot bid, disqualify or
choose.

**What it learned from earlier work.** The model is asked the coarsest
question that still carries the judgment, one bid at a time, and is never
shown a price. Every judgment has a clock: nothing is assessed after
`assess_close`, and an unassessed bid is not compliant. The uncertainty goes
into the value (an order-dependent verdict is fails), and the award is
counting, not judging.

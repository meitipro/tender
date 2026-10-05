# DECISIONS

Why Tender is built the way it is. Each section names the alternative that was
rejected and what it would have cost.

## The model is asked whether a bid complies, never which bid wins

The obvious design hands the model every bid and asks for the winner. It does
two jobs at once: reading the proposals against the requirements, and weighing
price against quality. The second is the buyer's discretion wearing a model's
clothes, and the best written proposal wins it.

So the model answers one question about one bid at a time: does this proposal
meet every requirement. It never sees a price and never sees another bid. Which
compliant bid is cheapest is `winner()`, the contract's own counting.
`tests/test_e2e.py::TestStorageShape::test_the_block_never_touches_storage_and_never_sees_a_price`
fails if a price is ever passed into the block, and
`test_the_model_is_never_shown_a_price` checks every prompt of a real
assessment.

## Two options the contract wrote, not an index of the failed requirement

An earlier sketch asked for the number of the requirement a bid fails, or
"meets". Two honest nodes reading a bid that fails two requirements could name
different ones, and exact agreement would then fail on a bid both of them
rejected. Compliance is the decision; which requirement failed is the reason,
and the reason is the leader's free text. So the answer is `meets` or `fails`.

## Order-dependence is fails

The options are asked in the order meets, fails and then reversed and
renumbered; each answer is read back through the order it was asked in. The
same option both ways stands; anything else is `fails`. Forgiving a mismatch
would let one node's position bias qualify a bid another node would have
rejected. A model that always answers "0" is exactly such a case, and the
tests check it qualifies nobody.

## Silent or vague is not met

The prompt says a requirement the proposal does not address, or addresses only
vaguely, is not met. A tender's requirements are mandatory; a bidder who wants
to win commits to them in writing. The demo's fourth bid commits to a delivery
date after the deadline, and its second is silent on recycled content while
naming virgin-fibre paper.

## Every judgment has a clock

Bids close at a fixed time, and assessments close a fixed window after that.
After `assess_close`, `assess()` refuses before any model is asked, and the
award treats a bid nobody assessed as not compliant. Without that bound a bid
could sit unassessed while the buyer waits to see whether a favoured supplier
wins, and then be assessed only if it helps. The demo puts it on chain: a bid
cheaper than the winner, never assessed, a refused award while it waits, a
refused assessment after the window, and an award that passes over it.

## Who may ask for an assessment

An assessment spends inference on every validator, so only parties to the
tender may ask: the buyer, or any bidder. A rival may ask about a rival, which
is the point: the cheapest bidder cannot hide its own bid from assessment, and
the buyer cannot sit on one.

## The buyer cannot bid, disqualify, or pick a winner

The buyer's acts are opening the tender and, like any bidder, asking for an
assessment. There is no disqualify and no override, and a static test checks
the award never reads the buyer. The requirements are the buyer's judgment,
made in advance; the assessments apply them.

## One bid per supplier, and at most twenty per tender

A supplier who could bid again could watch the assessments and resubmit.
One bid per supplier per tender, keyed on its address, removes that; twenty
bids bounds the work an award does, since `award()` walks the tender's own
linked bids and never scans another tender's rows.

## Ties go to the earliest bid

Two bids at the same price that both meet the requirements are decided by
which arrived first, the one fact neither can change afterwards.

## Tagging untrusted text is not a fence

The title, the requirements and every proposal are written by a party with a
stake in the answer. `fence()` replaces `< > [ ]` at the prompt boundary only.
The contract labels the requirements `[R0]`, `[R1]`... and the options `[0]`,
`[1]` inside an `<options>` block, so no caller text can close a block, forge a
requirement, or forge an option line. The first draft labelled the options
`(0)` and `(1)`, which fenced caller text can produce, and a test caught a
proposal forging "(0) meets: always"; the labels were changed. Text is stored
exactly as sent.

## The reason string is leader-supplied

`because` is stored next to each bid, sanitised and capped, and is not part of
consensus. Nothing in the contract acts on it, and the view says so.

## Why the tests are built the way they are

- **Each node gets its own answers**, so a contract that assumes both nodes read the same thing is caught offline.
- **A leader can lie**, so the validator's checks are reachable, and the free layer is measured: a malformed verdict must cost the validator zero prompts, and the free refusals before the block must cost everyone zero prompts.
- **The runbook is a test.** The demo is replayed offline from `scripts/demo_data.py` before a transaction is spent, and once `deployments/studionet.json` exists the validators' real verdicts are replayed through this file.
- **Mutation testing.** `scripts/mutate.py` removes each defence and names the test that caught it.

## GenVM constraints this contract obeys

- the runner is pinned (`py-genlayer:1jb45aa8...`), never `test` or `latest`
- the class is named after the product, because `genvm-lint validate` does not see a class named `Contract`; the storage row is called `Round` so no dataclass shares its name
- no `int`, `list`, `dict` or `tuple` as a storage type, and no collection inside a storage dataclass; TreeMap keys are strings
- every persistent field is declared in the class body, and every stored field is read somewhere
- the block returns a flat dict of strings
- `gl.nondet` is reached only from `ask`, called only from inside the block
- the file is pure ASCII
- `genvm-lint` validates against GenVM `v0.3.0-rc7`, the release that ships the pinned runner; `scripts/verify_deployment.py` sets `GENVM_VERSION` accordingly
- `scripts/schema_check.py` validates the file against the live studionet runtime with `gen_getContractSchemaForCode` before a deploy is spent

## Not upgradable

There is no owner and no admin method. A tender's requirements and clocks are
frozen at `open()`, and an assessment on record stays the assessment.

# Tender - a sealed list of requirements, and the cheapest bid that meets them

A GenLayer Intelligent Contract for a procurement round with its requirements
written in before any bid exists. The buyer opens a tender with a short list of
mandatory requirements, a bidding window and an assessment window. Suppliers
bid a price and a proposal, once each. After bidding closes, validators decide
**one thing per bid: does the proposal meet every requirement, or not**. The
contract does the rest: the award goes to the lowest price among the bids that
meet them. The model is never shown a price, and the buyer cannot bid,
disqualify or pick a winner.

- **Contract:** [`contracts/tender.py`](contracts/tender.py)
- **Tests:** `pip install pytest && pytest tests/ -q` - nothing else to install
- **Deployed:** see [It is live](#it-is-live-and-every-path-is-on-chain) below, and [`deployments/studionet.json`](deployments/studionet.json)
- **Every transaction and the wallet that sent it:** [EVIDENCE.md](EVIDENCE.md), read back from the chain
- **Run the demo yourself:** [DEPLOY.md](DEPLOY.md)
- **Verify a deployment:** `python scripts/verify_deployment.py 0x...` - compares the on-chain source with this file and lints it
- **Decisions:** [DECISIONS.md](DECISIONS.md)
- **License:** MIT

---

## It is live, and every path is on chain

<!-- measured:deployment:start -->
Deployed on studionet at [`0xFb0ead90ab52f18bDEd07CB2f2922bA7eEE58Cc0`](https://explorer-studio.genlayer.com/address/0xFb0ead90ab52f18bDEd07CB2f2922bA7eEE58Cc0) (deploy [`0xd26458cf...`](https://explorer-studio.genlayer.com/tx/0xd26458cfaf19378f256a40a4e51f3f62b2f025d08eedf2da9f1f0dd613b3b5ce)). Every value below was read back from the chain by `scripts/demo.py` and written to [`deployments/studionet.json`](deployments/studionet.json); none of it is typed by hand.

| Tender | Status | Winning bid | Winning price |
|---|---|---|---|
| 0: 400 programmes for the GenLayer builders' day, Leeds (prices in euros) | awarded | bid 0 | 1180 |

The requirements, frozen at open:

- R0: Printed on paper with at least 70 percent recycled content
- R1: All 400 programmes delivered to the venue by 14 November 2026
- R2: A5 size, full colour on every page, saddle stitched

Every bid, and what the validators decided:

| Bid | Price | Proposal | Verdict | Reason the leader gave (not consensus) |
|---|---|---|---|---|
| 0 | 1180 | We will print all 400 programmes on 100 percent recycled silk paper, A5, full... | **meets** | Commits to 100% recycled paper, delivery by 12 November 2026, and A5 full-colour saddle-stitched programmes for all 400 copies. |
| 1 | 950 | 400 programmes in A5, full colour throughout, saddle stitched, printed on our... | **fails** | Proposal specifies virgin-fibre paper, failing R0 which requires at least 70% recycled content. |
| 2 | 1240 | A5 programmes, full colour on every page, saddle stitched, printed on 80 perc... | **meets** | The proposal meets all requirements: 80% recycled paper, delivery by Nov 13 (before Nov 14), and A5 full-colour saddle stitched. |
| 3 | 1090 | Recycled paper, A5, full colour, stitched. We can deliver all 400 to the venu... | **unassessed** | - |

Every transaction, in order, refusals included:

| Step | Outcome | Transaction |
|---|---|---|
| tender 0 opened: three requirements | ok | [`0xf39a983b...`](https://explorer-studio.genlayer.com/tx/0xf39a983ba800ac26d9db7a549f3c8414335a336464ae61ff651c2885488adcf0) |
| the buyer bids on its own tender | refused: the buyer cannot bid on its own tender | [`0x255befee...`](https://explorer-studio.genlayer.com/tx/0x255befeeb22cdf612d3430192a843dcb7280f64174f03db9309a74f1ceb87e70) |
| bid 0: Ann, 1180 | ok | [`0x319c9e60...`](https://explorer-studio.genlayer.com/tx/0x319c9e60008d6c1536fb1ae77f764d8ac1b3146b1e2aab688c61d5e172ea0a77) |
| bid 1: Ben, 950, glossy virgin paper | ok | [`0xe4462e75...`](https://explorer-studio.genlayer.com/tx/0xe4462e75d64d2b1b5b89f4c9374cd8e618e077cbe5b5c1429373a4a74889ec6f) |
| bid 2: Cal, 1240 | ok | [`0x5fd7a6e8...`](https://explorer-studio.genlayer.com/tx/0x5fd7a6e8d2cbf3a6bbe3f26311fce9223ee5803797f5944e1e10462e3bcefc42) |
| bid 3: Dev, 1090, delivery on 20 November | ok | [`0xb4452bdb...`](https://explorer-studio.genlayer.com/tx/0xb4452bdb1d4081ef8e1970c8577cbed81a679b2758c967e6beb28575198c8858) |
| Ann bids a second time | refused: a supplier bids once per tender | [`0x006b588e...`](https://explorer-studio.genlayer.com/tx/0x006b588e0b6780d419bbb71e153357e3d278eaa3f7a8a98fa0c85a79e722eb65) |
| an assessment before bids close | refused: assessments open when bids close at 2026-10-05T23:39:27Z | [`0xd18ba0d1...`](https://explorer-studio.genlayer.com/tx/0xd18ba0d1244f94ce71b33ebf614054729af2cb8278b92236497186ade910cd31) |
| a bid after bids closed | refused: bids closed at 2026-10-05T23:39:27Z | [`0x382e946f...`](https://explorer-studio.genlayer.com/tx/0x382e946ff6f19a7cdaf3603244551136d0047d254dba113251aae6e14a6143c3) |
| a stranger asks for an assessment | refused: only the buyer or a bidder on this tender may ask for an assessment | [`0xaf47ef2d...`](https://explorer-studio.genlayer.com/tx/0xaf47ef2d09c4ee9384e1bd2c0eab6f9ab2ea0fb7a143fe6b893f792fc7e6dbc4) |
| bid 1 assessed: both orders | ok | [`0x1ccdeef4...`](https://explorer-studio.genlayer.com/tx/0x1ccdeef4247d112c29dd1bc6a21e5decb051f71337a11df6c57740543951de19) |
| bid 0 assessed: both orders | ok | [`0x99608abf...`](https://explorer-studio.genlayer.com/tx/0x99608abf37446b2f333bc482f0ca1bd10556206b2925e08589673ebb39b03f8f) |
| bid 2 assessed: both orders | ok | [`0xb8151efc...`](https://explorer-studio.genlayer.com/tx/0xb8151efcc3f835ab9ddb00b0ce2f10b25719e76a8b086ca27b7571bda94fdaf7) |
| an award while bid 3 waits | refused: bid 3 is waiting for its assessment until 2026-10-05T23:49:27Z | [`0x5666fe33...`](https://explorer-studio.genlayer.com/tx/0x5666fe33a0083e015ad2ec1f63dc3695f38c0b471d03034f2dd33247e1cffdc0) |
| bid 3 assessed after assessments closed | refused: assessments closed at 2026-10-05T23:49:27Z; a bid nobody assessed is not compliant at the award | [`0xd7ab2e39...`](https://explorer-studio.genlayer.com/tx/0xd7ab2e39ae3ca84982285c6c71479ad03a354d0dcdc7941c95ee4109b0906845) |
| tender 0 awarded | ok | [`0x78ec11d7...`](https://explorer-studio.genlayer.com/tx/0x78ec11d7ca0d0ef180b71611045dad1b982cd5e2c6be52f98afed1061394edbd) |

`tests/test_runbook.py::TestTheRecord` replays these verdicts through this repository's contract and fails unless it awards exactly what the deployed one did.
<!-- measured:deployment:end -->

## The problem

Every tender says "lowest compliant bid wins", and every disputed tender is an
argument about "compliant". The buyer who decides compliance also picks the
winner, so a favoured supplier is compliant and a cheaper rival "did not address
requirement 3", and the losing bidder has no way to tell which happened.

Asking a model "which bid should win?" does not fix it. It hands the model
compliance **and** price, and gets back the bid it liked. Tender splits them:
the requirements are frozen before any bid; the model answers only *does this
proposal meet every requirement*, one bid at a time, without the price; and
which compliant bid is cheapest is counted, not judged.

## How consensus is used

### Before any model: could any answer change the outcome?

The contract refuses for free, before a single prompt, an assessment asked for
by anyone but the buyer or a bidder, before bidding has closed, after
assessments have closed, or of a bid already assessed.

### The assessment

Otherwise the block sees the tender, the requirements and one proposal, and
picks one of two options the contract wrote itself:

```
<requirements>
[R0] Printed on paper with at least 70 percent recycled content
[R1] All 400 programmes delivered to the venue by 14 November 2026
[R2] A5 size, full colour on every page, saddle stitched
</requirements>

<proposal>
400 programmes in A5, full colour throughout, saddle stitched, printed on our standard glossy virgin-fibre paper ...
</proposal>

<options>
[0] meets: the proposal commits to every requirement
[1] fails: the proposal does not meet at least one requirement, or is silent or vague about one
</options>

answer: {"option": "1", "because": "..."}
```

A proposal meets the requirements only if it commits to every one of them; one
it does not address, or addresses only vaguely, is not met. The model is told
not to judge value, persuasiveness or likelihood of delivery, only what the
proposal commits to.

### Both orders

The leader asks **twice**, with the options in the order meets, fails and then
reversed and renumbered, and reads each answer back through the order it was
asked in. The same option in both orders stands; anything else is `fails`. A
proposal that only meets the requirements when "meets" is listed first does not
clearly meet them, and the bidder carries the burden of showing that it does.
A model that always answers "0" is order-dependent and qualifies nobody. The
uncertainty goes into the **value** (fails), never into the comparison.

### The validator, in two layers

1. **Structural, and free.** The verdict is `meets` or `fails`. Anything else
   is refused before the validator spends a single prompt.
2. **Exact agreement.** The validator asks both orders itself and compares.

An unusable answer is retried once inside the block and then raised as
`[LLM_ERROR]`, which a validator never agrees with, so a broken model can never
qualify a bid. There is no equivalence principle and no tolerance anywhere.

## What the contract decides, not the model

| At the award | Outcome |
|---|---|
| bids assessed `meets` | the lowest price wins; on a tie, the earliest bid |
| bids assessed `fails` | never win, however cheap |
| a bid nobody assessed before assessments closed | **unassessed**: never wins, however cheap |
| no bid meets the requirements | **no_award** |

## The state machine and its clocks

```
open       bids until bids_close; assessments from bids_close until assess_close
awarded    the winner is fixed
no_award   nothing met the requirements
```

| Clock | What happens after it |
|---|---|
| `bids_close` = open + bid window | no more bids; assessments open |
| `assess_close` = bids close + assessment window | `assess()` refuses for free, before any model; an unassessed bid is not compliant at the award, so a late assessment can never change a winner |
| the award | anyone, once every bid is assessed or once assessments have closed, whichever is first |

## Who may write

| Method | Caller | Why |
|---|---|---|
| `open(title, requirements, bid_window, assess_window)` | anyone | the caller becomes the buyer |
| `bid(id, price, proposal)` | anyone but the buyer, once per tender, until bids close | the bidder is recorded, and is the one awarded |
| `assess(id, bid)` | the buyer or any bidder on this tender, once per bid | an assessment spends inference on every validator, so only parties to the tender may ask; a rival may ask about a rival |
| `award(id)` | anyone, deliberately | it reads no model and only counts what the assessments already say; a buyer who has vanished cannot leave a tender undecided |

`tests/test_e2e.py::TestStorageShape::test_every_gated_write_checks_the_sender`
fails if `bid()` or `assess()` stops checking the sender, and
`test_the_buyer_has_no_say_over_the_winner_in_code` fails if the award ever
reads the buyer.

## The API

| View | Returns |
|---|---|
| `count()` | number of tenders |
| `status(id)` | `open`, `awarded` or `no_award`: one word for another contract |
| `winner_of(id)` | the winning supplier's address, or "" |
| `tender(id)` | buyer, status, the clocks, how many bids and assessments, the winning bid and price |
| `requirements_of(id)` | the requirements, in the frozen order |
| `bids_of(id)` | every bid: supplier, price, proposal, verdict, who asked for it, and the leader's reason |

## Running the tests

```bash
pip install pytest
pytest tests/ -q
```

<!-- measured:tests:start -->
Measured: **129 passed**, 1 skipped. The skipped tests are the opt-in StudioNet integration tests, which run with `GENLAYER_STUDIO=1`.
<!-- measured:tests:end -->

The suite runs on [`tests/glsim.py`](tests/glsim.py), a small GenVM stand-in
that executes the real contract file, gives the leader and the validator their
own mock answers, can make a leader lie, rolls back storage on a refusal, and
refuses what GenVM refuses.

- [`tests/test_logic.py`](tests/test_logic.py) - the pure rules: the requirements' shape, `winner()`, the answer read back through its order, the fold, the agreement, the fence and the prompt, and that `lib/tender_consensus.py` is the contract's own code
- [`tests/test_e2e.py`](tests/test_e2e.py) - the contract executed: bidding and its limits, the free refusals (zero prompts), the price the model never sees, the options in both orders, order-dependence, a leader that qualifies or disqualifies a bid, `[LLM_ERROR]` never agreed with, every clock on its last second, the award and its ties, and static checks over the parsed source
- [`tests/test_runbook.py`](tests/test_runbook.py) - the demo replayed offline before a transaction is spent, and the live record replayed through this code
- [`tests/test_integration.py`](tests/test_integration.py) - opt in, `GENLAYER_STUDIO=1`: senders, a TreeMap on a real address, and the free refusals on a real runtime

### The tests have teeth

[`scripts/mutate.py`](scripts/mutate.py) removes every defence one at a time
and names the test that caught each mutant. It refuses to run on a red
baseline and exits non-zero if anything escapes.

<!-- measured:mutations:start -->
Measured: **66 mutations, 66 caught, 0 escaped.**

| Mutation | Caught by |
|---|---|
| an option past the list is accepted | `test_an_unusable_answer_is_an_error_and_never_a_verdict` |
| an answer in words is read as a number | `test_an_unusable_answer_is_an_error_and_never_a_verdict` |
| the second pass is asked in the forward order | `test_the_options_follow_the_order_they_are_asked_in` |
| the reversed order is not reversed | `test_the_options_follow_the_order_they_are_asked_in` |
| a disagreement between the orders keeps the forward verdict | `test_an_answer_that_depends_on_the_order_is_fails` |
| a disagreement between the orders is meets | `test_an_answer_that_depends_on_the_order_is_fails` |
| an answer is not read back through its order | `test_a_bid_is_assessed_once` |
| an unusable answer is not retried | `test_an_unusable_answer_is_an_error_and_never_a_verdict` |
| an unusable answer is read as fails | `test_an_unusable_answer_is_an_error_and_never_a_verdict` |
| an answer that is not an object crashes the block | `test_an_unusable_answer_is_an_error_and_never_a_verdict` |
| the free structural layer is skipped | `test_a_verdict_that_is_neither_option_is_refused_for_free` |
| a validator agrees with a leader that raised | `test_an_unusable_answer_is_an_error_and_never_a_verdict` |
| a validator trusts the leader | `test_nodes_that_assess_differently_do_not_agree` |
| a validator whose own model failed agrees | `test_a_validator_whose_model_fails_does_not_agree` |
| unassessed is a sound verdict | `test_a_verdict_that_is_neither_option_is_refused_for_free` |
| agreement is not exact | `test_nodes_that_assess_differently_do_not_agree` |
| the agreed verdict is not checked again before it is stored | `test_the_agreed_verdict_is_checked_again_before_it_is_stored` |
| anyone may ask for an assessment | `test_only_the_buyer_or_a_bidder_may_ask` |
| only the buyer may ask for an assessment | `test_the_buyer_or_any_bidder_may_ask_even_about_a_rival` |
| an assessment is taken before bids close | `test_an_assessment_waits_for_bids_to_close` |
| an assessment is taken after assessments close | `test_an_assessment_on_the_last_second_lands_and_one_after_is_refused_for_free` |
| an assessment on the last second is refused | `test_an_assessment_on_the_last_second_lands_and_one_after_is_refused_for_free` |
| a bid is assessed twice | `test_a_bid_is_assessed_once` |
| an assessment is taken on a decided tender | `test_a_decided_tender_takes_nothing_more` |
| a bid of another tender is assessed here | `test_a_bid_of_another_tender_is_refused` |
| an assessment is not counted | `test_meets_and_fails_are_stored_with_who_asked` |
| the buyer may bid on its own tender | `test_the_buyer_cannot_bid_on_its_own_tender` |
| bids are taken after bids close | `test_bids_close_on_the_clock` |
| a bid on the last second is refused | `test_bids_close_on_the_clock` |
| a supplier may bid any number of times | `test_a_supplier_bids_once` |
| a bid is not remembered against its supplier | `test_a_supplier_bids_once` |
| a tender takes any number of bids | `test_a_tender_takes_at_most_twenty_bids` |
| a price of zero is accepted | `test_malformed_bids_are_refused` |
| the proposal is unbounded | `test_malformed_bids_are_refused` |
| bids are not linked | `test_a_supplier_bids_once` |
| the award is made while bids are open | `test_nothing_is_awarded_while_bids_are_open` |
| an unassessed bid does not hold the award | `test_a_cheaper_bid_nobody_assessed_cannot_win` |
| an unassessed bid is never marked | `test_a_cheaper_bid_nobody_assessed_cannot_win` |
| a tender is decided twice | `test_a_decided_tender_takes_nothing_more` |
| a bid that fails can win | `test_the_lowest_price_that_meets_the_requirements_wins_not_the_lowest_price` |
| an unassessed bid can win | `test_a_cheaper_bid_nobody_assessed_cannot_win` |
| the highest price wins | `test_the_lowest_price_that_meets_the_requirements_wins_not_the_lowest_price` |
| a tie goes to the latest bid | `test_a_tie_goes_to_the_earliest_bid` |
| no award still names a winner | `test_nothing_meets_and_nothing_is_awarded` |
| the winner is not recorded | `test_the_lowest_price_that_meets_the_requirements_wins_not_the_lowest_price` |
| the winner is off by one | `test_the_lowest_price_that_meets_the_requirements_wins_not_the_lowest_price` |
| the requirements refusal is ignored | `test_malformed_requirements_are_refused` |
| an empty list of requirements is accepted | `test_malformed_requirements_are_refused` |
| more than six requirements are accepted | `test_malformed_requirements_are_refused` |
| a requirement of any length is accepted | `test_malformed_requirements_are_refused` |
| two requirements with the same wording are accepted | `test_malformed_requirements_are_refused` |
| a missing requirement is dropped and the rest renumbered | `test_malformed_requirements_are_refused` |
| the windows are unbounded | `test_both_windows_are_bounded` |
| the assessment window is unbounded | `test_both_windows_are_bounded` |
| assessments close with the bids | `test_a_tender_opens_with_its_requirements_and_clocks_frozen` |
| the title is unbounded | `test_the_title_is_bounded` |
| the fence is removed | `test_caller_text_is_stored_verbatim_and_fenced_only_at_the_prompt` |
| the fence leaves square brackets | `test_caller_text_is_stored_verbatim_and_fenced_only_at_the_prompt` |
| the proposal reaches the prompt unfenced | `test_caller_text_is_stored_verbatim_and_fenced_only_at_the_prompt` |
| the requirements reach the prompt unfenced | `test_caller_text_is_stored_verbatim_and_fenced_only_at_the_prompt` |
| the title reaches the prompt unfenced | `test_every_value_interpolated_into_the_prompt_is_fenced_or_ours` |
| the prompt no longer says vague is not met | `test_the_prompt_asks_about_commitments_and_never_shows_a_price` |
| the prompt asks about value for money | `test_the_prompt_asks_about_commitments_and_never_shows_a_price` |
| a leader's reason is stored as sent | `test_the_reason_is_not_compared_and_is_stored_sanitised` |
| a leader's reason is stored uncapped | `test_the_reason_is_not_compared_and_is_stored_sanitised` |
| control characters are stored | `test_clean_text_collapses_whitespace_and_control_characters` |
<!-- measured:mutations:end -->

## Design rules applied

- **Settle what can be settled before the model:** an assessment that could change nothing is refused for free.
- **The coarsest answer that still carries the judgment:** one of two options the contract wrote, per bid.
- **No single call reveals what only the contract should see:** no price ever enters the prompt, and no bid is compared with another by a model.
- **Uncertainty in the value, never in the comparison:** an order-dependent verdict is fails.
- **Every judgment has a clock:** nothing is assessed after `assess_close`, and an unassessed bid cannot win.
- **Tagging untrusted text is not a fence:** `fence()` at the prompt boundary, requirements and options labelled by the contract.
- **The deployment is the submission:** `scripts/verify_deployment.py` reads the deployed source back and lints it.

## Further reading in this repository

- [DECISIONS.md](DECISIONS.md) - why each rule is the way it is
- [DEPLOY.md](DEPLOY.md) - the demo, step by step
- [SUBMISSION.md](SUBMISSION.md) - what to check before submitting
- [`lib/tender_consensus.py`](lib/tender_consensus.py) - the assessment and award rules, generated from the contract

## Related work

- [Warranty](https://github.com/meitipro/warranty) - a warranty with its payouts paid in before the sale closes
- [Tally](https://github.com/meitipro/tally) - an invoice paid line by line, only for what the order ordered
- [Mandate](https://github.com/meitipro/mandate) - a treasury that pays only what its charter allows

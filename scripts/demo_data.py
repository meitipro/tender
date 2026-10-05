"""The demo's data, in one place.

scripts/demo.py sends exactly these values to StudioNet, and
tests/test_runbook.py replays them offline, so the demo on the explorer and the
demo the tests check cannot drift apart.

One tender for 400 printed programmes with three mandatory requirements, and
four suppliers. Each bid changes one thing, so each rule of the contract shows
once, on chain:

  ANN    1180   recycled, on time, A5 full colour stitched: meets
  BEN     950   the cheapest, on glossy virgin paper: fails requirement 0
  CAL    1240   recycled, on time, A5 full colour stitched: meets
  DEV    1090   cheaper than Ann, but nobody asks for it to be assessed before
                assessments close: unassessed, not compliant

The award goes to Ann at 1180: not the cheapest bid, and not the cheapest
unassessed one, but the cheapest that meets every requirement.
"""

TITLE = "400 programmes for the GenLayer builders' day, Leeds (prices in euros)"
REQUIREMENTS = [
    "Printed on paper with at least 70 percent recycled content",
    "All 400 programmes delivered to the venue by 14 November 2026",
    "A5 size, full colour on every page, saddle stitched",
]
BID_WINDOW = 480
ASSESS_WINDOW = 600

ANN = ("We will print all 400 programmes on 100 percent recycled silk paper, A5, full colour on every page "
       "and saddle stitched, and deliver them to the venue on 12 November 2026.")
ANN_PRICE = 1180
BEN = ("400 programmes in A5, full colour throughout, saddle stitched, printed on our standard glossy "
       "virgin-fibre paper and delivered to the venue on 10 November 2026.")
BEN_PRICE = 950
CAL = ("A5 programmes, full colour on every page, saddle stitched, printed on 80 percent recycled paper; "
       "all 400 delivered to the venue by 13 November 2026.")
CAL_PRICE = 1240
DEV = ("Recycled paper, A5, full colour, stitched. We can deliver all 400 to the venue on 20 November 2026, "
       "after our current print run.")
DEV_PRICE = 1090
LATE = ("All 400 programmes on recycled paper, A5 full colour, saddle stitched, delivered by 1 November 2026.")
LATE_PRICE = 800


def joined(reqs):
    return "|".join(reqs)


# The demo, step by step, exactly as scripts/demo.py sends it and
# tests/test_runbook.py replays it: (who, method, arguments, expected, label).
# A step marked "after_bids" waits until bids have closed; "after_assess" until
# assessments have closed. Bids are numbered as the contract numbers them:
# 0 Ann, 1 Ben, 2 Cal, 3 Dev.
STEPS = [
    ("buyer", "open", (TITLE, REQUIREMENTS, BID_WINDOW, ASSESS_WINDOW), "ok", "tender 0 opened: three requirements"),
    ("buyer", "bid", (0, ANN_PRICE, ANN), "refused", "the buyer bids on its own tender"),
    ("ann", "bid", (0, ANN_PRICE, ANN), "ok", "bid 0: Ann, 1180"),
    ("ben", "bid", (0, BEN_PRICE, BEN), "ok", "bid 1: Ben, 950, glossy virgin paper"),
    ("cal", "bid", (0, CAL_PRICE, CAL), "ok", "bid 2: Cal, 1240"),
    ("dev", "bid", (0, DEV_PRICE, DEV), "ok", "bid 3: Dev, 1090, delivery on 20 November"),
    ("ann", "bid", (0, 999, ANN), "refused", "Ann bids a second time"),
    ("ann", "assess", (0, 0), "refused", "an assessment before bids close"),
    ("stranger", "bid", (0, LATE_PRICE, LATE), "refused", "a bid after bids closed", "after_bids"),
    ("stranger", "assess", (0, 1), "refused", "a stranger asks for an assessment"),
    ("buyer", "assess", (0, 1), "ok", "bid 1 assessed: both orders"),
    ("ann", "assess", (0, 0), "ok", "bid 0 assessed: both orders"),
    ("cal", "assess", (0, 2), "ok", "bid 2 assessed: both orders"),
    ("stranger", "award", (0,), "refused", "an award while bid 3 waits"),
    ("dev", "assess", (0, 3), "refused", "bid 3 assessed after assessments closed", "after_assess"),
    ("stranger", "award", (0,), "ok", "tender 0 awarded", "after_assess"),
]

# What each ok assessment is expected to come back with, in order.
EXPECTED_VERDICTS = ["fails", "meets", "meets"]

"""Integration tests, run against StudioNet.

    pip install genlayer-py==0.18.0
    GENLAYER_STUDIO=1 pytest tests/test_integration.py -v

They are opt in. Without GENLAYER_STUDIO set they skip, so `pytest tests/ -q`
stays clean and offline on a reviewer's machine whatever is installed there,
and an unreachable network can never be mistaken for a broken contract.

They exercise the deterministic half on a real runtime, where the simulator is
weakest: the sender is derived from a signature rather than set by a test, a
TreeMap is keyed on a real address, and the free refusals before any model are
shown to cost no inference. The assessments themselves cost inference on every
validator and are on the record from scripts/demo.py.
"""

import os
import pathlib
import sys

import pytest

if not os.environ.get("GENLAYER_STUDIO"):
    pytest.skip("integration tests run against StudioNet and are opt in: set GENLAYER_STUDIO=1. "
                "Everything else runs offline with pytest tests/ -q", allow_module_level=True)

pytest.importorskip("genlayer_py", reason="pip install genlayer-py==0.18.0")

sys.path.insert(0, str(pathlib.Path(__file__).absolute().parent.parent / "scripts"))
from studio import Studio                                     # noqa: E402

CODE = (pathlib.Path(__file__).absolute().parent.parent / "contracts" / "tender.py").read_text(encoding="utf-8")
TITLE = "Programmes, integration run"
REQS = "Printed on paper with at least 70 percent recycled content|A5 size, full colour, saddle stitched"
PROPOSAL = "Recycled paper, A5, full colour throughout, saddle stitched, delivered on time."


@pytest.fixture(scope="module")
def world():
    s = Studio()
    buyer = s.account("buyer")
    supplier = s.account("supplier")
    address = s.deploy(buyer, CODE, [])
    s.write(buyer, address, "open", [TITLE, REQS, 3600, 3600], step="open a tender")
    return s, address, buyer, supplier


def test_a_tender_opens_with_the_signer_as_buyer(world):
    s, address, buyer, _ = world
    t = s.read(address, "tender", [0])
    assert t["status"] == "open" and t["buyer"].lower() == buyer.address.lower() and t["requirements"] == 2


def test_the_buyer_cannot_bid(world):
    s, address, buyer, _ = world
    row = s.write(buyer, address, "bid", [0, 100, PROPOSAL], step="the buyer bids", expect="refused")
    assert "the buyer cannot bid" in row["refusal"]


def test_a_supplier_bids_once_keyed_on_its_real_address(world):
    s, address, _, supplier = world
    s.write(supplier, address, "bid", [0, 100, PROPOSAL], step="a supplier bids")
    row = s.write(supplier, address, "bid", [0, 90, PROPOSAL], step="the supplier bids again", expect="refused")
    assert "bids once per tender" in row["refusal"]
    assert [b["price"] for b in s.read(address, "bids_of", [0])["bids"]] == ["100"]


def test_an_assessment_before_bids_close_is_refused_for_free(world):
    s, address, _, supplier = world
    row = s.write(supplier, address, "assess", [0, 0], step="assess too early", expect="refused")
    assert "assessments open when bids close" in row["refusal"]
    assert s.read(address, "bids_of", [0])["bids"][0]["verdict"] == ""


def test_an_unknown_tender_is_a_refusal_not_the_newest_row(world):
    s, address, _, supplier = world
    row = s.write(supplier, address, "award", [99], step="award a tender that does not exist", expect="refused")
    assert "no such tender" in row["refusal"]

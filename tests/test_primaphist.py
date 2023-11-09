import pytest
from pytest import approx

from openclimatedata import PRIMAPHIST

versions = PRIMAPHIST.keys()

def test_primaphist():
    for version in versions:
        assert PRIMAPHIST[version]

def test_primaphist_2_5():
    df = PRIMAPHIST["2.5"].to_dataframe()
    assert df.iloc[0]["1750"] == approx(0.00564)
    assert df.iloc[0]["provenance"] == "measured"
    assert df.iloc[-1]["2022"] == approx(0.0)

    ocdf = PRIMAPHIST["2.5"].to_ocd()
    # First and last value should be the same after re-shaping.
    assert ocdf.iloc[0]["value"] == df.iloc[0]["1750"]
    assert ocdf.iloc[-1]["value"] == df.iloc[-1]["2022"]

    assert ocdf.iloc[0]["provenance"] == "measured"

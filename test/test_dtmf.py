import pytest
import src.dtmf as dtmf


def test_main():
    sig = dtmf.Signal()
    assert sig.sr== 8000

import functions as fun
from clig import Command


def test_posWithType_kwWithType_kwBoolWithType_cligDocMultiline():
    cmd = Command(fun.ptc_kti_ktb_cligDocMutiline)
    cmd._add_parsers()

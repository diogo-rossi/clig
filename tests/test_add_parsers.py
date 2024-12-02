import sys
from pathlib import Path

path = Path(__file__).parent
sys.path.insert(0, str((path).resolve()))
sys.path.insert(0, str((path / "../src").resolve()))

from clig import Command
import functions as fun


def test_posWithType_kwWithType_kwBoolWithType_cligDocMultiline():
    cmd = Command(fun.posWithType_kwWithType_kwBoolWithType_cligDocMultiline)
    cmd.add_parsers()

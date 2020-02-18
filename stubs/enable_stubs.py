import sys
from pathlib import Path

class StubbedModule():
    pass

def get_stubs_directory():
    return str(Path(__file__).parent)

def enable_stubs():
    import opensfm
    opensfm.csfm = StubbedModule()
    opensfm.csfm.DepthmapPruner = StubbedModule()
    sys.modules["pyopengv"] = StubbedModule()
    sys.path.insert(0, get_stubs_directory())

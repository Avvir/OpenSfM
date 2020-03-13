import sys
from pathlib import Path

class StubbedModule():
    def __call__(self, *args, **kwargs):
        pass

def get_stubs_directory():
    return str(Path(__file__).parent)

def enable_stubs():
    import opensfm
    opensfm.csfm = StubbedModule()
    opensfm.csfm.DepthmapPruner = StubbedModule()
    opensfm.pyfeatures = StubbedModule()
    opensfm.pydense = StubbedModule()
    opensfm.pygeometry = StubbedModule()
    opensfm.pyrobust = StubbedModule()
    opensfm.pybundle = StubbedModule()
    sys.modules["pyopengv"] = StubbedModule()
    sys.path.insert(0, get_stubs_directory())

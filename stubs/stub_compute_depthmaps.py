import os
from argparse import Namespace

from stubs.enable_stubs import enable_stubs
enable_stubs()
from opensfm.commands.compute_depthmaps import Command as ComputeDepthmaps



project_directory = os.path.expandvars("$HOME/avvir/data/SampleVideoWalk_opensfm")
args = Namespace(command='compute_depthmaps', dataset=project_directory, interactive=False, subfolder='undistorted')
command = ComputeDepthmaps()
command.run(args)

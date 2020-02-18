import os
from argparse import Namespace

from stubs.enable_stubs import enable_stubs
enable_stubs()
from opensfm.commands.undistort import Command as UndistortCommand



project_directory = os.path.expandvars("$HOME/avvir/data/SampleVideoWalk_opensfm")
# args = Namespace(command='compute_depthmaps', dataset=project_directory, interactive=False, subfolder='undistorted')
args = Namespace(command='undistort', dataset=project_directory, output='undistorted', reconstruction=None, reconstruction_index=0, tracks=None)
command = UndistortCommand()
command.run(args)

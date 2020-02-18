from stubs.enable_stubs import enable_stubs
enable_stubs()
import os
from opensfm.commands.undistort import Command as UndistortCommand


class RunArgs:
    pass


args = RunArgs()
args.dataset = os.path.expandvars("$HOME/avvir/data/SampleVideoWalk_opensfm")
args.output = os.path.expandvars("$HOME/avvir/data/SampleVideoWalk_opensfm")
args.reconstruction = os.path.expandvars("$HOME/avvir/data/SampleVideoWalk_opensfm/reconstruction.json")
args.tracks = os.path.expandvars("$HOME/avvir/data/SampleVideoWalk_opensfm/reports/tracks.json")
command = UndistortCommand()
command.run(args)

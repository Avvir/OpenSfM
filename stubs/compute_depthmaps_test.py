from argparse import Namespace
from pathlib import Path

from pynetest.expectations import expect
from pynetest.pyne_test_collector import describe, it, before_each
from pynetest.pyne_tester import pyne
from pynetest.test_doubles.attached_spy import attach_stub
from pynetest.test_doubles.spy import last_call_of
from pynetest.test_doubles.stub import group_stubs

from stubs.enable_stubs import enable_stubs

enable_stubs()

from opensfm import io, dense
from opensfm.commands.compute_depthmaps import Command as ComputeDepthmaps


def get_undistorted_path():
    return Path(__file__).parent / "resources" / "undistorted"

def some_data():
    class Data:
        def __init__(self):
            self.config = dict()
            self.config["processes"] = 1
            self.config["depthmap_num_neighbors"] = 5
            self.config["depthmap_min_depth"] = 0
            self.config["depthmap_max_depth"] = 1

    return Data()

@pyne
def compute_depthmaps_test():
    @before_each
    def _(self):
        reconstruction_path = str(get_undistorted_path() / "reconstruction.json")
        neighbors_path = str(get_undistorted_path() / "neighbors.json")

        with io.open_rt(reconstruction_path) as fin:
            reconstruction = io.reconstructions_from_json(io.json_load(fin))[0]
        self.shot_id = "1579044395.47_img_00088.jpg_perspective_view_front"
        self.lonely_shot_id = "1579044395.47_img_00088.jpg_perspective_view_back"

        self.shot = reconstruction.shots[self.shot_id]
        self.lonely_shot = reconstruction.shots[self.lonely_shot_id]
        self.shots_dict = reconstruction.shots

        self.expected_shot_ids = ["1579044395.47_img_00089.jpg_perspective_view_back", "1579044395.47_img_00081.jpg_perspective_view_bottom", "1579044395.47_img_00079.jpg_perspective_view_front"]
        self.neighbors_dict = { self.shot_id: self.expected_shot_ids, self.lonely_shot_id: [] }

        with io.open_wt(neighbors_path) as fp:
            io.json_dump(self.neighbors_dict, fp)

        self.data = some_data()
        self.reconstruction = reconstruction

    @describe("#run")
    def _():
        @it("loads the neighbors.json file if it exists")
        def _(self):
            args = Namespace(command='compute_depthmaps', dataset=get_undistorted_path().parent, interactive=False, subfolder='undistorted')
            command = ComputeDepthmaps()

            with group_stubs(
                    attach_stub(dense, "compute_depthmaps")):
                command.run(args)
                expect(dense.compute_depthmaps).was_called()
                args, kwargs = last_call_of(dense.compute_depthmaps)
                expect(args).to_have_length(4)
                data, graph, reconstrunction, neighbors_dict = args
                expect(graph).to_be_none()
                expect(neighbors_dict).to_be(self.neighbors_dict)

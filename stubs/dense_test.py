from pathlib import Path

from pynetest.expectations import expect
from pynetest.pyne_test_collector import describe, it, before_each
from pynetest.pyne_tester import pyne
from pynetest.test_doubles.attached_spy import attach_stub
from pynetest.test_doubles.stub import group_stubs

from stubs.enable_stubs import enable_stubs

enable_stubs()

from opensfm import io, dense
from opensfm.dense import lookup_neighboring_images, compute_depthmaps
from opensfm.types import Shot

def get_project_path():
    return Path(__file__).parent / "resources"

def get_undistorted_path():
    return get_project_path() / "undistorted"


def some_data():
    class Data:
        def __init__(self):
            self.config = dict()
            self.config["processes"] = 1
            self.config["depthmap_num_neighbors"] = 5
            self.config["depthmap_min_depth"] = 0
            self.config["depthmap_max_depth"] = 1
            self.data_path = get_project_path()
    return Data()

@pyne
def dense_test():
    @before_each
    def _(self):
        reconstruction_path = str(get_undistorted_path() / "reconstruction.json")
        with io.open_rt(reconstruction_path) as fin:
            reconstruction = io.reconstructions_from_json(io.json_load(fin))[0]
        self.shot_id = "1579044395.47_img_00088.jpg_perspective_view_front"
        self.lonely_shot_id = "1579044395.47_img_00088.jpg_perspective_view_back"
        self.shot = reconstruction.shots[self.shot_id]
        self.lonely_shot = reconstruction.shots[self.lonely_shot_id]
        self.shots_dict = reconstruction.shots
        self.expected_shot_ids = ["1579044395.47_img_00089.jpg_perspective_view_back", "1579044395.47_img_00081.jpg_perspective_view_bottom", "1579044395.47_img_00079.jpg_perspective_view_front"]
        self.neighbors_dict = { self.shot_id: self.expected_shot_ids, self.lonely_shot_id: [] }
        self.data = some_data()
        self.reconstruction = reconstruction

    @describe("#lookup_neighboring_images")
    def _():
        @it("returns the neighboring shots for the shot using the neighbor dict")
        def _(self):
            actual_shots = lookup_neighboring_images(self.shot, self.shots_dict, self.neighbors_dict)
            expect(actual_shots).to_be_a(list)
            actual_shot_ids = set([shot.id for shot in actual_shots])
            expect(actual_shots[0]).to_be_a(Shot)
            expect(actual_shots).to_have_length(len(self.expected_shot_ids))
            expect(actual_shot_ids).to_be(set(self.expected_shot_ids))

        @describe("when the shot has no neighbors")
        def _():
            @it("returns an empty list")
            def _(self):
                actual_shots = lookup_neighboring_images(self.lonely_shot, self.shots_dict, self.neighbors_dict)
                expect(actual_shots).to_be_a(list)
                expect(actual_shots).to_have_length(0)

    @describe("#compute_depthmaps")
    def _():
        @it("It uses the neighbors dict and config depths")
        def _(self):
            with group_stubs(

                    attach_stub(dense, "lookup_neighboring_images").call_real(),
                    attach_stub(dense, "config_depth_range").call_real(),
                    attach_stub(dense, "compute_depthmap"),
                    attach_stub(dense, "merge_depthmaps"),
                    attach_stub(dense, "clean_depthmap"),
                    attach_stub(dense, "prune_depthmap")):
                compute_depthmaps(self.data, None, self.reconstruction, self.neighbors_dict)
                expect(dense.lookup_neighboring_images).was_called()
                expect(dense.config_depth_range).was_called()
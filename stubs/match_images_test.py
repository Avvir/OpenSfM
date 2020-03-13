from pathlib import Path

from pynetest.expectations import expect
from pynetest.pyne_test_collector import describe, it, before_each
from pynetest.pyne_tester import pyne
from pynetest.test_doubles.attached_spy import attach_stub
from pynetest.test_doubles.spy import last_call_of
from pynetest.test_doubles.stub import group_stubs

from stubs.enable_stubs import enable_stubs

enable_stubs()

from opensfm import io, dense, matching
from opensfm.dense import lookup_neighboring_images, compute_depthmaps
from opensfm.types import Shot


def get_data_path():
    return Path(__file__).parent / "resources"

def get_adjacency_list_path():
    return get_data_path() / "match_adjacency_list.json"

def some_data():
    from opensfm.dataset import DataSet
    class Data(DataSet):
        def __init__(self):
            self.config = dict()
            self.config["processes"] = 1
            self.config["depthmap_num_neighbors"] = 5
            self.config["depthmap_min_depth"] = 0
            self.config["depthmap_max_depth"] = 1
            self.data_path = get_data_path()

        def load_exif(self, im):
            pass

    return Data()

@pyne
def match_images_test():
    @before_each
    def _(self):
        adjacency_list_path = get_adjacency_list_path()
        with io.open_rt(adjacency_list_path) as fin:
            adjacency_list = io.json_load(fin)
        self.data = some_data()
        self.images = sorted(adjacency_list.keys())
        self.expected_pairs = [('0000.jpg', '0001.jpg'), ('0001.jpg', '0002.jpg'), ('0002.jpg', '0003.jpg')]
        return

    @describe("#match_images")
    def _():
        @it("It generates pairs from the adjacency list")
        def _(self):
            with attach_stub(matching, "match_images_with_pairs"):
                images = self.images
                pairs_matches, preport = matching.match_images(self.data, images, images)
                args, kwargs = last_call_of(matching.match_images_with_pairs)
                data, exifs, ref_images, pairs = args
                expect(pairs).to_be(self.expected_pairs)

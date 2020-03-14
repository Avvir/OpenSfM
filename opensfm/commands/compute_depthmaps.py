import logging
from pathlib import Path

from opensfm import dataset, io
from opensfm import dense

logger = logging.getLogger(__name__)


class Command:
    name = 'compute_depthmaps'
    help = "Compute depthmap"

    def add_arguments(self, parser):
        parser.add_argument(
            'dataset',
            help='dataset to process',
        )
        parser.add_argument(
            '--subfolder',
            help='undistorted subfolder where to load and store data',
            default='undistorted'
        )
        parser.add_argument(
            '--interactive',
            help='plot results as they are being computed',
            action='store_true',
        )

    def run(self, args):
        data = dataset.DataSet(args.dataset)
        udata = dataset.UndistortedDataSet(data, args.subfolder)
        neighbors_path: Path = Path(data.data_path) / args.subfolder / "neighbors.json"

        data.config['interactive'] = args.interactive
        graph, neighbors_dict = None, None
        reconstructions = udata.load_undistorted_reconstruction()
        if neighbors_path.exists():
            with io.open_rt(neighbors_path) as fp:
                neighbors_dict = io.json_load(fp)
        else:
            graph = udata.load_undistorted_tracks_graph()

        dense.compute_depthmaps(udata, graph, reconstructions[0], neighbors_dict)

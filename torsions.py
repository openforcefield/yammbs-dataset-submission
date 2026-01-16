# Usage:
# python torsions.py path/to/config.yaml ncpus

import logging
import sys
from pathlib import Path

if True:  # to prevent future reordering around this import
    import qcportal  # noqa

from openff.toolkit.utils import OpenEyeToolkitWrapper
from yammbs.torsion import TorsionStore
from yammbs.torsion.inputs import QCArchiveTorsionDataset
from yammbs.scripts.run_torsion_comparisons import analyse_torsions

from config import Config

logging.basicConfig(level=logging.DEBUG)


if __name__ == "__main__":

    assert OpenEyeToolkitWrapper().is_available()

    if len(sys.argv) < 3:
        print("Not enough arguments")
        exit(1)

    conf = Config.from_file(sys.argv[1])

    ndatasets = len(conf.datasets)
    if ndatasets == 0:
        print("Must provide at least one dataset")
        exit(1)
    if ndatasets > 1:
        print("Only single dataset currently supported")
        exit(1)

    p = Path(sys.argv[1])
    out_dir = p.parent / "output"
    out_dir.mkdir(exist_ok=True)

    analyse_torsions(
        force_fields=[conf.forcefield],
        qcarchive_torsion_data=conf.datasets[0],
        database_file=out_dir / "torsions.sqlite",
        output_metrics=out_dir / "metrics.json",
        output_minimized=out_dir / "minimized.json",
        plot_dir=out_dir,
        metrics_csv_output_dir=out_dir,
        n_processes=int(sys.argv[2]),
    )

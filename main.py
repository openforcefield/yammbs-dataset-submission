# Usage:
# python main2.py path/to/config.yaml ncpus

import os
import sys
import time
from pathlib import Path

if True:  # to prevent future reordering around this import
    import qcportal  # noqa

from openff.toolkit.utils import OpenEyeToolkitWrapper
from yammbs import MoleculeStore
from yammbs.inputs import QCArchiveDataset

from config import Config

assert OpenEyeToolkitWrapper().is_available()


def make_csvs(store, forcefield, out_dir):
    print("getting DDEs")
    store.get_dde(forcefield, skip_check=True).to_csv(f"{out_dir}/dde.csv")
    print("getting RMSDs")
    store.get_rmsd(forcefield, skip_check=True).to_csv(f"{out_dir}/rmsd.csv")
    print("getting TFDs")
    store.get_tfd(forcefield, skip_check=True).to_csv(f"{out_dir}/tfd.csv")
    print("getting internal coordinate RMSDs")
    store.get_internal_coordinate_rmsd(forcefield, skip_check=True).to_csv(
        f"{out_dir}/icrmsd.csv"
    )


def _main(forcefield, dataset, sqlite_file, out_dir, procs, invalidate_cache):
    if invalidate_cache and os.path.exists(sqlite_file):
        os.remove(sqlite_file)
    if os.path.exists(sqlite_file):
        print(f"loading existing database from {sqlite_file}", flush=True)
        store = MoleculeStore(sqlite_file)
    else:
        print(f"loading cached dataset from {dataset}", flush=True)
        with open(dataset) as inp:
            crc = QCArchiveDataset.model_validate_json(inp.read())
        store = MoleculeStore.from_qcarchive_dataset(crc, sqlite_file)

    print("started optimizing store", flush=True)
    start = time.time()
    store.optimize_mm(force_field=forcefield, n_processes=procs)
    print(f"finished optimizing after {time.time() - start} sec")

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    make_csvs(store, forcefield, out_dir)


if __name__ == "__main__":
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

    _main(
        forcefield=conf.forcefield,
        dataset=conf.datasets[0],
        sqlite_file="tmp.sqlite",
        out_dir=out_dir,
        procs=int(sys.argv[2]),
        invalidate_cache=True,
    )

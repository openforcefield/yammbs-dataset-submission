# Usage:
# python main2.py path/to/config.yaml ncpus

import os
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import yaml
from openff.toolkit.utils import OpenEyeToolkitWrapper
from yammbs import MoleculeStore
from yammbs.cached_result import CachedResultCollection

assert OpenEyeToolkitWrapper().is_available()


@dataclass
class Config:
    forcefield: str
    datasets: list[str]

    @classmethod
    def from_file(cls, filename):
        with open(filename) as inp:
            d = yaml.load(inp, Loader=yaml.Loader)
            return cls(**d)


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
        crc = CachedResultCollection.from_json(dataset)
        store = MoleculeStore.from_cached_result_collection(crc, sqlite_file)

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
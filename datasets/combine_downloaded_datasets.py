"""Combines already-downloaded datasets (each with an existing cache.json) into
a single combined yammbs.QCArchiveDataset, without re-downloading anything from
QCArchive.

Usage:
    python combine_downloaded_datasets.py -o OUT_DIR DS_DIR [DS_DIR ...]

Each DS_DIR is the path to an existing dataset subdirectory (as produced by
download_and_filter_dataset.py or download_and_combine_datasets.py) containing
a cache.json file. The per-dataset yammbs.QCArchiveDatasets loaded from those
files are combined into a single yammbs.QCArchiveDataset, reassigning molecule
ids sequentially, and saved as OUT_DIR/cache.json. A README.md listing the
source datasets is also written to OUT_DIR.

If no DS_DIR arguments are given, defaults to the three NSP Optimization Set 1
datasets (Nitrogen, Phosphorus, Sulfur) in this directory.
"""

import argparse
import logging
from datetime import date
from pathlib import Path

from yammbs.inputs import QCArchiveDataset

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DEFAULT_DS_DIRS = [
    "OpenFF-NSP-Optimization-Set-1-Nitrogen-v4.0",
    "OpenFF-NSP-Optimization-Set-1-Phosphorus-v4.0",
    "OpenFF-NSP-Optimization-Set-1-Sulfur-v4.0",
]


def load_dataset(ds_dir: Path) -> QCArchiveDataset:
    """Load the yammbs.QCArchiveDataset from ``ds_dir / "cache.json"``."""

    cache_path = ds_dir / "cache.json"
    logger.info(f"Loading {cache_path}")
    with open(cache_path) as inp:
        return QCArchiveDataset.model_validate_json(inp.read())


def combine_datasets(datasets: dict[str, QCArchiveDataset]) -> QCArchiveDataset:
    """Combine multiple yammbs.QCArchiveDatasets into one, reassigning
    molecule ids sequentially across the combined set."""

    qm_molecules = [
        molecule.model_copy(update={"id": i})
        for i, molecule in enumerate(
            molecule
            for dataset in datasets.values()
            for molecule in dataset.qm_molecules
        )
    ]

    return QCArchiveDataset(
        tag=f"Combined dataset ({', '.join(datasets)})",
        qm_molecules=qm_molecules,
    )


def write_readme(out_dir: Path, datasets: dict[str, QCArchiveDataset]) -> None:
    """Write a README.md into ``out_dir`` documenting the source datasets used
    to build the combined cache.json."""

    lines = [
        "# Combined dataset",
        "",
        "This dataset was created by combining the following already-downloaded "
        "QCArchive datasets with `combine_downloaded_datasets.py`:",
        "",
    ]

    for ds_name, dataset in datasets.items():
        lines.append(f"- `{ds_name}` ({len(dataset.qm_molecules)} molecules)")

    total = sum(len(dataset.qm_molecules) for dataset in datasets.values())

    lines += [
        "",
        f"Total: {total} molecules.",
        "",
        f"Generated on {date.today().isoformat()}.",
        "",
        "The `cache.json` in this directory is the union of the source "
        "datasets' `cache.json` files and is the file that should be used "
        "for benchmark runs.",
    ]

    with open(out_dir / "README.md", "w") as out:
        out.write("\n".join(lines) + "\n")


def main():
    a = argparse.ArgumentParser(
        prog="python combine_downloaded_datasets.py",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    a.add_argument(
        "ds_dirs",
        nargs="*",
        default=DEFAULT_DS_DIRS,
        help="Paths to already-downloaded dataset directories, each "
        "containing a cache.json. Defaults to the three NSP Optimization "
        "Set 1 datasets (Nitrogen, Phosphorus, Sulfur).",
    )
    a.add_argument(
        "--out-dir",
        "-o",
        required=True,
        help="The name of the directory to create for the combined dataset",
    )
    args = a.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True)

    datasets: dict[str, QCArchiveDataset] = {
        Path(ds_dir).name: load_dataset(Path(ds_dir)) for ds_dir in args.ds_dirs
    }

    logger.info("Combining datasets")
    combined = combine_datasets(datasets)
    with open(out_dir / "cache.json", "w") as out:
        out.write(combined.model_dump_json())

    write_readme(out_dir, datasets)
    logger.info(f"Wrote combined dataset with {len(combined.qm_molecules)} molecules to {out_dir}")


if __name__ == "__main__":
    main()

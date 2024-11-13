import logging
import os
import warnings
from pathlib import Path

import click
import numpy
import pandas
import seaborn as sea
from matplotlib import pyplot
from openff.toolkit.utils import OpenEyeToolkitWrapper
from pandas import DataFrame as DF

assert OpenEyeToolkitWrapper().is_available()

# try to suppress stereo warnings - from lily's valence-fitting
# curate-dataset.py
logging.getLogger("openff").setLevel(logging.ERROR)

# suppress divide by zero in numpy.log
warnings.filterwarnings(
    "ignore", message="divide by zero", category=RuntimeWarning
)

pandas.set_option("display.max_columns", None)


def load_bench(d: Path) -> pandas.DataFrame:
    """Load the DDE, RMSD, TFD, and ICRMSD results from the CSV files in ``d``
    and return the result as a merged dataframe"""
    dde = pandas.read_csv(d / "dde.csv")
    dde.columns = ["rec_id", "dde"]
    rmsd = pandas.read_csv(d / "rmsd.csv")
    rmsd.columns = ["rec_id", "rmsd"]
    tfd = pandas.read_csv(d / "tfd.csv")
    tfd.columns = ["rec_id", "tfd"]
    icrmsd = pandas.read_csv(d / "icrmsd.csv")
    icrmsd.columns = ["rec_id", "bonds", "angles", "dihedrals", "impropers"]
    ret = dde.merge(rmsd).pipe(DF.merge, tfd).pipe(DF.merge, icrmsd)
    print(f"loaded {ret.shape} rows for {d}")
    return ret


def load_benches(ffs, in_dirs) -> list[pandas.DataFrame]:
    """Load a sequence of dataframes, one per ``ff``. If there are multiple
    ``in_dirs``, each ``ff`` is loaded from each ``in_dir`` and stacked into a
    single dataframe."""
    ret = list()
    for ff in ffs:
        df = load_bench(Path(in_dirs[0]) / ff)
        for d in in_dirs[1:]:
            df = pandas.concat([df, load_bench(Path(d) / ff)])
        ret.append(df)
    return ret


def merge_metrics(dfs, names, metric: str):
    assert len(dfs) > 0, "must provide at least one dataframe"
    df = dfs[0][["rec_id", metric]].copy()
    df.columns = ["rec_id", names[0]]
    for i, d in enumerate(dfs[1:]):
        name = names[i + 1]
        to_add = d[["rec_id", metric]].copy()
        to_add.columns = ["rec_id", name]
        df = df.merge(to_add, on="rec_id")
    return df


def plot_ddes(dfs: list[pandas.DataFrame], names, out_dir):
    figure, axis = pyplot.subplots(figsize=(6, 4))
    ddes = merge_metrics(dfs, names, "dde")
    ax = sea.histplot(
        data=ddes.iloc[:, 1:],
        binrange=(-15, 15),
        bins=16,
        element="step",
        fill=False,
    )
    label = "DDE (kcal mol$^{-1}$)"
    ax.set_xlabel(label)
    pyplot.savefig(f"{out_dir}/dde.png", dpi=300)
    pyplot.close()


def plot_rmsds(dfs: list[pandas.DataFrame], names, out_dir):
    figure, axis = pyplot.subplots(figsize=(6, 4))
    rmsds = merge_metrics(dfs, names, "rmsd")
    ax = sea.kdeplot(data=numpy.log10(rmsds.iloc[:, 1:]))
    ax.set_xlim((-2.0, 0.7))
    ax.set_xlabel("Log RMSD")
    pyplot.savefig(f"{out_dir}/rmsd.png", dpi=300)
    pyplot.close()

    figure, axis = pyplot.subplots(figsize=(6, 4))
    ax = sea.ecdfplot(rmsds.iloc[:, 1:])
    ax.set_xlabel("RMSD (Å)")
    pyplot.savefig(f"{out_dir}/rmsd_cdf.png", dpi=300)
    pyplot.close()


def plot_tfds(dfs: list[pandas.DataFrame], names, out_dir):
    figure, axis = pyplot.subplots(figsize=(6, 4))
    tfds = merge_metrics(dfs, names, "tfd")
    ax = sea.kdeplot(data=numpy.log10(tfds.iloc[:, 1:]))
    ax.set_xlim((-4.0, 0.5))
    ax.set_xlabel("Log TFD")
    pyplot.savefig(f"{out_dir}/tfd.png", dpi=300)
    pyplot.close()

    figure, axis = pyplot.subplots(figsize=(6, 4))
    ax = sea.ecdfplot(tfds.iloc[:, 1:])
    ax.set_xlabel("TFD")
    pyplot.savefig(f"{out_dir}/tfd_cdf.png", dpi=300)
    pyplot.close()


def plot_icrmsds(dfs, names, out_dir):
    titles = {
        "bonds": "Bond Internal Coordinate RMSDs",
        "angles": "Angle Internal Coordinate RMSDs",
        "dihedrals": "Proper Torsion Internal Coordinate RMSDs",
        "impropers": "Improper Torsion Internal Coordinate RMSDs",
    }
    ylabels = {
        "bonds": "Bond error (Å)",
        "angles": "Angle error (̂°)",
        "dihedrals": "Proper Torsion error (°)",
        "impropers": "Improper Torsion error(°)",
    }
    for m in ["bonds", "angles", "dihedrals", "impropers"]:
        full = merge_metrics(dfs, names, m)
        df = full.iloc[:, 1:]
        # only take the data points within f standard deviations of the mean
        if f := os.environ.get("OFF_BENCH_F", None):
            std, mean = df.std(), df.mean()
            f = float(f)
            cond = ((df > mean - f * std) & (df < mean + f * std)).all(1)
            df = df[cond]
            filt = full[~cond]["rec_id"].to_list()
            print(f"filtered {len(filt)} {m}:")
            print(filt)

        figure, axis = pyplot.subplots(figsize=(6, 4))
        ax = sea.boxplot(df)
        pyplot.title(titles[m])
        ax.set_ylabel(ylabels[m])
        pyplot.savefig(f"{out_dir}/{m}.png", dpi=300)
        pyplot.close()


def plot(out_dir, ffs, in_dirs, names=None):
    """Plot each of the `dde`, `rmsd`, and `tfd` CSV files found in `in_dirs`
    and write the resulting PNG images to out_dir. If provided, take the plot
    legend entries from `names` instead of `in_dirs`. If `filter_records` is
    provided, restrict the plot only to those records. `negate` swaps the
    comparison to include only the records *not* in `filter_records`.

    """
    # default to directory names
    if names is None:
        names = in_dirs

    dfs = load_benches(ffs, in_dirs)

    for name, df in zip(names, dfs):
        df.to_csv(f"{out_dir}/{name}.csv")

    plot_ddes(dfs, names, out_dir)
    plot_rmsds(dfs, names, out_dir)
    plot_tfds(dfs, names, out_dir)
    plot_icrmsds(dfs, names, out_dir)


def plotter(ffs, output_dir, input_dirs, names=None, **kwargs):
    if names is None:
        names = ["Sage 2.1.0", "Sage 2.2.0", "Sage TM"]
    out_path = Path(output_dir)
    out_path.mkdir(exist_ok=True)
    plot(output_dir, ffs, input_dirs, names, **kwargs)


@click.command()
@click.argument("forcefields", nargs=-1)
@click.option("--input-dir", "-d", default=["output/industry"], multiple=True)
@click.option("--output_dir", "-o", default="/tmp")
def main(forcefields, input_dir, output_dir):
    plotter(
        forcefields,
        output_dir,
        input_dirs=input_dir,
    )


if __name__ == "__main__":
    main()

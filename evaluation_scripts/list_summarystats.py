import pandas as pd
import os
import argparse


# Quartile functions
def q25(x):
    return x.quantile(0.25)


def q75(x):
    return x.quantile(0.75)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plot summary statistics for individual variables across all visits')
    # positional arguments:
    parser.add_argument('output_dir', help='path to folder where the output files will be saved')
    parser.add_argument('data_path', help='path to data in csv format, one row per visit')
    args = parser.parse_args()
    # check whether output folder exists, if not create
    if not os.path.exists(args.output_dir):
        os.mkdir(args.output_dir)

    data = pd.read_csv(args.data_path)
    summary_stats = data.agg(['min', q25, 'median', q75, 'max', 'mean', 'var', 'std']).T

    summary_stats.to_csv(os.path.join(args.output_dir, "summarystats.csv"))

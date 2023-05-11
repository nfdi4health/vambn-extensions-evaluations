import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import argparse
import numpy as np
from preprocessing import clean_df


def get_frobenius_norm(real, virtual):
    cor_diff = real - virtual
    norm_cor_diff = np.linalg.norm(cor_diff)
    norm_real = np.linalg.norm(real)
    norm = norm_cor_diff / norm_real
    return norm_real, norm_cor_diff, norm


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plot pearson correlations for both real and synthetic data')
    # positional arguments:
    parser.add_argument('output_dir', help='path to folder where the output files will be saved')
    parser.add_argument('original_data_path', help='path to original data in csv format, one row per participant')
    parser.add_argument('synthetic_data_path', help='path to synthetic data in csv format, one row per participant')

    args = parser.parse_args()
    # check whether output folder exists, if not create
    if not os.path.exists(args.output_dir):
        os.mkdir(args.output_dir)

    original = clean_df(pd.read_csv(args.original_data_path, sep=','))
    corr_orig = original.corr(method="pearson")

    synthetic = pd.read_csv(args.synthetic_data_path, sep=',')
    synthetic = clean_df(synthetic)
    corr_syn = synthetic.corr(method="pearson")

    # ensure same heat coloration across all 3 heatmaps
    vmin = min(corr_syn.values.min(), corr_orig.values.min())
    vmax = max(corr_syn.values.max(), corr_orig.values.max())

    for corr, title, dpi in zip([corr_syn, corr_orig], ['Synthetic Data', 'Real Data'], [143.5, 143.5]):
        plt.figure()
        hm = sns.heatmap(data=corr, xticklabels=False, yticklabels=False, vmin=vmin, vmax=vmax)
        hm.set_aspect('equal', 'box')
        plt.savefig(f'{args.output_dir}/corr_mat_'+title.replace(' ', '-')+'.png', dpi=dpi, bbox_inches='tight',
                    pad_inches=0.2)
        plt.close()
    # determine frobenius norm, i.e. quantify error
    norm = get_frobenius_norm(corr_orig, corr_syn)
    print("Frobenius Norm")
    print(norm)
    print('fin')

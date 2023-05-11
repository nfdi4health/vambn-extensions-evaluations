import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plot the boolean variable m_schulab over time')
    # positional arguments:
    parser.add_argument('output_dir', help='path to folder where the output files will be saved')
    parser.add_argument('data_path', help='path to data in csv format, one row per participant')

    args = parser.parse_args()
    # check whether output folder exists, if not create
    if not os.path.exists(args.output_dir):
        os.mkdir(args.output_dir)

    # load data
    data = pd.read_csv(args.data_path)
    sample_amount = 100
    schulab_cols = [c for c in data.columns if 'm_schul' in c]
    samples = data[schulab_cols].sample(n=sample_amount)

    samples = samples.reindex(sorted(samples.columns), axis=1)
    samples.rename(columns=lambda x: x.split('_')[-1], inplace=True)
    plt.figure()
    cmap = sns.color_palette("Blues_r", 2)
    hm = sns.heatmap(data=samples, yticklabels=False, cmap=cmap, cbar=False)
    colorbar = hm.collections[0].colorbar
    hm.set_ylabel(str(sample_amount)+' random samples')
    plt.savefig(f'{args.output_dir}/schulab_mat.pdf', bbox_inches='tight')
    plt.close()

    print('fin')


import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os
import argparse


def rename_columns(df):
    df = df[df.columns.drop(list(df.filter(regex='SUBJID|scode_')))]
    df.columns = df.columns.str.replace('DONALD_', '')
    df.columns = df.columns.str.replace('TIMES_', '')
    df.columns = df.columns.str.replace('NUTRI_', '')
    df.columns = df.columns.str.replace('SOCIO_', '')
    df.columns = df.columns.str.replace('ANTHRO_', '')
    df.rename(columns={'SA_fam_ID_VIS00': 'fam_ID', 'SA_sex_VIS00': 'sex'}, inplace=True)
    return df


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compare distributions of synthetic and real data for individual '
                                                 'variables')
    # positional arguments:
    parser.add_argument('output_dir', help='path to folder where the output files will be saved')
    parser.add_argument('original_data_path', help='path to original data in csv format, one row per participant')
    parser.add_argument('synthetic_data_path', help='path to synthetic data in csv format, one row per participant')

    args = parser.parse_args()
    # check whether output folder exists, if not create
    if not os.path.exists(args.output_dir):
        os.mkdir(args.output_dir)

    # read original data
    original = pd.read_csv(args.original_data_path, sep=',')
    # original = pd.read_sas('/home/langnickel/ownCloud/Kooperation_synthetische Daten/zuckertrends_final.sas7bdat')
    original.drop(columns=['Unnamed: 0', 'SUBJID'], inplace=True)

    # read original VAMBN result
    syn_data = pd.read_csv("../original_VAMBN/donald-data-virtual-pp-fixed-converted.csv")
    syn_data = pd.read_csv(args.syn_data_path)
    syn_data = rename_columns(syn_data)

    # get discrete variables
    discvarnames = ['fam_ID', 'sex', 'wo_tage', 'ovw', 'underrep', 'm_ovw', 'm_employ', 'm_schulab']
    cols_discrete = [v for v in original.columns if any([dvn in v for dvn in discvarnames])]
    cols_continuous = [v for v in original.columns if v not in cols_discrete and "Unnamed" not in v]

    plotnames = ['Real Data', 'Synthetic Data']

    # continuous plots: histogram with kde
    for i in cols_continuous[:]:
        plt.figure()
        df = pd.DataFrame({"Real Data": original[i].dropna(),
                           "Synthetic Data": syn_data[i]
                           })
        sns.displot(data=df, kde=True)
        plt.title(f'{i}')
        plt.xlim(0, 75)
        plt.ylim(0, 85)
        plt.tight_layout()
        plt.savefig(f'{args.output_dir}/{str(i)}', bbox_inches='tight')


    # discrete plots: histograms
    for i in cols_discrete:
        print(i)
        fig, axes = plt.subplots(1,4)
        for ax, d, name, color in zip(axes, [original[i], syn_data[i]], plotnames,
                                      ['tab:blue', 'tab:orange']):
            ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
            ax.xaxis.set_ticks([])
            ax.set_xlabel(name)
            ax.barh(*np.unique(d, return_counts=True), color=color)
        plt.suptitle(i)
        plt.savefig(f'{args.output_dir}/{str(i)}', bbox_inches='tight')
        plt.close()

    print('fin')

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import os
import argparse

output_dir = "../comparison/new_plots"


# compute deviation of alter/time passed inbetween visits
def compute_error(df):
    dage = df['alter'].shift(-1) - df['alter']
    dage = dage[dage.index % 16 != 15]  # drop diff between age 18 and next child's age 3
    dtime = df['time'].shift(-1) - df['time']
    dtime = dtime[dtime.index % 16 != 15]  # drop diff between age 18 and next child's age 3
    time_err = dtime - dage
    return time_err


def summing_error(df):
    macro_sum = df['EW_p'] + df['Fett_p'] + df['KH_p']
    macro_sum_err = macro_sum - 100
    return macro_sum_err


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plot pearson correlations for both real and synthetic data')
    # positional arguments:
    parser.add_argument('output_dir', help='path to folder where the output files will be saved')
    parser.add_argument('syn_data_vambn', help='path to synthetic vambn data in csv format, one row per participant')
    parser.add_argument('syn_data_vambn_ft',
                        help='path to synthetic vambn_ft data in csv format, one row per participant')
    parser.add_argument('syn_data_vambn_mt',
                        help='path to synthetic vambn_mt data in csv format, one row per participant')

    args = parser.parse_args()
    # check whether output folder exists, if not create
    if not os.path.exists(args.output_dir):
        os.mkdir(args.output_dir)

    df_vambn = pd.read_csv(args.original_data_path)
    df_vambn_ft = pd.read_csv(args.syn_data_vambn_ft)
    df_vambn_mt = pd.read_csv(args.syn_data_vambn_mt)

    df_vambn_error = compute_error(df_vambn)
    df_vambn_ft_error = compute_error(df_vambn_ft)
    df_vambn_mt_error = compute_error(df_vambn_mt)

    for error, name in zip([df_vambn_error, df_vambn_ft_error, df_vambn_mt_error],
                           ["VAMBN", "VAMBN-FT", "VAMBN-MT"]):
        print(f'mean/median absolute time-error {name}:', error.abs().mean(), '/', error.abs().median())

    use_logscale = False
    logticks = [-50, -20, -10, -5, -2, -1, 0, 1, 2, 5, 10, 20, 50]

    # plot line
    fig, ax = plt.subplots()
    ax = sns.kdeplot(data=df_vambn_error, label='VAMBN', ax=ax)
    ax = sns.kdeplot(data=df_vambn_ft_error, label='VAMBN-FT', ax=ax)
    ax = sns.kdeplot(data=df_vambn_mt_error, label='VAMBN-MT', ax=ax)
    ax.set_xlabel('Δ$\it{time}$ - Δ$\it{alter}$, in years')
    ax.set_ylabel('Density')
    if use_logscale:
        ax.set_xscale('symlog')
        ax.set_xticks(logticks)
        ax.get_xaxis().set_major_formatter(ticker.ScalarFormatter())
    plt.legend()
    plt.xlim(-75, 75)
    plt.savefig(f'{args.output_dir}/time-error.pdf', bbox_inches='tight')

    # 100% SUMMING ERROR
    df_vambn_error_sum = compute_error(df_vambn)
    df_vambn_ft_error_sum = compute_error(df_vambn_ft)
    df_vambn_mt_error_sum = compute_error(df_vambn_mt)

    for error, name in zip([df_vambn_error_sum, df_vambn_ft_error_sum,
                            df_vambn_mt_error_sum],
                           ["VAMBN", "VAMBN-FT", "VAMBN-MT"]):
        print(f'mean/median absolute sum-error {name}:', error.abs().mean(), '/', error.abs().median())

    use_logscale = False
    # plot line
    fig, ax = plt.subplots()
    ax = sns.kdeplot(data=df_vambn_error_sum, label='VAMBN', ax=ax)
    ax = sns.kdeplot(data=df_vambn_ft_error_sum, label='VAMBN-FT', ax=ax)
    ax = sns.kdeplot(data=df_vambn_mt_error_sum, label='VAMBN-MT', ax=ax)

    ax.set_xlabel('(EW_p+Fett_p+KH_p) - 100')
    ax.set_ylabel('Density')
    # ax.set_title('Capability of summing to 100%')
    if use_logscale:
        ax.set_xscale('symlog')
        ax.set_xticks(logticks)
        ax.get_xaxis().set_major_formatter(ticker.ScalarFormatter())
    plt.legend()
    plt.savefig(f'{args.output_dir}/100-error.pdf', bbox_inches='tight')
    plt.show()

print('fin')

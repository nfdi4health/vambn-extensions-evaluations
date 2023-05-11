import numpy as np
import scipy.spatial
import argparse
import pandas as pd
from preprocessing import clean_df


def get_jsd(real, virtual):
    # load datasets & remove id column
    jsd_d = {}
    for col in real:
        real_wo_missing = real[col].dropna()  # delete empty cells
        # binning
        if np.sum(real_wo_missing.values) % 1 == 0 and np.sum(virtual[col].values) % 1 == 0:
            # categorical column
            real_binned = np.bincount(real_wo_missing)
            virtual_binned = np.bincount(virtual[col])
        else:
            # get optimal amount of bins
            n_bins = np.histogram_bin_edges(real_wo_missing, bins='auto')
            real_binned = np.bincount(np.digitize(real_wo_missing, n_bins))
            virtual_binned = np.bincount(np.digitize(virtual[col], n_bins))
        # one array might be shorter here than the other, e.g. if real patients contain the categorical
        # encoding 0-3, but virtual patients only contain 0-2
        # in this case -> fill missing bin with zero
        if len(real_binned) != len(virtual_binned):
            padding_size = np.abs(len(real_binned) - len(virtual_binned))
            if len(real_binned) > len(virtual_binned):
                virtual_binned = np.pad(virtual_binned, (0, padding_size))
            else:
                real_binned = np.pad(real_binned, (0, padding_size))
        # compute jsd
        jsd = scipy.spatial.distance.jensenshannon(real_binned, virtual_binned)
        jsd_d[col] = jsd
    return jsd_d


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculate JS-divergence')
    # positional arguments:
    parser.add_argument('original_data_path', help='path to original data in csv format, one row per participant')
    parser.add_argument('synthetic_data_path', help='path to synthetic data in csv format, one row per participant')
    args = parser.parse_args()

    original = clean_df(pd.read_csv(args.original_data_path, sep=','))
    synthetic = clean_df(pd.read_csv(args.synthetic_data_path, sep=','))
    synthetic.columns = [col[col.find("_")+1:] for col in synthetic.columns]
    synthetic.rename(columns={"sex_VIS00": "sex", "fam_ID_VIS00": "fam_ID"}, inplace=True)
    assert list(synthetic.columns) == list(original.columns)

    js = get_jsd(original, synthetic)
    js_all = [js[key] for key in js.keys()]
    print("JS-Divergence per variable")
    print(js)
    print("Averaged JS-Divergence with std")
    print(np.average(js_all), np.std(js_all))

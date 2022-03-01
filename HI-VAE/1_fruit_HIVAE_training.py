
import re
import os
import numpy as np
import csv
import pandas as pd
from pandas.plotting import scatter_matrix
from matplotlib import pyplot as plt
from IPython.display import Audio

import helpers  # this is where the main training/decoding functions are, modified from teh original HIVAE main.py


# import warnings
# warnings.filterwarnings('ignore') ########## NOTE: comment out for testing in case it's hiding problems

def set_settings(opts, nepochs=500, modload=False,
                 save=True):  # note: modload doesnt do anything right now, hardcoded in helpers.py
    'replace setting template placeholders with file info'
    inputf = re.sub('.csv', '', opts['files'].iloc[0])
    missf = inputf + '_missing.csv'
    typef = inputf + '_types.csv'

    template = '--epochs NEPOCHS --model_name model_HIVAE_inputDropout --restore MODLOAD \
        --data_file data_python/INPUT_FILE.csv --types_file data_python/TYPES_FILE \
         --batch_size NBATCH --save NEPFILL --save_file SAVE_FILE\
        --dim_latent_s SDIM --dim_latent_z 1 --dim_latent_y YDIM \
        --miss_percentage_train 0 --miss_percentage_test 0 \
        --true_miss_file data_python/MISS_FILE --learning_rate LRATE'

    # replace placeholders in template
    settings = re.sub('INPUT_FILE', inputf, template)
    settings = re.sub('NBATCH', str(opts['nbatch'].iloc[0]), settings)
    settings = re.sub('NEPOCHS', str(nepochs), settings)
    settings = re.sub('NEPFILL', str(nepochs - 1), settings) if save else re.sub('NEPFILL', str(nepochs * 2), settings)
    settings = re.sub('YDIM', str(opts['ydims'].iloc[0]), settings)
    settings = re.sub('SDIM', str(opts['sdims'].iloc[0]), settings)
    settings = re.sub('MISS_FILE', missf, settings) if not 'medhist' in inputf else re.sub(
        '--true_miss_file data_python/MISS_FILE', '', settings)
    settings = re.sub('TYPES_FILE', typef, settings)
    settings = re.sub('SAVE_FILE', inputf, settings)
    settings = re.sub('LRATE', str(opts['lrates'].iloc[0]), settings)
    settings = re.sub('MODLOAD', '1', settings) if modload else re.sub('MODLOAD', '0', settings)
    return settings


sample_size = 8 #362
# get file list
files = [i for i in os.listdir('data_python/') if not '_type' in i and not '_missing' in i]
# sds = [1]*6
# sdims = dict(zip(files, sds))
best_hyper = pd.read_csv('fruit-results.csv')

# JS: read column types from fruit-data_types.csv and create _types files in data-python/ for every vargroup
types_dict = {}
with open('fruit-data_types.csv') as datafile:
    for entry in csv.DictReader(datafile, skipinitialspace=True):
        types_dict[entry['col']] = {k: v for k, v in entry.items() if not k == 'col'}
for cf in [i for i in os.listdir('python_names/') if '_cols' in i]:
    with open('python_names/'+cf) as colfile, open('data_python/'+cf.replace('_cols', '_types'), 'w') as typefile:
        writer = csv.DictWriter(typefile, fieldnames=['type', 'dim', 'nclass'])
        writer.writeheader()
        for row in csv.DictReader(colfile, skipinitialspace=True):
            writer.writerow(types_dict[row['x']])

for f in files:
    opts = dict(best_hyper[best_hyper['files'].copy() == f])
    settings = set_settings(opts, nepochs=60, modload=False, save=True)
    helpers.train_network(settings)
wave = np.sin(2*np.pi*400*np.arange(10000*2)/10000)
Audio(wave, rate=10000, autoplay=True)


#### get embeddings

dat = list()
dfs = list()
for f in files:
    # replace placeholders in template
    opts = dict(best_hyper[best_hyper['files'].copy() == f])
    opts['nbatch'].iloc[0] = sample_size
    settings = set_settings(opts, nepochs=1, modload=True, save=False)

    # run
    encs, encz, d = helpers.enc_network(settings)

    # make deterministic embeddings
    subj = pd.read_csv('python_names/' + re.sub('.csv', '', f) + '_subj.csv')['x']
    sc = pd.DataFrame({'scode_' + re.sub('.csv', '', f): pd.Series(np.array([i for i in encs])), 'SUBJID': subj})
    zc = pd.DataFrame({'zcode_' + re.sub('.csv', '', f): pd.Series(np.array([i[0] for i in encz])), 'SUBJID': subj})
    enc = pd.merge(sc, zc, on='SUBJID')

    # save out individual file's metadata
    enc.to_csv('Saved_Networks/' + re.sub('.csv', '', f) + '_meta.csv', index=False)
    dfs.append(enc)
    dat.append(d)

# join metadata
enc_vars = [pd.read_csv('Saved_Networks/' + re.sub('.csv', '', f) + '_meta.csv') for f in files]
meta = helpers.merge_dat(enc_vars)
meta[meta.columns[['Unnamed' not in i for i in meta.columns]]].to_csv('metaenc.csv', index=False)

dat_dic = dict(zip(files, dat))

# Plotting embedding distributions
fig = scatter_matrix(
    meta[meta.columns.drop(list(meta.filter(regex='SUBJID|scode_')))],
    figsize=[15, 15],
    marker=".",
    s=10,
    diagonal="kde"
)
for ax in fig.ravel():
    ax.set_xlabel(re.sub('_VIS|zcode_', '', ax.get_xlabel()), fontsize=20, rotation=90)
    ax.set_ylabel(re.sub('_VIS|zcode_', '', ax.get_ylabel()), fontsize=20, rotation=90)

plt.suptitle('HI-VAE embeddings (deterministic)', fontsize=20)


#### Reconstructed data

meta = pd.read_csv('metaenc.csv')

recon = list()
recdfs = list()
for f in files:
    # replace placeholders in template
    opts = dict(best_hyper[best_hyper['files'].copy() == f])
    opts['nbatch'].iloc[0] = sample_size
    settings = set_settings(opts, nepochs=1, modload=True, save=False)

    # run
    zcodes = meta['zcode_' + re.sub('.csv', '', f)]
    scodes = meta['scode_' + re.sub('.csv', '', f)]
    rec = helpers.dec_network(settings, zcodes, scodes)
    recon.append(rec)

    subj = pd.read_csv('python_names/' + re.sub('.csv', '', f) + '_subj.csv')['x']
    names = pd.read_csv('python_names/' + re.sub('.csv', '', f) + '_cols.csv')['x']
    recd = pd.DataFrame(rec)
    recd.columns = names
    recd['SUBJID'] = subj
    recdfs.append(recd)

recon_dic = dict(zip(files, recon))

data_recon = helpers.merge_dat(recdfs)
data_recon.to_csv('reconRP.csv', index=False)


# Get Loglikelihoods!
meta = pd.read_csv('metaenc.csv')

dfs = list()
for f in files:
    # replace placeholders in template
    opts = dict(best_hyper[best_hyper['files'].copy() == f])
    opts['nbatch'].iloc[0] = sample_size
    settings = set_settings(opts, nepochs=1, modload=True, save=False)

    # run
    zcodes = meta['zcode_' + re.sub('.csv', '', f)]
    scodes = meta['scode_' + re.sub('.csv', '', f)]

    loglik = helpers.dec_network_loglik(settings, zcodes, scodes)
    loglik = np.nanmean(np.array(loglik).T, axis=1)
    subj = pd.read_csv('python_names/' + re.sub('.csv', '', f) + '_subj.csv')['x']
    dat = pd.DataFrame(loglik)
    dat.columns = [f]
    dat['SUBJID'] = subj
    dfs.append(dat)

decoded = helpers.merge_dat(dfs)
decoded.to_csv('training_logliks.csv', index=False)

plt.show()

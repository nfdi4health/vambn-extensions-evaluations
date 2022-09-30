from matplotlib import pyplot as plt
import os
import re
import pandas as pd
import numpy as np
import seaborn as sns

import helpers  # this is where the main training/decoding functions are, modified from the original HIVAE main.py

# import warnings
# warnings.filterwarnings('ignore') ########## NOTE: comment out for testing in case it's hiding problems

def set_settings(opts, nepochs=500, modload=False,
                 save=True):  # note: modload doesnt do anything right now, hardcoded in helpers.py
    'replace setting template placeholders with file info'
    inputf = opts['vargroups'].iloc[0]+'_VIS00'
    missf = inputf + '_missing.csv'
    typef = inputf + '_types.csv'

    template = '--epochs NEPOCHS --model_name model_HIVAE_inputDropout --restore MODLOAD \
        --data_file data_python/INPUT_FILE.csv --types_file data_python/TYPES_FILE \
         --batch_size NBATCH --save NEPFILL --save_file SAVE_FILE\
        --dim_latent_s SDIM --dim_latent_z 1 --dim_latent_y YDIM \
        --miss_percentage_train 0 --miss_percentage_test 0 \
        --true_miss_file data_python/MISS_FILE --learning_rate LRATE --n_vis N_VIS'

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
    settings = re.sub('N_VIS', str(opts['nvis'].iloc[0]), settings)
    return settings

#### General settings

sample_size = 1274
# get file list
files = [i for i in os.listdir('data_python/') if not '_type' in i and not '_missing' in i]
vargroups = set([i.split('_')[0] for i in files])
sds = [1]*6
sdims = dict(zip(files, sds))
best_hyper = pd.read_csv('donald-results.csv')
if any(vargroups != best_hyper['vargroups']):
    print('ERROR!!')
else:
    best_hyper['sdims'] = sds

#### VP decoding (run after bnet.R)
## + Get Loglikelihoods for R plot!

VPcodes = pd.read_csv('../data/data_out/main_VirtualPPts.csv')
SA_cols = [c for c in VPcodes.columns if 'SA_' in c]
dat_SA = VPcodes[SA_cols]

subj_SA = pd.read_csv('python_names/stalone_VIS00_subj.csv')['x']
dat_SA['SUBJID'] = subj_SA

dfs_dec = list()
dfs_dec.append(dat_SA)

dfs_loglik = list()
virt = list()
for x, vg in enumerate(vargroups):
    print(x+1, '/', len(vargroups), 'decoding vargroup ',vg)
    # replace placeholders in template
    opts = dict(best_hyper[best_hyper['vargroups'].copy() == vg])
    opts['nbatch'].iloc[0] = sample_size
    settings = set_settings(opts, nepochs=1, modload=True, save=False)

    # run
    zcodes = VPcodes['zcode_' + vg]
    scodes = VPcodes['scode_' + vg] if 'scode_' + vg in VPcodes.columns else np.zeros(zcodes.shape)

    dec = helpers.dec_network(settings, zcodes, scodes, VP=True)

    for vis in range(dec.shape[1]):
        dec_vis = dec[:,vis,:]
        virt.append(dec_vis)

        subj = pd.read_csv('python_names/' + vg + '_VIS' + str(vis).zfill(2) + '_subj.csv')['x']
        names = pd.read_csv('python_names/' + vg + '_VIS'+ str(vis).zfill(2) + '_cols.csv')['x']

        dat_dec = pd.DataFrame(dec_vis)
        dat_dec.columns = names
        dat_dec['SUBJID'] = subj
        dfs_dec.append(dat_dec)

    loglik_list = helpers.dec_network_loglik(settings, zcodes, scodes, VP=True)

    for vis, loglik_vis in enumerate(loglik_list):
        loglik_vis = np.nanmean(np.array(loglik_vis).T, axis=1)
        subj = pd.read_csv('python_names/' + vg + '_VIS' + str(vis).zfill(2) + '_subj.csv')['x']
        dat_loglik = pd.DataFrame(loglik_vis)
        dat_loglik.columns = [vg + '_VIS' + str(vis).zfill(2)]
        dat_loglik['SUBJID'] = subj
        dfs_loglik.append(dat_loglik)

virt_dic = dict(zip(files, virt))
decoded_dec = helpers.merge_dat(dfs_dec)
decoded_dec.to_csv('decodedVP.csv', index=False)
decoded_loglik = helpers.merge_dat(dfs_loglik)
decoded_loglik.to_csv('virtual_logliks.csv', index=False)

#### Counterfactuals (counteractuals_bnlearn.R before running this!)

# f = 'UPDRS_VIS00.csv'
# VPcodes = pd.read_csv('../../data/data_out/counter_updrs_age.csv')
# # replace placeholders in template
# opts = dict(best_hyper[best_hyper['files'].copy() == f])
# opts['nbatch'].iloc[0] = sample_size
# settings = set_settings(opts, nepochs=1, modload=True, save=False)
#
# # run
# zcodes = VPcodes['dv']
# scodes = np.zeros(zcodes.shape)
#
# decs = list()
# n = 362
# for i in range(int(len(VPcodes['dv']) / n)):
#     dec = helpers.dec_network(settings, zcodes[i * n:(i * n + n)], scodes[i * n:(i * n + n)], VP='nomiss');
#     decs.append(dec)
#
#
# names = pd.read_csv('python_names/UPDRS_VIS00_cols.csv')['x']
# allPT = pd.DataFrame(np.vstack(decs))
# allPT.columns = names
# allPT['Intervention'] = VPcodes['level']
# dfm = allPT.melt(var_name='columns', id_vars='Intervention')
# g = sns.FacetGrid(dfm, col='columns', hue='Intervention', col_wrap=3, sharex=False, sharey=False)
# g = (g.map(sns.distplot, 'value')).add_legend()
# allPT.to_csv('CF_output.csv', index=False)
#
#
# group = ['No intervention', 'Age -20yrs', 'Age +20yrs']
#
# for group in group:
#     subset = allPT[allPT['Intervention'] == group]
#     sns.distplot(subset['UPDRS_UPDRS_VIS00'], hist=True, kde=True, label=group)
#
# plt.legend(title='Intervention')
# plt.xlabel('UPDRS total')
# plt.ylabel('Density')

print('fin')

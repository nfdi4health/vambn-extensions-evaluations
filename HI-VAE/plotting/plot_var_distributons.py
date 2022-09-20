import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


#### Plots distributions of all variables for:
#       the original dataset
#       decodings of the embedded original participants (RP)
#       decodings of virtual embeddings from the BNet (VP)

original=pd.read_csv('../../data/donald-data.csv', sep = ',')
original.drop(columns=['Unnamed: 0', 'SUBJID'],inplace=True)

recRP=pd.read_csv('../reconRP.csv', sep =',')
recRP = recRP[recRP.columns.drop(list(recRP.filter(regex='SUBJID|scode_')))]
recRP.columns = recRP.columns.str.replace('TIMES_', '')
recRP.columns = recRP.columns.str.replace('NUTRI_', '')
recRP.columns = recRP.columns.str.replace('SOCIO_', '')
recRP.columns = recRP.columns.str.replace('ANTHRO_', '')

decVP = pd.read_csv('../decodedVP.csv', sep =',')
decVP = decVP[decVP.columns.drop(list(decVP.filter(regex='SUBJID|scode_')))]
decVP.columns = decVP.columns.str.replace('TIMES_', '')
decVP.columns = decVP.columns.str.replace('NUTRI_', '')
decVP.columns = decVP.columns.str.replace('SOCIO_', '')
decVP.columns = decVP.columns.str.replace('ANTHRO_', '')
decVP.rename(columns={'SA_fam_ID_VIS00': 'fam_ID', 'SA_sex_VIS00': 'sex'}, inplace=True)

discvarnames = ['fam_ID','sex','wo_tage','ovw','underrep','m_ovw','m_employ','m_schulab']
cols_discrete = [v for v in recRP.columns if any([dvn in v for dvn in discvarnames])] #use recRP cols here, because it should be same as decVP, and orig may have more
cols_continuous = [v for v in recRP.columns if not v in cols_discrete]

plotnames = ['original','reconstructed real','reconstructed virtual']

# continuous: violinplot
for i in cols_continuous:
    plt.figure()
    vp = sns.violinplot(data=[original[i], recRP[i], decVP[i]])
    vp.set_xticklabels(plotnames)
    vp.set_title(f'{i}')
    plt.savefig('plots/real-vs-dec_'+str(i), bbox_inches='tight')
    plt.close()

# discrete: histograms
for i in cols_discrete:
    fig, axes = plt.subplots(1,3)
    for ax, d, name, color in zip(axes, [original[i], recRP[i], decVP[i]], plotnames, ['tab:blue', 'tab:orange', 'tab:green']):
        ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        ax.xaxis.set_ticks([])
        ax.set_xlabel(name)
        ax.barh(*np.unique(d, return_counts=True), color=color)
    plt.suptitle(i)
    plt.savefig('plots/real-vs-dec_'+str(i), bbox_inches='tight')
    plt.close()

#SA: histograms. not available for recRP!
for i in ['fam_ID','sex']:
    fig, axes = plt.subplots(1,2)
    for ax, d, name, color in zip(axes, [original[i], decVP[i]], ['original','reconstructed virtual'], ['tab:blue', 'tab:green']):
        ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        ax.xaxis.set_ticks([])
        ax.set_xlabel(name)
        ax.barh(*np.unique(d, return_counts=True), color=color)
    plt.suptitle(i)
    plt.savefig('plots/real-vs-dec_'+str(i), bbox_inches='tight')
    plt.close()


# ######## ENTROPY (experimental):
# decVP_LSTM = pd.read_csv('../decodedVP-LSTM.csv', sep =',')
# decVP_LSTM = decVP_LSTM[decVP_LSTM.columns.drop(list(decVP_LSTM.filter(regex='SUBJID|scode_')))]
# decVP_LSTM.columns = decVP_LSTM.columns.str.replace('TIMES_', '')
# decVP_LSTM.columns = decVP_LSTM.columns.str.replace('NUTRI_', '')
# decVP_LSTM.columns = decVP_LSTM.columns.str.replace('SOCIO_', '')
# decVP_LSTM.columns = decVP_LSTM.columns.str.replace('ANTHRO_', '')
# decVP_LSTM.rename(columns={'SA_fam_ID_VIS00': 'fam_ID', 'SA_sex_VIS00': 'sex'}, inplace=True)
#
# p_vals = []
# for var in cols_continuous:
#     sampleO = original[var].dropna()
#     sampleV = decVP[var].dropna()
#     sampleL = decVP_LSTM[var].dropna()
#
#     pOV = stats.ks_2samp(sampleO, sampleV).pvalue
#     pOL = stats.ks_2samp(sampleO, sampleL).pvalue
    # print('ks_2',var,'VAMBN:',pOV)
    # print('ks_2',var,'LSTM:',pOL)
#
#     p_vals.append({'variable':var,'VAMBN':pOV,'LSTM':pOL})
# p_df = pd.DataFrame(p_vals)

print('fin')

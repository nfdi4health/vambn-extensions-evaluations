import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


#### USE LOCAL PYTHON
wd = '/path/to/output/files/'

#load data
dfL = pd.read_csv(wd + 'LSTM/results/decodedVP.csv')
dfV = pd.read_csv(wd + 'origin/results/decodedVP.csv')

s=100
schulab_cols = [c for c in dfV.columns if 'm_schul' in c]
sampleL = dfL[schulab_cols].sample(n=s)
sampleV = dfV[schulab_cols].sample(n=s)

n = 2
for samples,title in zip([sampleV, sampleL], ['original VAMBN','LSTM extension']):
    samples = samples.reindex(sorted(samples.columns), axis=1)
    samples.rename(columns=lambda x: x.split('_')[-1], inplace=True)
    plt.figure()
    cmap = sns.color_palette("Blues_r", n)
    hm = sns.heatmap(data=samples, yticklabels = False, cmap=cmap)#, vmin=vmin, vmax=vmax)
    colorbar = hm.collections[0].colorbar
    r = colorbar.vmax - colorbar.vmin
    colorbar.set_ticks([colorbar.vmin + r / n * (0.5 + i) for i in range(n)])
    colorbar.set_ticklabels(list([False,True]))
    hm.set_title('m_schulab '+title)
    hm.set_ylabel(str(s)+' random samples')
    # hm.set_aspect('equal','box')
    # plt.savefig('plots/corr_mat_'+title.replace(' ', '-')+'.png', dpi=dpi, bbox_inches='tight') #input magic dpi numbers that make each corr-mat entry be juuuust over 1px in size
    plt.savefig('plots/schulab_mat_'+title.replace(' ', '-')+'.pdf', bbox_inches='tight') #dpi irrelevant for PDF, but it becomes huge file :(
    plt.show()
    plt.close()

print('fin')


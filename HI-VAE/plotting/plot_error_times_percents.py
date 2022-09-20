import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns


#### USE LOCAL PYTHON
wd = '/path/to/output/files/'

#load data as reformatted by donald_writer.py
dfL = pd.read_csv(wd + 'LSTM/results/decodedVP-studyformat.csv')
dfV = pd.read_csv(wd + 'origin/results/decodedVP-studyformat.csv')


####### PASSING TIME ERROR
#compute deviation of alter/time passed inbetween visits
dageL = dfL['alter'].shift(-1) - dfL['alter']
dageL = dageL[dageL.index % 16 != 15] #drop diff between age 18 and next child's age 3
dtimeL = dfL['time'].shift(-1) - dfL['time']
dtimeL = dtimeL[dtimeL.index % 16 != 15] #drop diff between age 18 and next child's age 3
time_errL = dtimeL - dageL

dageV = dfV['alter'].shift(-1) - dfV['alter']
dageV = dageV[dageV.index % 16 != 15] #drop diff between age 18 and next child's age 3
dtimeV = dfV['time'].shift(-1) - dfV['time']
dtimeV = dtimeV[dtimeV.index % 16 != 15] #drop diff between age 18 and next child's age 3
time_errV = dtimeV - dageV

print('mean/median absolute time-error VAMBN:', time_errV.abs().mean(), '/', time_errV.abs().median())
print('mean/median absolute time-error LSTMext:', time_errL.abs().mean(), '/', time_errL.abs().median())

use_logscale = True
logticks = [-50, -20, -10, -5, -2, -1, 0, 1, 2, 5, 10, 20, 50]

#plot line
fig, ax = plt.subplots()
ax = sns.kdeplot(data=time_errV, label='Original error', ax=ax)
ax = sns.kdeplot(data=time_errL, label='LSTM error', ax=ax)
ax.set_xlabel('Δ$\it{time}$ - Δ$\it{alter}$, in years')
ax.set_ylabel('Density')
# ax.set_title('Improvement in realistically passing time')
if use_logscale:
    ax.set_xscale('symlog')
    ax.set_xticks(logticks)
    ax.get_xaxis().set_major_formatter(ticker.ScalarFormatter())
plt.savefig('plots/time-error.pdf', bbox_inches='tight')
plt.show()

# #plot violin
# plt.figure()
# vp = sns.violinplot(data=[time_errV, time_errL])
# vp.set_xticklabels(['Original error', 'LSTM error'])
# # vp.set_title('Improvement in realistically passing time')
# if use_logscale:
#     vp.set_yscale('symlog')
#     vp.set_yticks(logticks)
#     vp.get_yaxis().set_major_formatter(ticker.ScalarFormatter())
# # plt.savefig('plots/time-error.pdf', bbox_inches='tight')
# plt.show()


####### 100% SUMMING ERROR
macro_sumV = dfV['EW_p'] + dfV['Fett_p'] + dfV['KH_p']
macro_sum_errV = macro_sumV - 100
macro_sumL = dfL['EW_p'] + dfL['Fett_p'] + dfL['KH_p']
macro_sum_errL = macro_sumL - 100

print('mean/median absolute 100%-error VAMBN:', macro_sum_errV.abs().mean(), '/', macro_sum_errV.abs().median())
print('mean/median absolute 100%-error LSTMext:', macro_sum_errL.abs().mean(), '/', macro_sum_errL.abs().median())

use_logscale = False
#plot line
fig, ax = plt.subplots()
ax = sns.kdeplot(data=macro_sumV, label='Original EW+Fett+KH sum', ax=ax)
ax = sns.kdeplot(data=macro_sumL, label='LSTM EW+Fett+KH sum', ax=ax)
ax.set_xlabel('EW_p + Fett_p + KH_p')
ax.set_ylabel('Density')
# ax.set_title('Capability of summing to 100%')
if use_logscale:
    ax.set_xscale('symlog')
    ax.set_xticks(logticks)
    ax.get_xaxis().set_major_formatter(ticker.ScalarFormatter())
plt.savefig('plots/100-error.pdf', bbox_inches='tight')
plt.show()


###### for original data, for reference. run on VM
# dfO = pd.read_sas('path/to/donald/data.sas7bdat')
# dageO = dfO['alter'].shift(-1) - dfO['alter']
# dageO = dageO[dageO.index % 16 != 15] #drop diff between age 18 and next child's age 3
# dtimeO = dfO['time'].shift(-1) - dfO['time']
# dtimeO = dtimeO[dtimeO.index % 16 != 15] #drop diff between age 18 and next child's age 3
# time_errO = dtimeO - dageO
# macro_sumO = dfO['EW_p'] + dfO['Fett_p'] + dfO['KH_p']
# macro_sum_errO = macro_sumO - 100
#
# sacc_sumO = dfO['MSacch_p'] + dfO['DISACCH_p']
# sacc_err = dfO['ZUCK_p'] - sacc_sumO
# errmin = min(sacc_err)
# errmax = max(sacc_err)

print('fin')

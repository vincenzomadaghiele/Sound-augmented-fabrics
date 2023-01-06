import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy import stats

# open test results file
df = pd.read_csv('data.csv', index_col=False)
df = df.set_index('participant')

# remove test columns
df = df[df['prolific_ID:1'] != 'nan']
df = df[df['prolific_ID:1'] != 'prova']
df = df[df['prolific_ID:1'] != 'PROVA']
df = df[df['prolific_ID:1'] != 'test']
df = df[df['prolific_ID:1'] != 's,dqwl.']
df = df[df['prolific_ID:1'].notna()]

# remove hearing impaired participants
df = df[df['prolific_ID:1'] != '5f9a0f1dba641d12282c8e41']
df = df[df['prolific_ID:1'] != '607176a53e0b57a4f8be7ac9']
df = df[df['prolific_ID:1'] != '5f458cb79f9aa31a7d7ab81b']
df = df[df['prolific_ID:1'] != '61043a26578a40077e1ade55']


#%% Remove outliers

# get cheater's ID (too fast test)
cheaters =  np.array(df[df['TIME_total'] <= 3]['prolific_ID:1'])
# remove cheaters
df =  df[df['TIME_total'] > 3]

# z-score test
cat_cols = ['prolific_ID:1', 'age:1', 'gender:1', 'gender2:1',
            'previous_knowledge:1', 'comments:1','PROLIFIC_PID', 
            'STUDY_ID', 'SESSION_ID', 'TIME_start', 'TIME_end', 'TIME_total']

only_numerical = df.drop(columns=cat_cols)
ID_before = np.array(df['prolific_ID:1'])
df = df[(np.abs(stats.zscore(only_numerical)) < 3).all(axis=1)]
ID_after = np.array(df['prolific_ID:1'])
cheaters = np.append(cheaters, ID_before[~np.isin(ID_before,ID_after)])


#%% DEMOGRAPHICS

dem_cols = ['age:1', 'gender:1', 'previous_knowledge:1']
dem = df.copy()[dem_cols]
age_stats = dem['age:1'].value_counts()
gender_stats = dem['gender:1'].value_counts()
knowledge_stats = dem['previous_knowledge:1'].value_counts()


#%% GRN synth

GRN_cols = ['GRN_01_01:1', 'GRN_01_02:1', 'GRN_01_03:1', 
               'GRN_02_01:1', 'GRN_02_02:1', 'GRN_02_03:1',
               'GRN_03_01:1', 'GRN_03_02:1', 'GRN_03_03:1', 
               'GRN_04_01:1', 'GRN_04_02:1', 'GRN_04_03:1', 
               'GRN_05_01:1', 'GRN_05_02:1', 'GRN_05_03:1']

GRN = df.copy()[GRN_cols]
GRN_mean = GRN.mean()
GRN_err = GRN.std()

GRN_cols4plot = ['GRN_01_01', 'GRN_01_02', 'GRN_01_03', 
               'GRN_02_01', 'GRN_02_02', 'GRN_02_03',
               'GRN_03_01', 'GRN_03_02', 'GRN_03_03', 
               'GRN_04_01', 'GRN_04_02', 'GRN_04_03', 
               'GRN_05_01', 'GRN_05_02', 'GRN_05_03']

plt.grid(axis='x', zorder=0)
plt.errorbar(GRN_mean, GRN_cols4plot, xerr=GRN_err, fmt='o', 
             #ecolor='tab:orange', color='tab:orange', 
             capsize=3, zorder=3)
plt.xlabel('Sound warmth')
plt.title('Granular synthesizer: rating of sonic stimuli from "cold" to "warm"')
plt.xlim([0, 100])
plt.show()

GRN.boxplot(vert=False)
plt.xlabel('Sound warmth')
plt.title('Granular synthesizer: rating of sonic stimuli from "cold" to "warm"')
plt.xlim([0, 100])
plt.show()


#%% GRN aggregate rows

GRN['GRN_01'] = (GRN['GRN_01_01:1'] + GRN['GRN_01_02:1'] + GRN['GRN_01_03:1']) / 3
GRN['GRN_02'] = (GRN['GRN_02_01:1'] + GRN['GRN_02_02:1'] + GRN['GRN_02_03:1']) / 3
GRN['GRN_03'] = (GRN['GRN_03_01:1'] + GRN['GRN_03_02:1'] + GRN['GRN_03_03:1']) / 3
GRN['GRN_04'] = (GRN['GRN_04_01:1'] + GRN['GRN_04_02:1'] + GRN['GRN_04_03:1']) / 3
GRN['GRN_05'] = (GRN['GRN_05_01:1'] + GRN['GRN_05_02:1'] + GRN['GRN_05_03:1']) / 3

agg_cols = ['GRN_01', 'GRN_02', 'GRN_03', 'GRN_04', 'GRN_05']
GRN_agg = GRN.copy()[agg_cols]

#GRN_agg.boxplot(vert=False)
plt.grid(axis='x', zorder=0)
sns.boxplot(data=GRN_agg[GRN_agg.columns[::-1]], palette="coolwarm", orient='h')
plt.xlabel('Sound warmth')
plt.title('Granular synthesizer: rating of sonic stimuli from "cold" to "warm"')
plt.xlim([0, 100])
plt.show()


#%% ADD synth

ADD_cols = ['ADD_01_01:1', 'ADD_01_02:1', 'ADD_01_03:1', 
               'ADD_02_01:1', 'ADD_02_02:1', 'ADD_02_03:1',
               'ADD_03_01:1', 'ADD_03_02:1', 'ADD_03_03:1', 
               'ADD_04_01:1', 'ADD_04_02:1', 'ADD_04_03:1', 
               'ADD_05_01:1', 'ADD_05_02:1', 'ADD_05_03:1']

ADD = df.copy()[ADD_cols]
ADD_mean = ADD.mean()
ADD_err = ADD.std()

ADD_cols4plot = ['ADD_01_01', 'ADD_01_02', 'ADD_01_03', 
               'ADD_02_01', 'ADD_02_02', 'ADD_02_03',
               'ADD_03_01', 'ADD_03_02', 'ADD_03_03', 
               'ADD_04_01', 'ADD_04_02', 'ADD_04_03', 
               'ADD_05_01', 'ADD_05_02', 'ADD_05_03']

plt.grid(axis='x', zorder=0)
plt.errorbar(ADD_mean, ADD_cols4plot, xerr=ADD_err, fmt='o', capsize=3, zorder=3)
plt.xlabel('Sound warmth')
plt.title('Additive synthesizer: rating of sonic stimuli from "cold" to "warm"')
plt.xlim([0, 100])
plt.show()

ADD.boxplot(vert=False)
plt.xlabel('Sound warmth')
plt.title('Additive synthesizer: rating of sonic stimuli from "cold" to "warm"')
plt.xlim([0, 100])
plt.show()


#%% ADD aggregate rows

ADD['ADD_01'] = (ADD['ADD_01_01:1'] + ADD['ADD_01_02:1'] + ADD['ADD_01_03:1']) / 3
ADD['ADD_02'] = (ADD['ADD_02_01:1'] + ADD['ADD_02_02:1'] + ADD['ADD_02_03:1']) / 3
ADD['ADD_03'] = (ADD['ADD_03_01:1'] + ADD['ADD_03_02:1'] + ADD['ADD_03_03:1']) / 3
ADD['ADD_04'] = (ADD['ADD_04_01:1'] + ADD['ADD_04_02:1'] + ADD['ADD_04_03:1']) / 3
ADD['ADD_05'] = (ADD['ADD_05_01:1'] + ADD['ADD_05_02:1'] + ADD['ADD_05_03:1']) / 3

agg_cols = ['ADD_01', 'ADD_02', 'ADD_03', 'ADD_04', 'ADD_05']
ADD_agg = ADD.copy()[agg_cols]


#ADD_agg.boxplot(vert=False)
plt.grid(axis='x', zorder=0)
sns.boxplot(data=ADD_agg[ADD_agg.columns[::-1]], palette="coolwarm", orient='h')
plt.xlabel('Sound warmth')
plt.title('Additive synthesizer: rating of sonic stimuli from "cold" to "warm"')
plt.xlim([0, 100])
plt.show()


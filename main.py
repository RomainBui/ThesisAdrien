
# coding: utf-8

# ## Librairies

# In[102]:

import pandas as pd
import numpy as np
import scipy.stats
import math
import os
import matplotlib.pyplot as plt
#%matplotlib inline


# ## Input

# In[103]:

L = 20
h = 2.06
l = 2.11


# In[117]:

in_df = pd.read_csv('Data/input.csv', sep = ';')
in_df = in_df.set_index('Material')
#in_df.index = in_df.Material.values


# In[118]:

in_df


# ## Support Function

# In[119]:

def getMeYoung(file_path, L,h,l):

    ### Data Loading & Preparation
    a = pd.read_csv(file_path, sep = '\t')
    X = a.loc[1:] # first line is empty
    X.columns = ['Force', 'Deformation']

    ### Cleaning in order to proper filter on the Deformation [0.01, 0.1]
    ix = (X.loc[:, 'Deformation'] > 0.01) & (X.loc[:, 'Deformation'] < 0.1 )
    X = X.loc[ix]

    try:
        ### Compute Slope
        slope, _, _, _, _ = scipy.stats.linregress(X.loc[:, 'Deformation'], X.loc[:, 'Force'])

        ### Compute Young Module
        E = L**3 * slope / (4 * l * h**3) / 1000
    except:
        E = None

    return E


# ## Make the loop

# In[120]:

YM = []
Material = []
XP = []

path = 'Data/ech_de_adri'

for d in os.listdir(path): ## Loop on the directories
    if d != '.DS_Store':
        for f in os.listdir(path + '/' + d):
            f_path = path + '/' + d + '/' + f
            ## Compute the Young Module
            YM.append(getMeYoung(f_path,in_df.loc[d,'L'],in_df.loc[d,'h'],in_df.loc[d,'l']))
            
            ## Update the Material
            Material.append(d)
            
            ## Update of the experimentator
            XP.append('Adri')
            
            
path = 'Data/ech_de_ali'
for d in os.listdir(path): ## Loop on the directories
    if d != '.DS_Store':
        for f in os.listdir(path + '/' + d):
            f_path = path + '/' + d + '/' + f
            ## Compute the Young Module
            YM.append(getMeYoung(f_path,in_df.loc[d,'L'],in_df.loc[d,'h'],in_df.loc[d,'l']))
            #YM.append(getMeYoung(f_path,L,h,l))
            
            ## Update the Material
            Material.append(d)
            
            ## Update of the experimentator
            XP.append('Ali')


# ## Final Res

# In[121]:

final_res = pd.DataFrame()


# In[122]:

final_res.loc[:, 'Material']       = Material
final_res.loc[:, 'Experimentator'] = XP
final_res.loc[:, 'Young Module']   = YM


# In[123]:

final_res.to_csv('final_res.csv', index = False, sep = ';')


# In[124]:

final_res.loc[final_res.Material == 'Luxacore Z Dual']


# ## Mean / Variance Matrix

# In[125]:

final_res


# In[126]:

final_res.loc[(final_res.Material == 'Permaflow'), :]


# In[127]:

meanvar_matrix = pd.DataFrame(index = set(Material), columns = ['mu', 'var'])
for m in set(Material):
    print(m)
    val = final_res.loc[(final_res.Material == m) & (~final_res.loc[:, 'Young Module'].isnull()), 'Young Module']
    meanvar_matrix.loc[m, 'mu']  = val.mean()
    meanvar_matrix.loc[m, 'var'] = val.var()


# In[128]:

meanvar_matrix.to_csv('meanvar.csv', index = True, sep = ';')


# In[129]:

meanvar_matrix


# ## P-values matrix

# In[130]:

pval_matrix = pd.DataFrame(index = set(Material), columns = set(Material))


# In[131]:

for m1 in set(Material):
    for m2 in set(Material):
        val_1 = final_res.loc[(final_res.Material == m1) & (~final_res.loc[:, 'Young Module'].isnull()), 'Young Module']
        val_2 = final_res.loc[(final_res.Material == m2) & (~final_res.loc[:, 'Young Module'].isnull()), 'Young Module']
        pval_matrix.loc[m1,m2] = scipy.stats.ttest_ind(val_1,  val_2).pvalue


# In[132]:

pval_matrix.to_csv('pval_matrix.csv', index = True, sep = ';')


# In[133]:

pval_matrix


# ## Test

# ## Make a graph

# In[11]:

# ix = final_res.loc[:, 'Material'] == 'Clearfil APX'

# plt.hist(final_res.loc[ix, 'Young Module'])
# plt.xlabel('Young Module Distribution of Clearfil APX')
# plt.show()
# plt.savefig('Clearfill APX.png')


# In[134]:

print('DONE DONE !')


# In[ ]:




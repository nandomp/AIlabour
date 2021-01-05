# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 12:03:52 2019

@author: tolanso
"""

#import os,sys
import sys
import pandas as pd
import seaborn as sns
import numpy as np
import numpy.matlib as mlb
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
fontP = FontProperties()
#import matplotlib.ticker as mticker
from itertools import chain 
#import statsmodels.api as sm
#import matplotlib.cm as cm
import scipy.stats as stats

def load_large_dta(fname):
    
    reader = pd.read_stata(fname, iterator=True)
    df = pd.DataFrame()

    try:
        chunk = reader.get_chunk(100*1000)
        while len(chunk) > 0:
            df = df.append(chunk, ignore_index=True)
            chunk = reader.get_chunk(100*1000)
            print('.'),
            sys.stdout.flush()
    except (StopIteration, KeyboardInterrupt):
        pass

    print('\nloaded {} rows'.format(len(df)))

    return df

#####################Load data#############################
df = pd.read_csv('tasks_cogab.csv')

###############compute cognitive ability scores################

####define names of cognitive abilities vectors
cogabs=['ec','ms','mc','co','ce','pa','mp','as','cl','ql','si','nv','vp','ap']
Cogabs=['EC','MS','MC','CO','CE','PA','MP','AS','CL','QL','SI','NV','VP','AP']


##############Sort variables into indices of task framework####################
###start with a legend
#physical tasks = phy
#intellectual tasks = int
#social tasks = soc

#phy_a          = e_1_a1, e_1_a2, e_1_a3, e_1_a4, o_1_a_1_Static_strength 
#                 o_1_a_2_Dynamic_strength, o_1_a_3_Trunk_strength
#phy_b          = p_1_b_1, o_1_b_1_Armhand_steadyness, o_1_b_2_Manual_dexterity,
#                 o_1_b_3_Finger_dexterity
#int_a_I_i      = p_2_a_I_i1, p_2_a_I_i2, p_2_a_I_i3
#int_a_I_ii     = p_2_a_I_ii1, p_2_a_I_ii2, p_2_a_I_ii3, p_2_a_I_ii4, p_2_a_I_ii5
#int_a_I_iii    = p_2_a_I_iii1, p_2_a_I_iii2, p_2_a_I_iii3, p_2_a_I_iii4
#int_a_II_i     = p_2_a_II_i1, p_2_a_II_i2, p_2_a_II_i3, o_2_a_II_i_1_OralComp,
#                 o_2_a_II_i_2_WritComp, o_2_a_II_i_3_OralExp, o_2_a_II_i_4_WritExp,                 
#int_a_II_ii    = p_2_a_II_ii1, p_2_a_II_ii2, p_2_a_II_ii3, o_2_a_II_ii_1_Math 
#                 o_2_a_II_ii_2_Num
#int_b_I        = e_2_b_I_2, o_2_b_I_1_Deduct, o_2_b_I_1_Induct, o_2_b_I_1_Info
#int_b_II       = e_2_b_II_1, e_2_b_II_2, o_2_b_II_1_Orig
#soc_a          = o_3_a_1_PerfPub
#soc_b          = p_3_b1, p_3_b2, p_3_b3, p_3_b4, o_3_b_1_Instruct, o_3_b_2_Teach
#                 o_3_b_3_Coach
#soc_c          = p_3_c1, p_3_c2, o_3_c_1_Persuad, o_3_c_2_Negotiat, o_3_c_3_Sellinfl
#                 o_3_c_4_Resolv, 
#soc_d          = p_3_d1, p_3_d2, o_3_d_1_Coordin, o_3_d_2_Guiding 

###########################
####Start with sorting into indices#####
###########################
##############normal



for cog in cogabs:
    
    df['index_'+cog+'n_phy_a'] = (df[cog+'_e_1_a1_wt'] + df[cog+'_e_1_a2_wt'] + df[cog+'_e_1_a3_wt'] \
    + df[cog+'_e_1_a4_wt'] + df[cog+'_o_1_a_1_Static_wt'] + df[cog+'_o_1_a_2_Dynamic_wt'] \
    + df[cog+'_o_1_a_3_Trunk_wt'])/np.sum([df[cog+'_e_1_a1_wt']>0 , df[cog+'_e_1_a2_wt']>0 , df[cog+'_e_1_a3_wt']>0, \
     df[cog+'_e_1_a4_wt']>0 , df[cog+'_o_1_a_1_Static_wt']>0 , df[cog+'_o_1_a_2_Dynamic_wt']>0, \
     df[cog+'_o_1_a_3_Trunk_wt']>0],axis=0)
    df['index_'+cog+'n_phy_a'] = df['index_'+cog+'n_phy_a'].replace([np.inf, -np.inf], np.nan).fillna(0)
      
#7      
    
    df['index_'+cog+'n_phy_b'] = (df[cog+'_p_1_b1_wt'] + df[cog+'_o_1_b_1_Armhand_wt'] \
      + df[cog+'_o_1_b_2_Manual_wt'] + df[cog+'_o_1_b_3_Finger_wt'])/np.sum([df[cog+'_p_1_b1_wt']>0 , df[cog+'_o_1_b_1_Armhand_wt']>0 , \
       df[cog+'_o_1_b_2_Manual_wt'] >0 , df[cog+'_o_1_b_3_Finger_wt'] >0 ],axis=0)
    df['index_'+cog+'n_phy_b'] = df['index_'+cog+'n_phy_b'].replace([np.inf, -np.inf], np.nan).fillna(0)
#4
    
    df['index_'+cog+'n_int_a_I_i'] = (df[cog+'_p_2_a_I_i1_wt'] + df[cog+'_p_2_a_I_i2_wt'] \
      + df[cog+'_p_2_a_I_i3_wt'])/np.sum([df[cog+'_p_2_a_I_i1_wt'] >0 , df[cog+'_p_2_a_I_i2_wt']>0 , \
       df[cog+'_p_2_a_I_i3_wt'] >0 ],axis=0)
    df['index_'+cog+'n_int_a_I_i'] = df['index_'+cog+'n_int_a_I_i'].replace([np.inf, -np.inf], np.nan).fillna(0) 
#3
      
    df['index_'+cog+'n_int_a_I_ii'] = (df[cog+'_p_2_a_I_ii1_wt'] + df[cog+'_p_2_a_I_ii2_wt'] \
      + df[cog+'_p_2_a_I_ii3_wt'] + df[cog+'_p_2_a_I_ii4_wt'] + df[cog+'_p_2_a_I_ii5_wt'])/np.sum([df[cog+'_p_2_a_I_ii1_wt']  >0 , \
          df[cog+'_p_2_a_I_ii2_wt']  >0 , df[cog+'_p_2_a_I_ii3_wt']  >0 , df[cog+'_p_2_a_I_ii4_wt']  >0 , df[cog+'_p_2_a_I_ii5_wt'] >0 ],axis=0)
    df['index_'+cog+'n_int_a_I_ii'] = df['index_'+cog+'n_int_a_I_ii'].replace([np.inf, -np.inf], np.nan).fillna(0)  
#5
      
    df['index_'+cog+'n_int_a_I_iii'] = (df[cog+'_p_2_a_I_iii1_wt'] + df[cog+'_p_2_a_I_iii2_wt'] \
      + df[cog+'_p_2_a_I_iii3_wt'] + df[cog+'_p_2_a_I_iii4_wt'])/np.sum([df[cog+'_p_2_a_I_iii1_wt']  >0 , df[cog+'_p_2_a_I_iii2_wt'] >0 , \
       df[cog+'_p_2_a_I_iii3_wt']  >0 , df[cog+'_p_2_a_I_iii4_wt'] >0 ],axis=0)
    df['index_'+cog+'n_int_a_I_iii'] = df['index_'+cog+'n_int_a_I_iii'].replace([np.inf, -np.inf], np.nan).fillna(0)    
    
      
#4
      
    df['index_'+cog+'n_int_a_II_i'] = (df[cog+'_p_2_a_II_i1_wt'] + df[cog+'_p_2_a_II_i2_wt'] \
      + df[cog+'_p_2_a_II_i3_wt'] +  df[cog+'_o_2_a_II_i_1_OComp_wt'] + df[cog+'_o_2_a_II_i_2_WComp_wt'] \
      + df[cog+'_o_2_a_II_i_3_OExp_wt'] +  df[cog+'_o_2_a_II_i_4_WExp_wt'])/np.sum([df[cog+'_p_2_a_II_i1_wt']  >0 , df[cog+'_p_2_a_II_i2_wt'] >0 , \
       df[cog+'_p_2_a_II_i3_wt']  >0 ,  df[cog+'_o_2_a_II_i_1_OComp_wt']  >0 , df[cog+'_o_2_a_II_i_2_WComp_wt'] >0 , \
       df[cog+'_o_2_a_II_i_3_OExp_wt']  >0 ,  df[cog+'_o_2_a_II_i_4_WExp_wt'] >0 ],axis=0)
    df['index_'+cog+'n_int_a_II_i']  = df['index_'+cog+'n_int_a_II_i'].replace([np.inf, -np.inf], np.nan).fillna(0)
      
#7
      
    df['index_'+cog+'n_int_a_II_ii'] = (df[cog+'_p_2_a_II_ii1_wt'] + df[cog+'_p_2_a_II_ii2_wt'] \
     + df[cog+'_p_2_a_II_ii3_wt'] + df[cog+'_o_2_a_II_ii_1_Math_wt'] \
     + df[cog+'_o_2_a_II_ii_2_Num_wt'])/np.sum([df[cog+'_p_2_a_II_ii1_wt']  >0 , df[cog+'_p_2_a_II_ii2_wt'] >0 , \
      df[cog+'_p_2_a_II_ii3_wt']  >0 , df[cog+'_o_2_a_II_ii_1_Math_wt'] >0 , \
      df[cog+'_o_2_a_II_ii_2_Num_wt'] >0 ],axis=0)
    df['index_'+cog+'n_int_a_II_ii']  = df['index_'+cog+'n_int_a_II_ii'].replace([np.inf, -np.inf], np.nan).fillna(0)
    
      
#5      
      
    df['index_'+cog+'n_int_b_I'] = (df[cog+'_e_2_b_I_2_wt'] + df[cog+'_o_2_b_I_1_Deduct_wt'] \
      + df[cog+'_o_2_b_I_1_Induct_wt'] + df[cog+'_o_2_b_I_1_Info_wt'])/np.sum([df[cog+'_e_2_b_I_2_wt']  >0 , df[cog+'_o_2_b_I_1_Deduct_wt'] >0 , \
       df[cog+'_o_2_b_I_1_Induct_wt']  >0 , df[cog+'_o_2_b_I_1_Info_wt'] >0 ],axis=0)
    df['index_'+cog+'n_int_b_I'] = df['index_'+cog+'n_int_b_I'].replace([np.inf, -np.inf], np.nan).fillna(0)
    
      
#4      
      
    df['index_'+cog+'n_int_b_II'] = (df[cog+'_e_2_b_II_1_wt'] + df[cog+'_e_2_b_II_2_wt'] \
      + df[cog+'_o_2_b_II_1_Orig_wt'])/np.sum([df[cog+'_e_2_b_II_1_wt']  >0 , df[cog+'_e_2_b_II_2_wt'] >0 , \
       df[cog+'_o_2_b_II_1_Orig_wt'] >0 ],axis=0)
    df['index_'+cog+'n_int_b_II'] = df['index_'+cog+'n_int_b_II'].replace([np.inf, -np.inf], np.nan).fillna(0)
   
      
#3      
      
    df['index_'+cog+'n_soc_a'] = (df[cog+'_o_3_a_1_PerfPub_wt'])
    
    df['index_'+cog+'n_soc_b'] = (df[cog+'_p_3_b1_wt'] + df[cog+'_p_3_b2_wt'] \
      + df[cog+'_p_3_b3_wt'] + df[cog+'_p_3_b4_wt'] + df[cog+'_o_3_b_1_Instruct_wt'] \
      + df[cog+'_o_3_b_2_Teach_wt'] + df[cog+'_o_3_b_3_Coach_wt'])/np.sum([df[cog+'_p_3_b1_wt']  >0 , df[cog+'_p_3_b2_wt'] >0 , \
       df[cog+'_p_3_b3_wt']  >0 , df[cog+'_p_3_b4_wt']  >0 , df[cog+'_o_3_b_1_Instruct_wt'] >0 , \
       df[cog+'_o_3_b_2_Teach_wt']  >0 , df[cog+'_o_3_b_3_Coach_wt'] >0 ],axis=0)
    df['index_'+cog+'n_soc_b'] = df['index_'+cog+'n_soc_b'].replace([np.inf, -np.inf], np.nan).fillna(0)
   
      
#7      
      
    df['index_'+cog+'n_soc_c'] = (df[cog+'_p_3_c1_wt'] + df[cog+'_p_3_c2_wt'] \
      + df[cog+'_o_3_c_1_Persuad_wt'] + df[cog+'_o_3_c_2_Negotiat_wt'] \
      + df[cog+'_o_3_c_3_Sellinfl_wt'] + df[cog+'_o_3_c_4_Resolv_wt'])/np.sum([df[cog+'_p_3_b1_wt']  >0 , df[cog+'_p_3_b2_wt'] >0 , \
       df[cog+'_p_3_b3_wt']  >0 , df[cog+'_p_3_b4_wt']  >0 , df[cog+'_o_3_b_1_Instruct_wt'] >0 , \
       df[cog+'_o_3_b_2_Teach_wt']  >0 , df[cog+'_o_3_b_3_Coach_wt'] >0 ],axis=0)
    df['index_'+cog+'n_soc_c'] = df['index_'+cog+'n_soc_c'].replace([np.inf, -np.inf], np.nan).fillna(0)
   
      
#6      
      
    df['index_'+cog+'n_soc_d'] = (df[cog+'_p_3_d1_wt'] + df[cog+'_p_3_d2_wt'] \
      + df[cog+'_o_3_d_1_Coordin_wt'] + df[cog+'_o_3_d_2_Guiding_wt'])/np.sum([df[cog+'_p_3_d1_wt']  >0 , df[cog+'_p_3_d2_wt'] >0 , \
       df[cog+'_o_3_d_1_Coordin_wt']  >0 , df[cog+'_o_3_d_2_Guiding_wt'] >0 ],axis=0)
    df['index_'+cog+'n_soc_d'] = df['index_'+cog+'n_soc_d'].replace([np.inf, -np.inf], np.nan).fillna(0)
   
      
#4      
      
    df['index_norm'+cog+'n_phy_a']=df['index_'+cog+'n_phy_a']/np.max(df['index_'+cog+'n_phy_a'],axis=0)
    df['index_norm'+cog+'n_phy_b']=df['index_'+cog+'n_phy_b']/np.max(df['index_'+cog+'n_phy_b'],axis=0)
    
############min1sd
for cog in cogabs:
    df['index_'+cog+'_min1sd_phy_a'] = (df[cog+'_min1sd_e_1_a1_wt'] + df[cog+'_min1sd_e_1_a2_wt'] + df[cog+'_min1sd_e_1_a3_wt'] \
    + df[cog+'_min1sd_e_1_a4_wt'] + df[cog+'_min1sd_o_1_a_1_Static_wt'] + df[cog+'_min1sd_o_1_a_2_Dynamic_wt'] \
    + df[cog+'_min1sd_o_1_a_3_Trunk_wt'])/np.sum([df[cog+'_min1sd_e_1_a1_wt']>0 , df[cog+'_min1sd_e_1_a2_wt']>0 , df[cog+'_min1sd_e_1_a3_wt']>0, \
     df[cog+'_min1sd_e_1_a4_wt']>0 , df[cog+'_min1sd_o_1_a_1_Static_wt']>0 , df[cog+'_min1sd_o_1_a_2_Dynamic_wt']>0, \
     df[cog+'_min1sd_o_1_a_3_Trunk_wt']>0],axis=0)
    df['index_'+cog+'_min1sd_phy_a'] = df['index_'+cog+'_min1sd_phy_a'].replace([np.inf, -np.inf], np.nan).fillna(0)
    
      
#7      
    
    df['index_'+cog+'_min1sd_phy_b'] = (df[cog+'_min1sd_p_1_b1_wt'] + df[cog+'_min1sd_o_1_b_1_Armhand_wt'] \
      + df[cog+'_min1sd_o_1_b_2_Manual_wt'] + df[cog+'_min1sd_o_1_b_3_Finger_wt'])/np.sum([df[cog+'_min1sd_p_1_b1_wt']>0 , df[cog+'_min1sd_o_1_b_1_Armhand_wt']>0 , \
       df[cog+'_min1sd_o_1_b_2_Manual_wt'] >0 , df[cog+'_min1sd_o_1_b_3_Finger_wt'] >0 ],axis=0)
    df['index_'+cog+'_min1sd_phy_b'] = df['index_'+cog+'_min1sd_phy_b'].replace([np.inf, -np.inf], np.nan).fillna(0)
    
#4
    
    df['index_'+cog+'_min1sd_int_a_I_i'] = (df[cog+'_min1sd_p_2_a_I_i1_wt'] + df[cog+'_min1sd_p_2_a_I_i2_wt'] \
      + df[cog+'_min1sd_p_2_a_I_i3_wt'])/np.sum([df[cog+'_min1sd_p_2_a_I_i1_wt'] >0 , df[cog+'_min1sd_p_2_a_I_i2_wt']>0 , \
       df[cog+'_min1sd_p_2_a_I_i3_wt'] >0 ],axis=0)
    df['index_'+cog+'_min1sd_int_a_I_i'] = df['index_'+cog+'_min1sd_int_a_I_i'].replace([np.inf, -np.inf], np.nan).fillna(0)
    
#3
      
    df['index_'+cog+'_min1sd_int_a_I_ii'] = (df[cog+'_min1sd_p_2_a_I_ii1_wt'] + df[cog+'_min1sd_p_2_a_I_ii2_wt'] \
      + df[cog+'_min1sd_p_2_a_I_ii3_wt'] + df[cog+'_min1sd_p_2_a_I_ii4_wt'] + df[cog+'_min1sd_p_2_a_I_ii5_wt'])/np.sum([df[cog+'_min1sd_p_2_a_I_ii1_wt']  >0 , \
          df[cog+'_min1sd_p_2_a_I_ii2_wt']  >0 , df[cog+'_min1sd_p_2_a_I_ii3_wt']  >0 , df[cog+'_min1sd_p_2_a_I_ii4_wt']  >0 , df[cog+'_min1sd_p_2_a_I_ii5_wt'] >0 ],axis=0)
    df['index_'+cog+'_min1sd_int_a_I_ii'] = df['index_'+cog+'_min1sd_int_a_I_ii'].replace([np.inf, -np.inf], np.nan).fillna(0)
      
#5
      
    df['index_'+cog+'_min1sd_int_a_I_iii'] = (df[cog+'_min1sd_p_2_a_I_iii1_wt'] + df[cog+'_min1sd_p_2_a_I_iii2_wt'] \
      + df[cog+'_min1sd_p_2_a_I_iii3_wt'] + df[cog+'_min1sd_p_2_a_I_iii4_wt'])/np.sum([df[cog+'_min1sd_p_2_a_I_iii1_wt']  >0 , df[cog+'_min1sd_p_2_a_I_iii2_wt'] >0 , \
       df[cog+'_min1sd_p_2_a_I_iii3_wt']  >0 , df[cog+'_min1sd_p_2_a_I_iii4_wt'] >0 ],axis=0)
    df['index_'+cog+'_min1sd_int_a_I_iii'] = df['index_'+cog+'_min1sd_int_a_I_iii'].replace([np.inf, -np.inf], np.nan).fillna(0)
    
      
#4
      
    df['index_'+cog+'_min1sd_int_a_II_i'] = (df[cog+'_min1sd_p_2_a_II_i1_wt'] + df[cog+'_min1sd_p_2_a_II_i2_wt'] \
      + df[cog+'_min1sd_p_2_a_II_i3_wt'] +  df[cog+'_min1sd_o_2_a_II_i_1_OComp_wt'] + df[cog+'_min1sd_o_2_a_II_i_2_WComp_wt'] \
      + df[cog+'_min1sd_o_2_a_II_i_3_OExp_wt'] +  df[cog+'_min1sd_o_2_a_II_i_4_WExp_wt'])/np.sum([df[cog+'_min1sd_p_2_a_II_i1_wt']  >0 , df[cog+'_min1sd_p_2_a_II_i2_wt'] >0 , \
       df[cog+'_min1sd_p_2_a_II_i3_wt']  >0 ,  df[cog+'_min1sd_o_2_a_II_i_1_OComp_wt']  >0 , df[cog+'_min1sd_o_2_a_II_i_2_WComp_wt'] >0 , \
       df[cog+'_min1sd_o_2_a_II_i_3_OExp_wt']  >0 ,  df[cog+'_min1sd_o_2_a_II_i_4_WExp_wt'] >0 ],axis=0)
    df['index_'+cog+'_min1sd_int_a_II_i'] = df['index_'+cog+'_min1sd_int_a_II_i'].replace([np.inf, -np.inf], np.nan).fillna(0)
    
      
#7
      
    df['index_'+cog+'_min1sd_int_a_II_ii'] = (df[cog+'_min1sd_p_2_a_II_ii1_wt'] + df[cog+'_min1sd_p_2_a_II_ii2_wt'] \
     + df[cog+'_min1sd_p_2_a_II_ii3_wt'] + df[cog+'_min1sd_o_2_a_II_ii_1_Math_wt'] \
     + df[cog+'_min1sd_o_2_a_II_ii_2_Num_wt'])/np.sum([df[cog+'_min1sd_p_2_a_II_ii1_wt']  >0 , df[cog+'_min1sd_p_2_a_II_ii2_wt'] >0 , \
      df[cog+'_min1sd_p_2_a_II_ii3_wt']  >0 , df[cog+'_min1sd_o_2_a_II_ii_1_Math_wt'] >0 , \
      df[cog+'_min1sd_o_2_a_II_ii_2_Num_wt'] >0 ],axis=0)
    df['index_'+cog+'_min1sd_int_a_II_ii'] = df['index_'+cog+'_min1sd_int_a_II_ii'].replace([np.inf, -np.inf], np.nan).fillna(0)
    
    
      
#5      
      
    df['index_'+cog+'_min1sd_int_b_I'] = (df[cog+'_min1sd_e_2_b_I_2_wt'] + df[cog+'_min1sd_o_2_b_I_1_Deduct_wt'] \
      + df[cog+'_min1sd_o_2_b_I_1_Induct_wt'] + df[cog+'_min1sd_o_2_b_I_1_Info_wt'])/np.sum([df[cog+'_min1sd_e_2_b_I_2_wt']  >0 , df[cog+'_min1sd_o_2_b_I_1_Deduct_wt'] >0 , \
       df[cog+'_min1sd_o_2_b_I_1_Induct_wt']  >0 , df[cog+'_min1sd_o_2_b_I_1_Info_wt'] >0 ],axis=0)
    df['index_'+cog+'_min1sd_int_b_I'] = df['index_'+cog+'_min1sd_int_b_I'].replace([np.inf, -np.inf], np.nan).fillna(0)
    
      
#4      
      
    df['index_'+cog+'_min1sd_int_b_II'] = (df[cog+'_min1sd_e_2_b_II_1_wt'] + df[cog+'_min1sd_e_2_b_II_2_wt'] \
      + df[cog+'_min1sd_o_2_b_II_1_Orig_wt'])/np.sum([df[cog+'_min1sd_e_2_b_II_1_wt']  >0 , df[cog+'_min1sd_e_2_b_II_2_wt'] >0 , \
       df[cog+'_min1sd_o_2_b_II_1_Orig_wt'] >0 ],axis=0)
    df['index_'+cog+'_min1sd_int_b_II'] = df['index_'+cog+'_min1sd_int_b_II'].replace([np.inf, -np.inf], np.nan).fillna(0)
    
      
#3      
      
    df['index_'+cog+'_min1sd_soc_a'] = (df[cog+'_min1sd_o_3_a_1_PerfPub_wt'])
    
    df['index_'+cog+'_min1sd_soc_b'] = (df[cog+'_min1sd_p_3_b1_wt'] + df[cog+'_min1sd_p_3_b2_wt'] \
      + df[cog+'_min1sd_p_3_b3_wt'] + df[cog+'_min1sd_p_3_b4_wt'] + df[cog+'_min1sd_o_3_b_1_Instruct_wt'] \
      + df[cog+'_min1sd_o_3_b_2_Teach_wt'] + df[cog+'_min1sd_o_3_b_3_Coach_wt'])/np.sum([df[cog+'_min1sd_p_3_b1_wt']  >0 , df[cog+'_min1sd_p_3_b2_wt'] >0 , \
       df[cog+'_min1sd_p_3_b3_wt']  >0 , df[cog+'_min1sd_p_3_b4_wt']  >0 , df[cog+'_min1sd_o_3_b_1_Instruct_wt'] >0 , \
       df[cog+'_min1sd_o_3_b_2_Teach_wt']  >0 , df[cog+'_min1sd_o_3_b_3_Coach_wt'] >0 ],axis=0)
    df['index_'+cog+'_min1sd_soc_b'] = df['index_'+cog+'_min1sd_soc_b'].replace([np.inf, -np.inf], np.nan).fillna(0)
    
      
#7      
      
    df['index_'+cog+'_min1sd_soc_c'] = (df[cog+'_min1sd_p_3_c1_wt'] + df[cog+'_min1sd_p_3_c2_wt'] \
      + df[cog+'_min1sd_o_3_c_1_Persuad_wt'] + df[cog+'_min1sd_o_3_c_2_Negotiat_wt'] \
      + df[cog+'_min1sd_o_3_c_3_Sellinfl_wt'] + df[cog+'_min1sd_o_3_c_4_Resolv_wt'])/np.sum([df[cog+'_min1sd_p_3_b1_wt']  >0 , df[cog+'_min1sd_p_3_b2_wt'] >0 , \
       df[cog+'_min1sd_p_3_b3_wt']  >0 , df[cog+'_min1sd_p_3_b4_wt']  >0 , df[cog+'_min1sd_o_3_b_1_Instruct_wt'] >0 , \
       df[cog+'_min1sd_o_3_b_2_Teach_wt']  >0 , df[cog+'_min1sd_o_3_b_3_Coach_wt'] >0 ],axis=0)
    df['index_'+cog+'_min1sd_soc_c'] = df['index_'+cog+'_min1sd_soc_c'].replace([np.inf, -np.inf], np.nan).fillna(0)
    
      
#6      
      
    df['index_'+cog+'_min1sd_soc_d'] = (df[cog+'_min1sd_p_3_d1_wt'] + df[cog+'_min1sd_p_3_d2_wt'] \
      + df[cog+'_min1sd_o_3_d_1_Coordin_wt'] + df[cog+'_min1sd_o_3_d_2_Guiding_wt'])/np.sum([df[cog+'_min1sd_p_3_d1_wt']  >0 , df[cog+'_min1sd_p_3_d2_wt'] >0 , \
       df[cog+'_min1sd_o_3_d_1_Coordin_wt']  >0 , df[cog+'_min1sd_o_3_d_2_Guiding_wt'] >0 ],axis=0)
    df['index_'+cog+'_min1sd_soc_d'] = df['index_'+cog+'_min1sd_soc_d'].replace([np.inf, -np.inf], np.nan).fillna(0)
    
      
#4 
      
    df['index_norm'+cog+'_min1sd_phy_a']=df['index_'+cog+'_min1sd_phy_a']/np.max(df['index_'+cog+'_min1sd_phy_a'],axis=0)
    df['index_norm'+cog+'_min1sd_phy_b']=df['index_'+cog+'_min1sd_phy_b']/np.max(df['index_'+cog+'_min1sd_phy_b'],axis=0)


################# plu1sd
    
for cog in cogabs:
    df['index_'+cog+'_plu1sd_phy_a'] = (df[cog+'_plu1sd_e_1_a1_wt'] + df[cog+'_plu1sd_e_1_a2_wt'] + df[cog+'_plu1sd_e_1_a3_wt'] \
    + df[cog+'_plu1sd_e_1_a4_wt'] + df[cog+'_plu1sd_o_1_a_1_Static_wt'] + df[cog+'_plu1sd_o_1_a_2_Dynamic_wt'] \
    + df[cog+'_plu1sd_o_1_a_3_Trunk_wt'])/np.sum([df[cog+'_plu1sd_e_1_a1_wt']>0 , df[cog+'_plu1sd_e_1_a2_wt']>0 , df[cog+'_plu1sd_e_1_a3_wt']>0, \
     df[cog+'_plu1sd_e_1_a4_wt']>0 , df[cog+'_plu1sd_o_1_a_1_Static_wt']>0 , df[cog+'_plu1sd_o_1_a_2_Dynamic_wt']>0, \
     df[cog+'_plu1sd_o_1_a_3_Trunk_wt']>0],axis=0)
    df['index_'+cog+'_plu1sd_phy_a'] = df['index_'+cog+'_plu1sd_phy_a'].replace([np.inf, -np.inf], np.nan).fillna(0)
    
      
#7      
    
    df['index_'+cog+'_plu1sd_phy_b'] = (df[cog+'_plu1sd_p_1_b1_wt'] + df[cog+'_plu1sd_o_1_b_1_Armhand_wt'] \
      + df[cog+'_plu1sd_o_1_b_2_Manual_wt'] + df[cog+'_plu1sd_o_1_b_3_Finger_wt'])/np.sum([df[cog+'_plu1sd_p_1_b1_wt']>0 , df[cog+'_plu1sd_o_1_b_1_Armhand_wt']>0 , \
       df[cog+'_plu1sd_o_1_b_2_Manual_wt'] >0 , df[cog+'_plu1sd_o_1_b_3_Finger_wt'] >0 ],axis=0)
    df['index_'+cog+'_plu1sd_phy_b'] = df['index_'+cog+'_plu1sd_phy_b'].replace([np.inf, -np.inf], np.nan).fillna(0)
    
#4
    
    df['index_'+cog+'_plu1sd_int_a_I_i'] = (df[cog+'_plu1sd_p_2_a_I_i1_wt'] + df[cog+'_plu1sd_p_2_a_I_i2_wt'] \
      + df[cog+'_plu1sd_p_2_a_I_i3_wt'])/np.sum([df[cog+'_plu1sd_p_2_a_I_i1_wt'] >0 , df[cog+'_plu1sd_p_2_a_I_i2_wt']>0 , \
       df[cog+'_plu1sd_p_2_a_I_i3_wt'] >0 ],axis=0)
    df['index_'+cog+'_plu1sd_int_a_I_i'] = df['index_'+cog+'_plu1sd_int_a_I_i'].replace([np.inf, -np.inf], np.nan).fillna(0)
    
#3
      
    df['index_'+cog+'_plu1sd_int_a_I_ii'] = (df[cog+'_plu1sd_p_2_a_I_ii1_wt'] + df[cog+'_plu1sd_p_2_a_I_ii2_wt'] \
      + df[cog+'_plu1sd_p_2_a_I_ii3_wt'] + df[cog+'_plu1sd_p_2_a_I_ii4_wt'] + df[cog+'_plu1sd_p_2_a_I_ii5_wt'])/np.sum([df[cog+'_plu1sd_p_2_a_I_ii1_wt']  >0 , \
          df[cog+'_plu1sd_p_2_a_I_ii2_wt']  >0 , df[cog+'_plu1sd_p_2_a_I_ii3_wt']  >0 , df[cog+'_plu1sd_p_2_a_I_ii4_wt']  >0 , df[cog+'_plu1sd_p_2_a_I_ii5_wt'] >0 ],axis=0)
    df['index_'+cog+'_plu1sd_int_a_I_ii'] = df['index_'+cog+'_plu1sd_int_a_I_ii'].replace([np.inf, -np.inf], np.nan).fillna(0)
      
#5
      
    df['index_'+cog+'_plu1sd_int_a_I_iii'] = (df[cog+'_plu1sd_p_2_a_I_iii1_wt'] + df[cog+'_plu1sd_p_2_a_I_iii2_wt'] \
      + df[cog+'_plu1sd_p_2_a_I_iii3_wt'] + df[cog+'_plu1sd_p_2_a_I_iii4_wt'])/np.sum([df[cog+'_plu1sd_p_2_a_I_iii1_wt']  >0 , df[cog+'_plu1sd_p_2_a_I_iii2_wt'] >0 , \
       df[cog+'_plu1sd_p_2_a_I_iii3_wt']  >0 , df[cog+'_plu1sd_p_2_a_I_iii4_wt'] >0 ],axis=0)
    df['index_'+cog+'_plu1sd_int_a_I_iii'] = df['index_'+cog+'_plu1sd_int_a_I_iii'].replace([np.inf, -np.inf], np.nan).fillna(0)
    
      
#4
      
    df['index_'+cog+'_plu1sd_int_a_II_i'] = (df[cog+'_plu1sd_p_2_a_II_i1_wt'] + df[cog+'_plu1sd_p_2_a_II_i2_wt'] \
      + df[cog+'_plu1sd_p_2_a_II_i3_wt'] +  df[cog+'_plu1sd_o_2_a_II_i_1_OComp_wt'] + df[cog+'_plu1sd_o_2_a_II_i_2_WComp_wt'] \
      + df[cog+'_plu1sd_o_2_a_II_i_3_OExp_wt'] +  df[cog+'_plu1sd_o_2_a_II_i_4_WExp_wt'])/np.sum([df[cog+'_plu1sd_p_2_a_II_i1_wt']  >0 , df[cog+'_plu1sd_p_2_a_II_i2_wt'] >0 , \
       df[cog+'_plu1sd_p_2_a_II_i3_wt']  >0 ,  df[cog+'_plu1sd_o_2_a_II_i_1_OComp_wt']  >0 , df[cog+'_plu1sd_o_2_a_II_i_2_WComp_wt'] >0 , \
       df[cog+'_plu1sd_o_2_a_II_i_3_OExp_wt']  >0 ,  df[cog+'_plu1sd_o_2_a_II_i_4_WExp_wt'] >0 ],axis=0)
    df['index_'+cog+'_plu1sd_int_a_II_i'] = df['index_'+cog+'_plu1sd_int_a_II_i'].replace([np.inf, -np.inf], np.nan).fillna(0)
    
      
#7
      
    df['index_'+cog+'_plu1sd_int_a_II_ii'] = (df[cog+'_plu1sd_p_2_a_II_ii1_wt'] + df[cog+'_plu1sd_p_2_a_II_ii2_wt'] \
     + df[cog+'_plu1sd_p_2_a_II_ii3_wt'] + df[cog+'_plu1sd_o_2_a_II_ii_1_Math_wt'] \
     + df[cog+'_plu1sd_o_2_a_II_ii_2_Num_wt'])/np.sum([df[cog+'_plu1sd_p_2_a_II_ii1_wt']  >0 , df[cog+'_plu1sd_p_2_a_II_ii2_wt'] >0 , \
      df[cog+'_plu1sd_p_2_a_II_ii3_wt']  >0 , df[cog+'_plu1sd_o_2_a_II_ii_1_Math_wt'] >0 , \
      df[cog+'_plu1sd_o_2_a_II_ii_2_Num_wt'] >0 ],axis=0)
    df['index_'+cog+'_plu1sd_int_a_II_ii'] = df['index_'+cog+'_plu1sd_int_a_II_ii'].replace([np.inf, -np.inf], np.nan).fillna(0)
    
    
      
#5      
      
    df['index_'+cog+'_plu1sd_int_b_I'] = (df[cog+'_plu1sd_e_2_b_I_2_wt'] + df[cog+'_plu1sd_o_2_b_I_1_Deduct_wt'] \
      + df[cog+'_plu1sd_o_2_b_I_1_Induct_wt'] + df[cog+'_plu1sd_o_2_b_I_1_Info_wt'])/np.sum([df[cog+'_plu1sd_e_2_b_I_2_wt']  >0 , df[cog+'_plu1sd_o_2_b_I_1_Deduct_wt'] >0 , \
       df[cog+'_plu1sd_o_2_b_I_1_Induct_wt']  >0 , df[cog+'_plu1sd_o_2_b_I_1_Info_wt'] >0 ],axis=0)
    df['index_'+cog+'_plu1sd_int_b_I'] = df['index_'+cog+'_plu1sd_int_b_I'].replace([np.inf, -np.inf], np.nan).fillna(0)
    
      
#4      
      
    df['index_'+cog+'_plu1sd_int_b_II'] = (df[cog+'_plu1sd_e_2_b_II_1_wt'] + df[cog+'_plu1sd_e_2_b_II_2_wt'] \
      + df[cog+'_plu1sd_o_2_b_II_1_Orig_wt'])/np.sum([df[cog+'_plu1sd_e_2_b_II_1_wt']  >0 , df[cog+'_plu1sd_e_2_b_II_2_wt'] >0 , \
       df[cog+'_plu1sd_o_2_b_II_1_Orig_wt'] >0 ],axis=0)
    df['index_'+cog+'_plu1sd_int_b_II'] = df['index_'+cog+'_plu1sd_int_b_II'].replace([np.inf, -np.inf], np.nan).fillna(0)
    
      
#3      
      
    df['index_'+cog+'_plu1sd_soc_a'] = (df[cog+'_plu1sd_o_3_a_1_PerfPub_wt'])
    
    df['index_'+cog+'_plu1sd_soc_b'] = (df[cog+'_plu1sd_p_3_b1_wt'] + df[cog+'_plu1sd_p_3_b2_wt'] \
      + df[cog+'_plu1sd_p_3_b3_wt'] + df[cog+'_plu1sd_p_3_b4_wt'] + df[cog+'_plu1sd_o_3_b_1_Instruct_wt'] \
      + df[cog+'_plu1sd_o_3_b_2_Teach_wt'] + df[cog+'_plu1sd_o_3_b_3_Coach_wt'])/np.sum([df[cog+'_plu1sd_p_3_b1_wt']  >0 , df[cog+'_plu1sd_p_3_b2_wt'] >0 , \
       df[cog+'_plu1sd_p_3_b3_wt']  >0 , df[cog+'_plu1sd_p_3_b4_wt']  >0 , df[cog+'_plu1sd_o_3_b_1_Instruct_wt'] >0 , \
       df[cog+'_plu1sd_o_3_b_2_Teach_wt']  >0 , df[cog+'_plu1sd_o_3_b_3_Coach_wt'] >0 ],axis=0)
    df['index_'+cog+'_plu1sd_soc_b'] = df['index_'+cog+'_plu1sd_soc_b'].replace([np.inf, -np.inf], np.nan).fillna(0)
    
      
#7      
      
    df['index_'+cog+'_plu1sd_soc_c'] = (df[cog+'_plu1sd_p_3_c1_wt'] + df[cog+'_plu1sd_p_3_c2_wt'] \
      + df[cog+'_plu1sd_o_3_c_1_Persuad_wt'] + df[cog+'_plu1sd_o_3_c_2_Negotiat_wt'] \
      + df[cog+'_plu1sd_o_3_c_3_Sellinfl_wt'] + df[cog+'_plu1sd_o_3_c_4_Resolv_wt'])/np.sum([df[cog+'_plu1sd_p_3_b1_wt']  >0 , df[cog+'_plu1sd_p_3_b2_wt'] >0 , \
       df[cog+'_plu1sd_p_3_b3_wt']  >0 , df[cog+'_plu1sd_p_3_b4_wt']  >0 , df[cog+'_plu1sd_o_3_b_1_Instruct_wt'] >0 , \
       df[cog+'_plu1sd_o_3_b_2_Teach_wt']  >0 , df[cog+'_plu1sd_o_3_b_3_Coach_wt'] >0 ],axis=0)
    df['index_'+cog+'_plu1sd_soc_c'] = df['index_'+cog+'_plu1sd_soc_c'].replace([np.inf, -np.inf], np.nan).fillna(0)
    
      
#6      
      
    df['index_'+cog+'_plu1sd_soc_d'] = (df[cog+'_plu1sd_p_3_d1_wt'] + df[cog+'_plu1sd_p_3_d2_wt'] \
      + df[cog+'_plu1sd_o_3_d_1_Coordin_wt'] + df[cog+'_plu1sd_o_3_d_2_Guiding_wt'])/np.sum([df[cog+'_plu1sd_p_3_d1_wt']  >0 , df[cog+'_plu1sd_p_3_d2_wt'] >0 , \
       df[cog+'_plu1sd_o_3_d_1_Coordin_wt']  >0 , df[cog+'_plu1sd_o_3_d_2_Guiding_wt'] >0 ],axis=0)
    df['index_'+cog+'_plu1sd_soc_d'] = df['index_'+cog+'_plu1sd_soc_d'].replace([np.inf, -np.inf], np.nan).fillna(0)
    
      
#4 
      
    df['index_norm'+cog+'_plu1sd_phy_a']=df['index_'+cog+'_plu1sd_phy_a']/np.max(df['index_'+cog+'_plu1sd_phy_a'],axis=0)
    df['index_norm'+cog+'_plu1sd_phy_b']=df['index_'+cog+'_plu1sd_phy_b']/np.max(df['index_'+cog+'_plu1sd_phy_b'],axis=0)


###############################################################################
#########Make matrices to analyse############################################# 

for cog in cogabs:
    df[cog+'n_sumindex']=np.sum(df[[col for col in df if (col.startswith('index_'+cog+'n_'))]],axis=1)
    df[cog+'n_countindex']=np.sum((df[[col for col in df if (col.startswith('index_'+cog+'n_'))]]>0),axis=1)
    df[cog+'n_avgindex']=df[cog+'n_sumindex']/df[cog+'n_countindex']
    df[cog+'_min1sd_sumindex']=np.sum(df[[col for col in df if (col.startswith('index_'+cog+'_min'))]],axis=1)
    df[cog+'_min1sd_countindex']=np.sum((df[[col for col in df if (col.startswith('index_'+cog+'_min'))]]>0),axis=1)
    df[cog+'_min1sd_avgindex']=df[cog+'_min1sd_sumindex']/df[cog+'_min1sd_countindex']
    df[cog+'_plu1sd_sumindex']=np.sum(df[[col for col in df if (col.startswith('index_'+cog+'_plu'))]],axis=1)
    df[cog+'_plu1sd_countindex']=np.sum((df[[col for col in df if (col.startswith('index_'+cog+'_plu'))]]>0),axis=1)
    df[cog+'_plu1sd_avgindex']=df[cog+'_plu1sd_sumindex']/df[cog+'_plu1sd_countindex']


#########load ISCO 08 strings and merge to dataframe

isco08 = pd.read_csv('struct08.csv')

##get rid of multiple armed forces codes
isco08.drop(isco08[ isco08.index == 610 ].index,inplace=True)
isco08.drop(isco08[ isco08.index == 611 ].index,inplace=True)
isco08.drop(isco08[ isco08.index == 613 ].index,inplace=True)
isco08.drop(isco08[ isco08.index == 614 ].index,inplace=True)
isco08.drop(isco08[ isco08.index == 616 ].index,inplace=True)
isco08.drop(isco08[ isco08.index == 617 ].index,inplace=True)

isco08.ISCO_08_Code = isco08.ISCO_08_Code.astype(float)
isco08 = isco08.set_index('ISCO_08_Code')


## adjust isco digit coding
df.isco.replace(20,2,inplace=True)
df.isco.replace(30,3,inplace=True)
df.isco.replace(40,4,inplace=True)
df.isco.replace(70,7,inplace=True)
df.isco.replace(80,8,inplace=True)
df.isco.replace(90,9,inplace=True)
df.isco.replace(230,23,inplace=True)
df.isco.replace(250,25,inplace=True)
df.isco.replace(410,41,inplace=True)
df.isco.replace(510,51,inplace=True)
df.isco.replace(520,52,inplace=True)
df.isco.replace(530,53,inplace=True)
df.isco.replace(710,71,inplace=True)
df.isco.replace(720,72,inplace=True)
df.isco.replace(740,74,inplace=True)
df.isco.replace(750,75,inplace=True)
df.isco.replace(810,81,inplace=True)
df.isco.replace(820,82,inplace=True)
df.isco.replace(830,83,inplace=True)
df.isco.replace(910,91,inplace=True)
df.isco.replace(930,93,inplace=True)


df['iscostr']=(isco08.Title.loc[df.isco].values)

#df.to_csv('piaacewcsonet_isco08_cogabs.csv')

#################Plot data#####################################################

cols = ['isco','ecn_sumindex','msn_sumindex','mcn_sumindex','con_sumindex','cen_sumindex','pan_sumindex', \
        'mpn_sumindex','asn_sumindex','cln_sumindex','qln_sumindex', \
        'sin_sumindex','nvn_sumindex','vpn_sumindex','apn_sumindex']
cogabn_sumindex=df[cols]
cogabn_sumindex = cogabn_sumindex.set_index('isco')

cols = ['isco','ecn_avgindex','msn_avgindex','mcn_avgindex','con_avgindex','cen_avgindex','pan_avgindex', \
        'mpn_avgindex','asn_avgindex','cln_avgindex','qln_avgindex', \
        'sin_avgindex','nvn_avgindex','vpn_avgindex','apn_avgindex']
cogabn_avgindex=df[cols]
cogabn_avgindex = cogabn_avgindex.set_index('isco')

cogabn_sumindreltoisco=cogabn_sumindex.div(cogabn_sumindex.sum(axis=1),axis=0)
cogabn_avgindreltoisco=cogabn_avgindex.div(cogabn_avgindex.sum(axis=1),axis=0)


cols = ['isco','ec_min1sd_sumindex','ms_min1sd_sumindex','mc_min1sd_sumindex','co_min1sd_sumindex','ce_min1sd_sumindex','pa_min1sd_sumindex', \
        'mp_min1sd_sumindex','as_min1sd_sumindex','cl_min1sd_sumindex','ql_min1sd_sumindex', \
        'si_min1sd_sumindex','nv_min1sd_sumindex','vp_min1sd_sumindex','ap_min1sd_sumindex']
cogab_min1sd_sumindex=df[cols]
cogab_min1sd_sumindex = cogab_min1sd_sumindex.set_index('isco')

cols = ['isco','ec_min1sd_avgindex','ms_min1sd_avgindex','mc_min1sd_avgindex','co_min1sd_avgindex','ce_min1sd_avgindex','pa_min1sd_avgindex', \
        'mp_min1sd_avgindex','as_min1sd_avgindex','cl_min1sd_avgindex','ql_min1sd_avgindex', \
        'si_min1sd_avgindex','nv_min1sd_avgindex','vp_min1sd_avgindex','ap_min1sd_avgindex']
cogab_min1sd_avgindex=df[cols]
cogab_min1sd_avgindex = cogab_min1sd_avgindex.set_index('isco')

cogab_min1sd_sumindreltoisco=cogab_min1sd_sumindex.div(cogab_min1sd_sumindex.sum(axis=1),axis=0)
cogab_min1sd_sumindreltoisco2=cogab_min1sd_sumindex.div(cogabn_sumindex.sum(axis=1),axis=0)
cogab_min1sd_avgindreltoisco=cogab_min1sd_avgindex.div(cogab_min1sd_avgindex.sum(axis=1),axis=0)

cols = ['isco','ec_plu1sd_sumindex','ms_plu1sd_sumindex','mc_plu1sd_sumindex','co_plu1sd_sumindex','ce_plu1sd_sumindex','pa_plu1sd_sumindex', \
        'mp_plu1sd_sumindex','as_plu1sd_sumindex','cl_plu1sd_sumindex','ql_plu1sd_sumindex', \
        'si_plu1sd_sumindex','nv_plu1sd_sumindex','vp_plu1sd_sumindex','ap_plu1sd_sumindex']
cogab_plu1sd_sumindex=df[cols]
cogab_plu1sd_sumindex = cogab_plu1sd_sumindex.set_index('isco')

cols = ['isco','ec_plu1sd_avgindex','ms_plu1sd_avgindex','mc_plu1sd_avgindex','co_plu1sd_avgindex','ce_plu1sd_avgindex','pa_plu1sd_avgindex', \
        'mp_plu1sd_avgindex','as_plu1sd_avgindex','cl_plu1sd_avgindex','ql_plu1sd_avgindex', \
        'si_plu1sd_avgindex','nv_plu1sd_avgindex','vp_plu1sd_avgindex','ap_plu1sd_avgindex']
cogab_plu1sd_avgindex=df[cols]
cogab_plu1sd_avgindex = cogab_plu1sd_avgindex.set_index('isco')

cogab_plu1sd_sumindreltoisco=cogab_plu1sd_sumindex.div(cogab_plu1sd_sumindex.sum(axis=1),axis=0)
cogab_plu1sd_sumindreltoisco2=cogab_plu1sd_sumindex.div(cogabn_sumindex.sum(axis=1),axis=0)
cogab_plu1sd_avgindreltoisco=cogab_plu1sd_avgindex.div(cogab_plu1sd_avgindex.sum(axis=1),axis=0)


##################################################################################

df = df.set_index('isco')

#######content1: selected occupations



iscosel=[[911, 513, 522], [711, 532, 833],  [234,221,411]]
df['iscostr'].replace('Building frame and related trades workers', \
  'Building and related trades in construction',inplace=True)
df['iscoshortstr'] = df['iscostr'].replace('General office clerks', 'Office Clerks')
df['iscoshortstr'].replace('Domestic, hotel and office cleaners and helpers', 'Cleaners & helpers',inplace=True)
df['iscoshortstr'].replace('Personal care workers in health services','Care workers',inplace=True)
df['iscoshortstr'].replace('Primary school and early childhood teachers','Teachers',inplace=True )
df['iscoshortstr'].replace('Heavy truck and bus drivers','Drivers',inplace=True )
df['iscoshortstr'].replace('Waiters and bartenders','Waiters & bartenders',inplace=True )
df['iscoshortstr'].replace('Building and related trades in construction','Construction workers',inplace=True )




iscoselstr=df['iscostr'].loc[list(chain.from_iterable(iscosel))].values.reshape(3,3)
iscoselshortstr=df['iscoshortstr'].loc[list(chain.from_iterable(iscosel))].values.reshape(3,3)

###############################################################################
####################Distribution of ability-specific relevance################

cogabn_sumindrel2 = pd.melt(cogabn_sumindreltoisco.reset_index(), id_vars=('isco'),value_vars=list(cogabn_sumindreltoisco))
cogabn_sumindrel2['iscostr']=mlb.repmat(df.iscostr,1,14).transpose()
for cog in cogabs:
    cogabn_sumindrel2['variable']=cogabn_sumindrel2['variable'].str.replace(cog+'n_sumindex',cog.upper())


##style
fontP = FontProperties()
fontP.set_size('small')
plt.figure(figsize = (15,8))

sns.set(style="whitegrid", font_scale = 2)
sns.violinplot(x='variable',y='value',data=cogabn_sumindrel2,scale="count", \
                    inner="box")

plt.axvline(x=3.5, ls='--',color='orange')
plt.axvline(x=9.5, ls='--',color='orange')
 
# Add titles
plt.xlabel("Cognitive ability")
plt.ylabel("Score")
plt.text(2.0, 0.188, 'People', ha='right', va='center')
plt.text(6.8, 0.188, 'Ideas', ha='right', va='center')
plt.text(12.2, 0.188, 'Things', ha='right', va='center')


plt.savefig("figure_5",bbox_inches='tight')


#######################relevance scores for selected occupations
# style
fontP = FontProperties()
fontP.set_size('small')
plt.style.use('seaborn-darkgrid')
plt.figure(figsize = (15,10))
palette = plt.get_cmap('tab10')
sns.set(style="whitegrid", font_scale = 1)

num=0
for i in list(chain.from_iterable(iscosel)):
    
    
    # Find the right spot on the plot
    plt.subplot(3,3, num+1)
    
    # plot every groups, but discreet
    for v in list(chain.from_iterable(iscosel)):
        plt.plot(Cogabs, cogabn_sumindreltoisco.loc[v,:], marker='', color='black', linewidth=0.8, alpha=0.2)

    # Plot the lineplot
    plt.plot(Cogabs, cogabn_sumindreltoisco.loc[i,:], marker='D', color=palette(num), \
             linewidth=0, alpha=1, label = list(chain.from_iterable(iscoselstr))[num])
    plt.plot(Cogabs, cogab_min1sd_sumindreltoisco2.loc[i,:], marker='_', color=palette(num), \
             linewidth=0, alpha=1, label = list(chain.from_iterable(iscoselstr))[num])
    plt.plot(Cogabs, cogab_plu1sd_sumindreltoisco2.loc[i,:], marker='_', color=palette(num), \
             linewidth=0, alpha=1, label = list(chain.from_iterable(iscoselstr))[num])
    
    # Same limits for every subgraph
    plt.ylim(0,0.19)
    plt.grid(color='black', linestyle='-', linewidth=0.3, alpha=0.3)
    
    ##Add vertical lines
    plt.axvline(x=3.5, ls='--',color='orange',linewidth=1,)
    plt.axvline(x=9.5, ls='--',color='orange',linewidth=1,)
    
    # Not ticks everywhere
    if num not in [1,4,7] :
        plt.tick_params(labelleft='off')
        
    ##background color
    ax = plt.gca()
    ax.set_facecolor('white')
 
    # Add title
    plt.title(list(chain.from_iterable(iscoselstr))[num], loc='left', \
              fontsize=9, fontweight=0, color=palette(num) )
    num+=1
    
# Add titles
plt.text(-8.0, -0.05, 'Cognitive abilities', ha='right', va='center')
plt.text(-35.0, .35, 'Score', ha='right', va='center', rotation='vertical')
plt.text(-32.0, 0.64, 'People', ha='right', va='center')
plt.text(-27.3, 0.64, 'Ideas', ha='right', va='center')
plt.text(-22.0, 0.64, 'Things', ha='right', va='center')

plt.text(-15.0, 0.64, 'People', ha='right', va='center')
plt.text(-9.9, 0.64, 'Ideas', ha='right', va='center')
plt.text(-4.50, 0.64, 'Things', ha='right', va='center')

plt.text(2.0, 0.64, 'People', ha='right', va='center')
plt.text(7.1, 0.64, 'Ideas', ha='right', va='center')
plt.text(12.5, 0.64, 'Things', ha='right', va='center')

plt.text(-32.0, 0.18, 'People', ha='right', va='center')
plt.text(-27.3, 0.18, 'Ideas', ha='right', va='center')
plt.text(-22.0, 0.18, 'Things', ha='right', va='center')

plt.text(-15.0, 0.18, 'People', ha='right', va='center')
plt.text(-9.9, 0.18, 'Ideas', ha='right', va='center')
plt.text(-4.50, 0.18, 'Things', ha='right', va='center')

plt.text(2.0, 0.18, 'People', ha='right', va='center')
plt.text(7.1, 0.18, 'Ideas', ha='right', va='center')
plt.text(12.5, 0.18, 'Things', ha='right', va='center')


plt.savefig("figure_6",bbox_inches='tight')

######################################
###########Compute AI Impact score
######################################

##load data on RnD relevance of cogabs
df_ai_raw = pd.read_csv('interestAIbench_0819.csv')
del df_ai_raw['Unnamed: 0']

times=list(range(2008,2020))

ai_scores = {}
ai_scores['numdocs_year'] = {}
ai_scores['by_cogab'] ={}
for cog in Cogabs:
    ai_scores['by_cogab'][cog]={}
    for time in times:
        ai_scores['numdocs_year'][time] = np.sum(df_ai_raw[str(time)])
        ai_scores['by_cogab'][cog][time]={}
        ai_scores['by_cogab'][cog][time] = np.sum(df_ai_raw[str(time)].loc[df_ai_raw[cog]==1])
arr=[]
for cog in Cogabs:
    arr.append(np.array(list(ai_scores['by_cogab'][cog].values()))/np.array(list(ai_scores['numdocs_year'].values())))
arr=np.array(arr)
df_aiscore=pd.DataFrame(arr, columns=times, index=Cogabs)     

df_aiscore['mean']=df_aiscore.mean(axis=1)


times.append('mean')

impactscore = {}
impactscore['by_cogab']={}
impactscore['by_cogab']['sumindrel']={}
impactscore['by_cogab']['minsumindrel']={}
impactscore['by_cogab']['plusumindrel']={}


impactscore['Isco']={}
impactscore['Isco']['sumindrel']={}
impactscore['Isco']['minsumindrel']={}
impactscore['Isco']['plusumindrel']={}

for time in times:
    impactscore['by_cogab']['sumindrel'][time]=cogabn_sumindreltoisco.copy()
    impactscore['by_cogab']['minsumindrel'][time]=cogab_min1sd_sumindreltoisco.copy()
    impactscore['by_cogab']['plusumindrel'][time]=cogab_plu1sd_sumindreltoisco.copy()
    
    for cog in cogabs:
        impactscore['by_cogab']['sumindrel'][time].rename(columns={cog+'n_sumindex':cog},inplace=True)
        impactscore['by_cogab']['minsumindrel'][time].rename(columns={cog+'_min1sd_sumindex':cog},inplace=True)
        impactscore['by_cogab']['plusumindrel'][time].rename(columns={cog+'_plu1sd_sumindex':cog},inplace=True)
        
        impactscore['by_cogab']['sumindrel'][time][cog]=impactscore['by_cogab']['sumindrel'][time][cog]*df_aiscore.loc[cog.upper(),time]
        impactscore['by_cogab']['minsumindrel'][time][cog]=impactscore['by_cogab']['minsumindrel'][time][cog]*df_aiscore.loc[cog.upper(),time]
        impactscore['by_cogab']['plusumindrel'][time][cog]=impactscore['by_cogab']['plusumindrel'][time][cog]*df_aiscore.loc[cog.upper(),time]

    impactscore['by_cogab']['sumindrel'][time]['total']=impactscore['by_cogab']['sumindrel'][time].sum(axis=1)   
    impactscore['by_cogab']['sumindrel'][time]['total_pct']=impactscore['by_cogab']['sumindrel'][time].total.rank(pct = True)
    impactscore['by_cogab']['minsumindrel'][time]['total']=impactscore['by_cogab']['minsumindrel'][time].sum(axis=1)   
    impactscore['by_cogab']['minsumindrel'][time]['total_pct']=impactscore['by_cogab']['minsumindrel'][time].total.rank(pct = True)    
    impactscore['by_cogab']['plusumindrel'][time]['total']=impactscore['by_cogab']['plusumindrel'][time].sum(axis=1)   
    impactscore['by_cogab']['plusumindrel'][time]['total_pct']=impactscore['by_cogab']['plusumindrel'][time].total.rank(pct = True)    

            
    impactscore['Isco']['sumindrel'][time] = pd.DataFrame(pd.concat([df.iscostr,impactscore['by_cogab']['sumindrel'][time].total_pct],axis=1))
    impactscore['Isco']['sumindrel'][time] = impactscore['Isco']['sumindrel'][time].sort_values(by=['total_pct'])
    impactscore['Isco']['minsumindrel'][time] = pd.DataFrame(pd.concat([df.iscostr,impactscore['by_cogab']['minsumindrel'][time].total_pct],axis=1))
    impactscore['Isco']['minsumindrel'][time] = impactscore['Isco']['minsumindrel'][time].sort_values(by=['total_pct'])    
    impactscore['Isco']['plusumindrel'][time] = pd.DataFrame(pd.concat([df.iscostr,impactscore['by_cogab']['plusumindrel'][time].total_pct],axis=1))
    impactscore['Isco']['plusumindrel'][time] = impactscore['Isco']['plusumindrel'][time].sort_values(by=['total_pct'])    

    
###############################################################################
################2018 AI impact#################################################
###############################################################################


###############Bar plot of AI impact scores####################################

cogtype=['People','Ideas','Things']
years=range(2008,2020)
N=9
ind = np.arange(N) 

impactscore['by_cogab']['sumindrel_group']={}
for time in times:
    impactscore['by_cogab']['sumindrel_group'][time]={}
    impactscore['by_cogab']['sumindrel_group'][time]['ec_co']=np.sum(impactscore['by_cogab']['sumindrel'][time].iloc[:,:4],1)
    impactscore['by_cogab']['sumindrel_group'][time]['ce_cl']=np.sum(impactscore['by_cogab']['sumindrel'][time].iloc[:,4:10],1)
    impactscore['by_cogab']['sumindrel_group'][time]['si_ap']=np.sum(impactscore['by_cogab']['sumindrel'][time].iloc[:,10:14],1)

cog_group_score={}
for time in times:
    cog_group_score[time]=pd.DataFrame([])
    cog_group_score[time]['people'] = impactscore['by_cogab']['sumindrel_group'][time]['ec_co']
    cog_group_score[time]['ideas'] = impactscore['by_cogab']['sumindrel_group'][time]['ce_cl']
    cog_group_score[time]['things'] = impactscore['by_cogab']['sumindrel_group'][time]['si_ap']

df1=impactscore['by_cogab']['sumindrel'][2018].loc[list(chain.from_iterable(iscosel))].iloc[:,:14]
df2=cog_group_score[2018].loc[list(chain.from_iterable(iscosel))]


##bar chart for 3 groups of cognitive abilities
fig, ax =plt.subplots(1,2)
g1 = cog_group_score[2018].loc[list(chain.from_iterable(iscosel))].plot(kind='bar', \
           stacked=True, figsize=(10,10),edgecolor = "none", ax=ax[0])

plt.setp(ax, xlabel = " ", ylabel = "AI exposure score", xticks=ind, xticklabels=list(chain.from_iterable(iscoselshortstr)))

fontP.set_size('small')
g1.legend(cogtype,prop=fontP, \
    loc='upper center', bbox_to_anchor=(0.3, -0.15),ncol=3)

g1.set_xticklabels(g1.get_xticklabels(), rotation=45,horizontalalignment='right') 

##bar chart for all 14 cognitive abilities    


g1 = impactscore['by_cogab']['sumindrel'][2018].loc[list(chain.from_iterable(iscosel))].iloc[:,:14].plot(kind='bar', \
           stacked=True, figsize=(10,10),edgecolor = "none", ax=ax[1])    
plt.setp(ax,  xlabel = " ", ylabel = " ", xticks=ind, xticklabels=list(chain.from_iterable(iscoselshortstr)))
fontP.set_size('small')
g1.legend(Cogabs,prop=fontP, \
    loc='upper center', bbox_to_anchor=(0.4, -0.15),ncol=5)

g1.set_xticklabels(g1.get_xticklabels(), rotation=45,horizontalalignment='right') 
    

plt.savefig("figure_8",bbox_inches='tight')


###Make table for all occupations
table_isco_score=df['iscostr'].to_frame(name='iscostr')
table_isco_score['pct_total']=impactscore['by_cogab']['sumindrel'][2018]['total_pct'].to_frame(name='total_pct')
table_isco_score['pct_total_min']=impactscore['by_cogab']['minsumindrel'][2018]['total_pct'].to_frame(name='total_pct_min')
table_isco_score['pct_total_plu']=impactscore['by_cogab']['plusumindrel'][2018]['total_pct'].to_frame(name='total_pct_plu')
table_isco_score.sort_values('pct_total',ascending=False,inplace=True)

print(table_isco_score.to_latex(float_format="%.3f"))

####correlate AI impact score and wage percentiles

df_wage = load_large_dta('isco3dwagerank.dta')
df_wage.sort_values(by=['isco3d'],inplace=True)
df_wage.set_index(df_wage['isco3d'],inplace = True)
impactscore['by_cogab']['sumindrel'][2018]['total_pct'].index = impactscore['by_cogab']['sumindrel'][2018]['total_pct'].index.astype('int64')

df_wage=df_wage.join(impactscore['by_cogab']['sumindrel'][2018]['total_pct'])

df_iscosel= pd.DataFrame({'iscosel': chain.from_iterable(iscosel), 'iscoselstr':chain.from_iterable(iscoselstr), 'iscoselshortstr':chain.from_iterable(iscoselshortstr)})
df_iscosel.set_index('iscosel',inplace=True)
df_wage=df_wage.join(df_iscosel)
df_wage.iscoselshortstr.replace(np.nan, '', regex=True,inplace=True)
df_wage.iscoselshortstr[215]='Electrotechnology engineers'
df_wage.iscoselshortstr[622]='Fishery workers & hunters'


fig, ax =plt.subplots(1,1)
g2 = sns.regplot(x="wp", y="total_pct", data=df_wage, line_kws={'color': 'red'})

for line in df_wage.index:
     g2.text(df_wage.wp[line]+0.2, df_wage.total_pct[line], df_wage.iscoselshortstr[line], horizontalalignment='left', size='medium', color='black', weight='semibold')
g2.set(xlabel='Wage percentile', ylabel='AI exposure score' )
g2.figure.set_size_inches(10,5)

g2.get_figure().savefig("figure_9",bbox_inches='tight')


##############################################################################
#########################Correlate with other scores##########################
##############################################################################

################## Felten, Raj and Seamus 2018#################################
## import AI score FRS
df_tmp = pd.read_excel('./Appendix_data_FRS2018_AI_occupation/Simulation_Data_Results_Occupations.xls')

#load crosswalk
df_cross = pd.read_excel('isco_soc_crosswalk.xlsx')
df_cross.drop(['ISCO-08 Title EN','2010 SOC Title'],axis=1,inplace=True)
df_cross['occ_code'] = df_cross['occ_code'].str.replace(' ', '')

##map isco4 to soc
tmp_value = set(df_cross['occ_code'].unique())
df_tmp['test']=df_tmp['occ_code'].map(lambda x : True if x in tmp_value  else False)

df_frs = pd.merge(df_tmp, df_cross, how='inner', on='occ_code')
del df_tmp
df_frs.rename(columns={"ISCO-08 Code": "isco4d"},inplace=True)

##take mean of avg_wtd_impact of all same isco4
df_frs['ai_impact4d'] = df_frs.isco4d.map(df_frs.groupby(['isco4d']).avg_wtd_impact.mean())
df_frs.drop_duplicates(subset=['isco4d','ai_impact4d'],inplace = True)

##convert isco4d to isco3d and average again
df_frs['isco3d']=np.floor(df_frs.isco4d/10)
df_frs['ai_impact_frs'] = df_frs.isco3d.map(df_frs.groupby(['isco3d']).ai_impact4d.mean())
df_frs.drop_duplicates(subset=['isco3d','ai_impact_frs'],inplace = True)
del df_frs['avg_wtd_impact']

df_frs.rename(columns={"isco3d": "isco"},inplace=True)
df_frs.set_index('isco',inplace=True)

df_frs = pd.merge(df_frs,impactscore['by_cogab']['sumindrel'][2018],left_index = True, right_index = True)

df_frs['ai_impact_frs_pct'] = df_frs['ai_impact_frs'].rank(pct = True)

df_frs['absdiff']=np.abs(df_frs['total_pct']-df_frs['ai_impact_frs_pct'])

##add selected occupation labels
df_frs=df_frs.join(df_iscosel)
df_frs.iscoselshortstr.replace(np.nan, '', regex=True,inplace=True)
df_frs.iscoselshortstr[215]='Engineers'
df_frs.iscoselshortstr[622]='Fishery workers & hunters'

##correlate the 2 scores
fig, ax = plt.subplots()
fontP = FontProperties()
fontP.set_size('small')
plt.style.use('seaborn-darkgrid')
palette = plt.get_cmap('tab20')
plt.figure(figsize = (5,5))
sns.set(style="whitegrid", font_scale = 1)

rho1 = stats.spearmanr(df_frs['total_pct'],df_frs['ai_impact_frs_pct'])
ax.scatter(df_frs["total_pct"], df_frs['ai_impact_frs_pct'])
ax.plot([0, 1], [0, 1], color = 'black', linewidth = 2)
for line in df_frs.index:
     ax.text(df_frs.total_pct[line], df_frs.ai_impact_frs_pct[line], df_frs.iscoselshortstr[line], horizontalalignment='left', size='small', color='black')
ax.set_xlim(-0.05, 1.05)
ax.set_ylim(-0.05, 1.05)
ax.set_xlabel('AI exposure score (pct.)')
ax.set_ylabel('AI score (pct.) FRS')
ax.text(1.04, -0.02, '\u03C1 = {:.3f} (p-val={:.3f})'.format(rho1[0],rho1[1]), ha='right', va='center')


fig.savefig("figure_10c",bbox_inches='tight')


################## Webb 2020#################################
## import AI score FRS
df_tmp = pd.read_excel('./scores_webb2020/exposure_by_soc4.xlsx')
df_tmp['occ_code'] = df_tmp['occ_code'].str.replace('\.00', '')
df_tmp['occ_code'] = df_tmp['occ_code'].str.replace('\.01', '')
df_tmp['occ_code'] = df_tmp['occ_code'].str.replace('\.02', '')
df_tmp['occ_code'] = df_tmp['occ_code'].str.replace('\.03', '')
df_tmp['occ_code'] = df_tmp['occ_code'].str.replace('\.04', '')
df_tmp['occ_code'] = df_tmp['occ_code'].str.replace('\.05', '')
df_tmp['occ_code'] = df_tmp['occ_code'].str.replace('\.06', '')
df_tmp['occ_code'] = df_tmp['occ_code'].str.replace('\.07', '')
df_tmp['occ_code'] = df_tmp['occ_code'].str.replace('\.08', '')
df_tmp['occ_code'] = df_tmp['occ_code'].str.replace('\.09', '')
df_tmp['occ_code'] = df_tmp['occ_code'].str.replace('\.10', '')
df_tmp['occ_code'] = df_tmp['occ_code'].str.replace('\.11', '')
df_tmp['occ_code'] = df_tmp['occ_code'].str.replace('\.12', '')

##map isco4 to soc
tmp_value = set(df_cross['occ_code'].unique())
df_tmp['test']=df_tmp['occ_code'].map(lambda x : True if x in tmp_value  else False)

df_webb = pd.merge(df_tmp, df_cross, how='inner', on='occ_code')
del df_tmp
df_webb.rename(columns={"ISCO-08 Code": "isco4d"},inplace=True)

##take mean of avg_wtd_impact of all same isco4
df_webb['ai_impact4d'] = df_webb.isco4d.map(df_webb.groupby(['isco4d']).ai_score.mean())
df_webb.drop_duplicates(subset=['isco4d','ai_impact4d'],inplace = True)

##convert isco4d to isco3d and average again
df_webb['isco3d']=np.floor(df_webb.isco4d/10)
df_webb['ai_impact_webb'] = df_webb.isco3d.map(df_webb.groupby(['isco3d']).ai_impact4d.mean())
df_webb.drop_duplicates(subset=['isco3d','ai_impact_webb'],inplace = True)

df_webb.rename(columns={"isco3d": "isco"},inplace=True)
df_webb.set_index('isco',inplace=True)

df_webb = pd.merge(df_webb,impactscore['by_cogab']['sumindrel'][2018],left_index = True, right_index = True)

df_webb['ai_impact_webb_pct'] = df_webb['ai_impact_webb'].rank(pct = True)

##add selected occupation labels
df_webb=df_webb.join(df_iscosel)
df_webb.iscoselshortstr.replace(np.nan, '', regex=True,inplace=True)
df_webb.iscoselshortstr[215]='Engineers'
df_webb.iscoselshortstr[622]='Fishery workers & hunters'
df_webb['absdiff']=np.abs(df_webb['total_pct']-df_webb['ai_impact_webb_pct'])


##correlate the 2 scores
fig, ax = plt.subplots()
fontP = FontProperties()
fontP.set_size('small')
plt.style.use('seaborn-darkgrid')
palette = plt.get_cmap('tab20')
plt.figure(figsize = (5,5))
sns.set(style="whitegrid", font_scale = 1)

rho1 = stats.spearmanr(df_webb['total_pct'],df_webb['ai_impact_webb_pct'])
ax.scatter(df_webb["total_pct"], df_webb['ai_impact_webb_pct'])
ax.plot([0, 1], [0, 1], color = 'black', linewidth = 2)
for line in df_webb.index:
     ax.text(df_webb.total_pct[line], df_webb.ai_impact_webb_pct[line], df_webb.iscoselshortstr[line], horizontalalignment='left', size='small', color='black')
ax.set_xlim(-0.05, 1.05)
ax.set_ylim(-0.05, 1.05)
ax.set_xlabel('AI exposure score (pct.)')
ax.set_ylabel('AI score (pct.) Webb')
ax.text(1.04, -0.02, '\u03C1 = {:.3f} (p-val={:.3f})'.format(rho1[0],rho1[1]), ha='right', va='center')

fig.savefig("figure_10b",bbox_inches='tight')

################## BRM 2018#################################
## import AI scoreBRM
df_tmp = pd.read_csv('./Appendix_data_BMR2018_AI_occupation/SML_score.csv')
df_tmp['occ_code'] = df_tmp['occ_code'].str.replace('\.00', '')
df_tmp['occ_code'] = df_tmp['occ_code'].str.replace('\.01', '')
df_tmp['occ_code'] = df_tmp['occ_code'].str.replace('\.02', '')
df_tmp['occ_code'] = df_tmp['occ_code'].str.replace('\.03', '')
df_tmp['occ_code'] = df_tmp['occ_code'].str.replace('\.04', '')
df_tmp['occ_code'] = df_tmp['occ_code'].str.replace('\.05', '')
df_tmp['occ_code'] = df_tmp['occ_code'].str.replace('\.06', '')
df_tmp['occ_code'] = df_tmp['occ_code'].str.replace('\.07', '')
df_tmp['occ_code'] = df_tmp['occ_code'].str.replace('\.08', '')
df_tmp['occ_code'] = df_tmp['occ_code'].str.replace('\.09', '')
df_tmp['occ_code'] = df_tmp['occ_code'].str.replace('\.10', '')
df_tmp['occ_code'] = df_tmp['occ_code'].str.replace('\.11', '')
df_tmp['occ_code'] = df_tmp['occ_code'].str.replace('\.12', '')


##map isco4 to soc
tmp_value = set(df_cross['occ_code'].unique())
df_tmp['test']=df_tmp['occ_code'].map(lambda x : True if x in tmp_value  else False)

df_BMR = pd.merge(df_tmp, df_cross, how='inner', on='occ_code')
del df_tmp
df_BMR.rename(columns={"ISCO-08 Code": "isco4d"},inplace=True)

##take mean of avg_wtd_impact of all same isco4
df_BMR['ai_impact4d'] = df_BMR.isco4d.map(df_BMR.groupby(['isco4d']).mSML.mean())
df_BMR.drop_duplicates(subset=['isco4d','ai_impact4d'],inplace = True)

##convert isco4d to isco3d and average again
df_BMR['isco3d']=np.floor(df_BMR.isco4d/10)
df_BMR['ai_impact_BMR'] = df_BMR.isco3d.map(df_BMR.groupby(['isco3d']).ai_impact4d.mean())
df_BMR.drop_duplicates(subset=['isco3d','ai_impact_BMR'],inplace = True)

df_BMR.rename(columns={"isco3d": "isco"},inplace=True)
df_BMR.set_index('isco',inplace=True)

df_BMR = pd.merge(df_BMR,impactscore['by_cogab']['sumindrel'][2018],left_index = True, right_index = True)

df_BMR['ai_impact_BMR_pct'] = df_BMR['ai_impact_BMR'].rank(pct = True)

##add selected occupation labels
df_BMR=df_BMR.join(df_iscosel)
df_BMR.iscoselshortstr.replace(np.nan, '', regex=True,inplace=True)
df_BMR.iscoselshortstr[215]='Engineers'
df_BMR.iscoselshortstr[622]='Fishery workers & hunters'

df_BMR['absdiff']=np.abs(df_BMR['total_pct']-df_BMR['ai_impact_BMR_pct'])

##correlate the 2 scores
fig, ax = plt.subplots()
fontP = FontProperties()
fontP.set_size('small')
plt.style.use('seaborn-darkgrid')
palette = plt.get_cmap('tab20')
plt.figure(figsize = (5,5))
sns.set(style="whitegrid", font_scale = 1)

rho1 = stats.spearmanr(df_BMR['total_pct'],df_BMR['ai_impact_BMR_pct'])
ax.scatter(df_BMR["total_pct"], df_BMR['ai_impact_BMR_pct'])
ax.plot([0, 1], [0, 1], color = 'black', linewidth = 2)
for line in df_BMR.index:
     ax.text(df_BMR.total_pct[line], df_BMR.ai_impact_BMR_pct[line], df_BMR.iscoselshortstr[line], horizontalalignment='left', size='small', color='black')
ax.set_xlim(-0.05, 1.05)
ax.set_ylim(-0.05, 1.05)
ax.set_xlabel('AI exposure score (pct.)')
ax.set_ylabel('AI score (pct.) BMR')
ax.text(1.04, -0.02, '\u03C1 = {:.3f} (p-val={:.3f})'.format(rho1[0],rho1[1]), ha='right', va='center')

fig.savefig("figure_10a",bbox_inches='tight')





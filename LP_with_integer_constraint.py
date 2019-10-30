"""
Code to identify the best year to select issuers for audit

Created: 10/29/2019 , Pratik Sule

"""

import os
import pandas as pd
from pulp import *

#input file directory

os.chdir("C://Old Laptop//My Docs//CMS//2019//Audit")

input_file = 'Test_ip.csv'

input_data = pd.read_csv(input_file)
#Issuers to select per year

no_issuers = 2

#formulate the LPP problem

prob = LpProblem("Issuer_Audit", LpMaximize)

hios_list = list(input_data['HIOS ID'])

by2017_score = dict(zip(hios_list,input_data['BY2017']))

by2018_score = dict(zip(hios_list,input_data['BY2018']))

by2019_score = dict(zip(hios_list,input_data['BY2019']))

hios_select_2017 = LpVariable.dicts("risk2017",hios_list, 0, 1, cat='Integer')
hios_select_2018 = LpVariable.dicts("risk2018",hios_list, 0, 1, cat='Integer')
hios_select_2019 = LpVariable.dicts("risk2019",hios_list, 0, 1, cat='Integer')

#Add the function to be maximized

prob += lpSum([(by2017_score[i]*hios_select_2017[i] \
                + by2018_score[i]*hios_select_2018[i]\
                + by2019_score[i]*hios_select_2019[i]) for i in hios_list])

#Add constraints

#Number of issuers to be selected for each cycle
prob += lpSum([hios_select_2017[i] for i in hios_list]) == no_issuers
prob += lpSum([hios_select_2018[i] for i in hios_list]) == no_issuers
prob += lpSum([hios_select_2019[i] for i in hios_list]) == no_issuers

#No issuer to be selected more than once across all 3 years
for i in hios_list:
    
    prob += hios_select_2017[i] + hios_select_2018[i] + hios_select_2019[i] <=1

prob.solve()

#getting output variables

for v in prob.variables():
    if v.varValue>0:
        print(v.name, "=", v.varValue)


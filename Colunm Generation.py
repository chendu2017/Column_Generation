# -*- coding: utf-8 -*-
"""
Created on Wed May  2 18:32:20 2018

@author: chend
"""

from gurobipy import gurobipy as grb
import numpy as np
import time

# length of one steel tube
length = 50

# number of material every buyer need
num_demand = []

# length that every buyer need
L = []

for amount,l in zip(demand['Amount'].values,demand['Length'].values):
    num_demand.append(int(amount))
    L.append(l)
#
buyer = range(len(num_demand))
max_material = range(sum(num_demand))


#General model

#estabilish model 
m = grb.Model('model1')
m.modelSense = grb.GRB.MINIMIZE
m.setParam('OutputFlag',0)

# addvars
X = m.addVars(max_material,buyer,vtype = grb.GRB.INTEGER,ub=1,lb=0,obj = 0)
Y = m.addVars(max_material,vtype = grb.GRB.INTEGER,ub=1,lb=0,obj = 1)

#add constraints

#1rt : aggregated cutted length should less than total length
for i in max_material:
    expr = 0
    for j in buyer:
        expr = X[i,j]*L[j] + expr 
    m.addConstr(expr <= Y[i]*length)
    del expr
    
#2nd
for j in buyer:
    expr = 0
    for i in max_material:
        expr = X[i,j] + expr
    m.addConstr(expr >= num_demand[j])
    del expr
#3rd
for i in max_material:
    expr = 0
    expr = Y[i] + expr
m.addConstr(expr <= sum(num_demand))

m.update()
#m.optimize()
'''
num_sum = 0
for i in max_material:
    num_sum = Y[i].x+ num_sum
'''
#print('time for MIP:%.4f' %m.Runtime) # == 15.31S 当有20个客户时,ObjVal=137
relaxedModel = m.relax()
relaxedModel.optimize()
print('time for CA:%.4f' %relaxedModel.Runtime)
print('CA: %.4f' %relaxedModel.ObjVal)





'''
#Colunm Generation
cg = grb.Model('cg')
cg.modelSense = grb.GRB.MINIMIZE
cg.setParam('OutputFlag',0) 
#add variables
M = cg.addVars(range(len(L)),vtype=grb.GRB.CONTINUOUS,obj=[1]*len(L))

#Matrix A
#at the very begginning, we suppose that one tube can only 
#satisfy one customer's one demand
cut_type = len(L)
A = np.eye(cut_type)

#add Constraints
constraints = 0
for i in range(cut_type):
    constraints = A.transpose()[i]*M[i] + constraints
cg.addConstrs(constraints[i] >= num_demand[i] for i in range(cut_type)) 

while 1:
    #solve the initial problem
    cg.optimize()

    #simplex multiplier Y
    multiplier = cg.Pi

    # try to find out the max theta
    #and corresponding colunm is the one to be inserted
    sub = grb.Model('sub')
    sub.modelSense = grb.GRB.MINIMIZE
    sub.setParam('OutputFlag',0)
    
    #add variables
    a = sub.addVars(range(len(L)),vtype=grb.GRB.CONTINUOUS)
    
    #set objective function
    expr = 0
    for i in range(len(L)):
        expr = expr + multiplier[i]*a[i]
    sub.setObjective(1-expr)
    del expr
    
    #add submodel's Constraints
    expr = 0
    for i in range(len(L)):
        expr = expr + a[i]*L[i]
    sub.addConstr(expr <= length)
    del expr
    
    #solve submodel
    sub.optimize()
    print(sub.ObjVal)
    
    #if submodel's objval>=0,means all theta >= 0 ,stop
    #whether, add one column 'a' & one new variable to primal model
    if sub.ObjVal >= -0.001:
        break
    else:
        #delete all constraints
        cg.remove(cg.getConstrs())
        
        #new colunm 
        new_colunm = [0]*len(a)
        for i in range(len(a)):
            new_colunm[i] = a[i].x 
         
        #new variable
        cut_type = cut_type + 1
        cg.addVar(vtype=grb.GRB.CONTINUOUS,obj=1) 
        cg.update()
        
        #Add new whole new constraints
        constraints = constraints + np.array(new_colunm)*cg.getVars()[-1]
        cg.addConstrs(constraints[i] >= num_demand[i] for i in range(len(L)))
        cg.update()
'''
    

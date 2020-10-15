# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 11:05:33 2020

@author: mfirat
"""

import gurobipy as grb
import pandas as pd
import time
from ProjectschedulingLibrary import Project,Employee,ConstructDataStructure,SolveLPMOdel

#123

###############################################################################
def Question(Projects,Employees,problem_name,insid,timelimit):
    
    print('--------------------------------------------------------------')
 
    LPModel = grb.Model(problem_name+str(insid)+"_LP")   
    LPModel.modelSense = grb.GRB.MAXIMIZE
    print('LP Solver timelimit:',timelimit)
    
    #  Creating decision variables..
        
 
    # employee busy vars z_{e,t} 
    # iterate employees and use for each emplpoyee TimeSet
  
    
    # assignvars x_{e,p}, project start vars theta_{p,t}, and lambda var \lambda_{p,p'}
     
    
    
    # Creating decision variables.. 
     
    LPModel.update()
        
    # Construct constraints 
        
    # constrains (2.2):
          
    # constraints (2.3):  
    
    # constraints (2.4):  

    # constraints (2.5): 
   
    # constraints (2.6):
 
    # constraints (2.7):
             
    # constraints (2.8):
    
    # constraints (2.9):
    
    # constraints (2.10):
    
    # constraints (2.11):
                                    
    # Construct constraints
    
    
    
    #LPModel.write(problem_name+str(insid)+'.lp')
    print('--------------------------------------------------------------')
    
   
    return Projects,Employees,LPModel
####################################################################################

# problem_name = "ProjectScheduling"  
# timelimit = 60

# instances = [1]

# print('--> 1BK50 LP Assignment Template<--')
# print('--> Important: Uncomment these lines to start working!',problem_name)

# for insid in instances:          
#     print('Problem instance: ',insid)       
#     Projects,Employees = ConstructDataStructure(problem_name,insid)   
#     Projects,Employees,LPModel = Question(Projects,Employees,problem_name,insid,timelimit)  
#     LPModel,Projects,Employees,feedback,fgrade,varscore = SolveLPMOdel(LPModel,Projects,Employees,timelimit,insid)
 
#     for feed in feedback:
#         print(feed)
      
# print('--> Important: Submit your file by making it back commented!')




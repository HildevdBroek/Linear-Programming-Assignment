# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 11:05:33 2020

@author: mfirat
"""

import gurobipy as grb
import pandas as pd
import time
from ProjectschedulingLibrary import Project,Employee,ConstructDataStructure,SolveLPMOdel

###############################################################################
def Question(Projects,Employees,problem_name,insid,timelimit):
    
    print('--------------------------------------------------------------')
 
    LPModel = grb.Model(problem_name+str(insid)+"_LP")   
    LPModel.modelSense = grb.GRB.MAXIMIZE
    print('LP Solver timelimit:',timelimit)
    

    # employee busy vars z_{e,t} 
    # iterate employees and use for each emplpoyee TimeSet
    # Employee busy/idle times The binary variable ze,t indicates that employee e is busy at time unit t for t = 1, 2, . . . , ∣T∣.
    # ze,t binary variable indicating that employee e ∈ E is busy at time t ∈ T, employee.getBusyVars()
    
    TimeSet = set(range(len(Employees[0].getAvailability()))) 
    for emp in Employees:
       Employeeavailablevars = LPModel.addVars(TimeSet, vtype=grb.GRB.BINARY, name="z_"+str(emp.getID()))

    emp.setBusyVars(Employeeavailablevars.values())
    
    # assignvars x_{e,p}, project start vars theta_{p,t}, and lambda var \lambda_{p,p'}
    #xe,p assignment variable of employee e ∈ E to project p ∈ P project.getAssignmentVars()
    Projectslist = set(range(0, len(insid.getProjects())))
    
    for Project in insid.getProject():
        vname="X_"+str(Project.getID())
        #place.setOpeningvar(LPModel.addVar(obj = place.getCost(), vtype=grb.GRB.BINARY,name = vname))
        #klopt deze?        
        Project.setExecVar(LPModel.addVar( vtype=grb.GRB.BINARY,name = vname))
       
        
    for emp in insid.getEmployee():
        #skills van employee checken met de skillsrequirements van project
        Employeeprojectvars = LPModel.addVars(Projectslist.obj = [(emp.getSkills(),Proj.Skillsrequirements()) for Proj in insid.getProj()], vtype=grb.GRB.BINARY, name="x_"+str(emp.getID()))
        #SkillSet = set(range(len(Employees[0].getSkills())))
        Emp.getEmployeeprojectVars(Employeeproject.values())
     #θp,t indicates that project p start in time t project.getStartVars()
     #Project starts We consider every time unit as potential for a project start and define the binary variable θp,t indicating that project p starts at time t.   
    
    #λp,p′ indicates that projects p and p’ have overlap in time p, p′ ∈ P project.getLambdaVars()
    
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




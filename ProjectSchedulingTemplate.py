# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 11:05:33 2020

@author: mfirat
"""

import gurobipy as grb
import pandas as pd
import time
from ProjectschedulingLibrary import Project,Employee,ConstructDataStructure, SolveLPMOdel

###############################################################################
def Question(Projects,Employees,problem_name,insid,timelimit):

    print('--------------------------------------------------------------')
    LPModel = grb.Model(problem_name+str(insid)+"_LP")   
    LPModel.modelSense = grb.GRB.MAXIMIZE
    print('LP Solver timelimit:',timelimit)

# employee busy vars z_{e,t} 
#iterate employees and use for each emplpoyee TimeSet Employee busy/idle times The binary variable ze,t indicates that employee e is busy at time unit t  employee.getBusyVars()
    
    for emp in Employees:
        TimeSetEmp = list(range(len(emp.getAvailability())))
        vname = "z_" + str(emp.getID())
        Busy = LPModel.addVars(TimeSetEmp, vtype=grb.GRB.BINARY, name = vname)
        emp.setBusyVars(Busy.values())
        #print("Z works")
    
#λp,p′ indicates that projects p and p’ have overlap in time p, p′ ∈ P project.getLambdaVars()

    for Project in Projects:
        OtherProjs = list(range(Project.getID()+1, len(Projects)))
        lname = "lambda_"+str(Project.getID())
        lambdavars = LPModel.addVars(OtherProjs,vtype=grb.GRB.BINARY, name=lname)
        Project.setLambdaVars(lambdavars.values())    
        #print("lambda works")
    
#θp,t indicates that project p start in time t project.getStartVars()
#Project starts We consider every time unit as potential for a project start and define the binary variable θp,t indicating that project p starts at time t.   

    for Project in Projects:
        TimeSetTheta = list(range(len(Employees[0].getAvailability())))
        Tname = "Theta_"+str(Project.getID())
        Theta = LPModel.addVars(TimeSetTheta, obj=Project.getWeight(), vtype=grb.GRB.BINARY, name=Tname)
        Project.setStartVars(Theta.values())      
        #print("Theta works")               

# assignvars x_{e,p}, project start vars theta_{p,t}, and lambda var \lambda_{p,p'}
#xe,p assignment variable of employee e ∈ E to project p ∈ P project.getAssignmentVars()      

    for Project in Projects:
        pname = "X_"+str(Project.getID())
        EmployeeProject = LPModel.addVars((list(range(len(Employees)))), vtype=grb.GRB.BINARY, name=pname)
        Project.setAssignmentVars(EmployeeProject.values())
        #print("X works")  
     
    LPModel.update()
    return Projects, Employees, LPModel
        
    # Construct constraints 
        

    # constrains (2.2): - Hilde
    #LPModel.addConstr((emp.getAvailability()[emp]*emp.setBusyVars()[emp] for emp in list(range(len(emp.getAvailability())))) <= emp.getAvailability(), 'A_'+str(emp.getID()))
    Aname = 'A_'+str(emp.getID())
    LPModel.addConstr(((emp.getBusyVars() <= emp.getAvailability()) for emp in Employees), name = Aname)
    # constraints (2.3):  - Nicole

    # constraints (2.4):  - Nicole

    # constraints (2.5):  - Nicole
   
    # constraints (2.6): - Hilde
 
    # constraints (2.7):  - Nicole
             
    # constraints (2.8):   - Hilde
    
    # constraints (2.9):  - Nicole
        #was een probeersel van eerdere decision variabelen:
                #for emp in Employees:
        #Employeesskills = list(range(len(emp.getSkills())))
        #print ("employeeskills")
                #skills = list(range(len(Project.getSkillRequirements())))
                   
        #intersect = len(intersection(skills, Employeesskills))
    # constraints (2.10):  - Hilde
    
    # constraints (2.11):  - Nicole
                                    
    # Construct constraints
    
    
    
    #LPModel.write(problem_name+str(insid)+'.lp')
    print('--------------------------------------------------------------')
   
    return Projects,Employees,LPModel


####################################################################################

problem_name = "ProjectScheduling"  
timelimit = 60

instances = [1, 2, 3, 4]

print('--> 1BK50 LP Assignment Template<--')
print('--> Important: Uncomment these lines to start working!',problem_name)

for insid in instances:          
    print('Problem instance: ',insid)       
    Projects,Employees = ConstructDataStructure(problem_name,insid)   
    Projects,Employees,LPModel = Question(Projects,Employees,problem_name,insid,timelimit)  
    LPModel,Projects,Employees,feedback,fgrade,varscore, sgrade = SolveLPMOdel(LPModel,Projects,Employees,timelimit,insid)
 
    for feed in feedback:
         print(feed)
      
#print('--> Important: Submit your file by making it back commented!')




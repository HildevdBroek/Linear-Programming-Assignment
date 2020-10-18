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
#iterate employees and use for each emplpoyee TimeSet Employee busy/idle times The binary variable ze,t indicates that employee e is busy at time unit t  employee.getBusyVars()

    TimeSet = list(range(Employees[0].getAvailability()))
    for emp in Employees:
       Employeeavailablevars = LPModel.addVars(TimeSet, vtype=grb.GRB.BINARY, name="z_"+str(emp.getID()))
        #employee.setExecVar(LPModel.addVar( vtype=grb.GRB.BINARY,name = vname))      
    Employeeavailable = Employee.getBusyVars(Employeeavailablevars.values())
   
    
#λp,p′ indicates that projects p and p’ have overlap in time p, p′ ∈ P project.getLambdaVars()

    counter = 0
    for Project in insid.getProject():
        counter = counter + 1
        TimeSet1 = list(range(Projects[0].getLambdavars()))
        TimeSet2 = list(range(Projects[counter].getLambdavars()))
        if TimeSet1 == TimeSet2:
            
            print("p = p'")
        else:
            OtherProjs = set(range(Project.getID()+1,len(Projects)))
            lambdavars = LPModel.addVars(OtherProjs,vtype=grb.GRB.BINARY, name="lmbd_"+str(Project.getID()))
            Project.getLambdaVars(lambdavars.values())            
    
#θp,t indicates that project p start in time t project.getStartVars()
#Project starts We consider every time unit as potential for a project start and define the binary variable θp,t indicating that project p starts at time t.   
    TimeSetproject = list(range(Project[0].getAvailability()))
    if Project in TimeSetproject == True:
        θname="θ_"+str(Project.getID())
    else:
        print("θ not in t")
        

# assignvars x_{e,p}, project start vars theta_{p,t}, and lambda var \lambda_{p,p'}
#xe,p assignment variable of employee e ∈ E to project p ∈ P project.getAssignmentVars()
    
    Projectslist = list(range(Projects[0], len(insid.getProjects())))
    SkillSet = list(range(Employees[0].getSkills())) 
    
    for emp in insid.getEmployee():
        Employeesskills = LPModel.addVars(SkillSet, vtype=grb.GRB.BINARY, name="z_"+str(emp.getskills()))  
        
    
    for projects in Projects:
        skills = list(range(Projects[0].getSkillRequirements))
        if Employeesskills == skills:
            empvars = LPModel.addVars(Employeesskills, vtype=grb.GRB.BINARY, name="Z_"+str(Project.getID()))
            Employee.getProjectVars(empvars.values())
        else:
            print("fout")
 
            

    # Creating decision variables.. 
     
    LPModel.update()
    return SolveLPMOdel()
        
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




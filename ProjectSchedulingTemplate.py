# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 11:05:33 2020

@author: mfirat
"""

import gurobipy as grb
import pandas as pd
import time
from ProjectschedulingLibrary import Project,Employee,ConstructDataStructure, intersection, SolveLPMOdel

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
        emp.setBusyVars(LPModel.addVars(TimeSetEmp, vtype=grb.GRB.BINARY, name = vname))
        print("Z works")
    
#λp,p′ indicates that projects p and p’ have overlap in time p, p′ ∈ P project.getLambdaVars()

    for Project in Projects:
        TimeSetLambda = list(range(len(Project.getCoincindingProjects())))
        print("p = p'")
        #OtherProjs = set(range(Project.getID()+1,len(Projects)))
        lname = "lambda_"+str(Project.getID())
        Project.setLambdaVars(LPModel.addVars(TimeSetLambda, vtype=grb.GRB.BINARY, name=lname))      
        print("lambda works")
    
#θp,t indicates that project p start in time t project.getStartVars()
#Project starts We consider every time unit as potential for a project start and define the binary variable θp,t indicating that project p starts at time t.   

    for Project in Projects:
        TimeSetTheta = list(range(Project.getStartTime()))
        Tname = "Theta_"+str(Project.getID())
        Project.setStartVars(LPModel.addVars(TimeSetTheta, vtype=grb.GRB.BINARY, name=Tname))      
        print("Theta works")               

# assignvars x_{e,p}, project start vars theta_{p,t}, and lambda var \lambda_{p,p'}
#xe,p assignment variable of employee e ∈ E to project p ∈ P project.getAssignmentVars()
    
  #  Projectslist = list(range(Projects[0], len(insid.getProjects())))
  #  SkillSet = list(range(Employees[0].getSkills()))         
    
    for Project in Projects:
        skills = list(range(len(Project.getSkillRequirements())))
        print("Skills requirements")    
        
    for emp in Employees:
        Employeesskills = list(range(len(emp.getSkills())))
        print ("employeeskills")
        intersect = intersection(skills, Employeesskills)
        pname = "X_"+str(Project.getID())
        Team = Project.setAssignmentVars(LPModel.addVars(intersect, vtype=grb.GRB.BINARY, name=pname))
           
        #if Employeesskills == skills:
          #  pname = "X_"+str(Project.getID())
          #  empvars = emp.getSkills(LPModel.addVars(skills, vtype=grb.GRB.BINARY, name=pname))
          # emp.setAssignmentVars(empvars.values())
          #  print("X works")     
        #else:
         #   print("fout")
    

         
         
    return Projects, Employees, timelimit   


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

problem_name = "ProjectScheduling"  
timelimit = 60

instances = [1, 2, 3, 4]

print('--> 1BK50 LP Assignment Template<--')
print('--> Important: Uncomment these lines to start working!',problem_name)

for insid in instances:          
    print('Problem instance: ',insid)       
    Projects,Employees = ConstructDataStructure(problem_name,insid)   
    Projects,Employees,LPModel = Question(Projects,Employees,problem_name,insid,timelimit)  
    LPModel,Projects,Employees,feedback,fgrade,varscore = SolveLPMOdel(LPModel,Projects,Employees,timelimit,insid)
 
    for feed in feedback:
         print(feed)
      
#print('--> Important: Submit your file by making it back commented!')




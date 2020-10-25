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
def Question(Projects, Employees, problem_name, insid, timelimit):

    print('--------------------------------------------------------------')
    LPModel = grb.Model(problem_name + str(insid) + "_LP")   
    LPModel.modelSense = grb.GRB.MAXIMIZE #2.1
    print('LP Solver timelimit:', timelimit)

# employee busy vars z_{e,t} 
#iterate employees and use for each emplpoyee TimeSet Employee busy/idle times The binary variable ze,t indicates that employee e is busy at time unit t  employee.getBusyVars()
    
    for emp in Employees:
        TimeSetEmp = list(range(len(emp.getAvailability())))
        vname = "z_" + str(emp.getID())
        Busy = LPModel.addVars(TimeSetEmp, vtype = grb.GRB.BINARY, name = vname)
        emp.setBusyVars(Busy.values())
        #print("Z works")
    
#λp,p′ indicates that projects p and p’ have overlap in time p, p′ ∈ P project.getLambdaVars()

    for Project in Projects:
        OtherProjs = list(range(Project.getID() + 1, len(Projects)))
        lname = "lambda_" + str(Project.getID())
        lambdavars = LPModel.addVars(OtherProjs, vtype = grb.GRB.BINARY, name = lname)
        Project.setLambdaVars(lambdavars.values())    
        #print("lambda works")
    
#θp,t indicates that project p start in time t project.getStartVars()
#Project starts We consider every time unit as potential for a project start and define the binary variable θp,t indicating that project p starts at time t.   

    for Project in Projects:
        TimeSetTheta = list(range(len(Employees[0].getAvailability())))
        Tname = "Theta_" + str(Project.getID())
        Theta = LPModel.addVars(TimeSetTheta, obj = Project.getWeight(), vtype = grb.GRB.BINARY, name = Tname)
        Project.setStartVars(Theta.values())      
        #print("Theta works")               

# assignvars x_{e,p}, project start vars theta_{p,t}, and lambda var \lambda_{p,p'}
#xe,p assignment variable of employee e ∈ E to project p ∈ P project.getAssignmentVars()      

    for Project in Projects:
        pname = "X_" + str(Project.getID())
        EmployeeProject = LPModel.addVars((list(range(len(Employees)))), vtype = grb.GRB.BINARY, name = pname)
        Project.setAssignmentVars(EmployeeProject.values())
        #print("X works")  
     
    LPModel.update()
    #return Projects, Employees, LPModel
        
    # Construct constraints        

    # constraints (2.2):
    C1name = 'C1_' + str(emp.getID())
    for i in range(len(emp.getBusyVars())):
        LPModel.addConstrs(((emp.getBusyVars()[i] <= emp.getAvailability()[i]) for emp in Employees), name = C1name)
     
    # constraints (2.3):
    M = 10000
    Mname = 'M_' + str(Project.getID())
    for Project in Projects:
        LPModel.addConstr((sum(Project.getAssignmentVars()) <= (M * sum(Project.getStartVars()))), name = Mname)

    # constraints (2.4):
    D1name = 'D1_' + str(Project.getID())
    TimeSetTheta = list(range(len(Employees[0].getAvailability())))
    for Project in Projects:
        for time in TimeSetTheta:
            if time <= Project.getDeadline():
                continue
            LPModel.addConstr((sum(Project.getStartVars()) <= 1), name = D1name)
        
    # constraints (2.5):
    D2name = 'D2' + str(Project.getID())
    TimeSetTheta = list(range(len(Employees[0].getAvailability())))
    for Project in Projects:
        for time in TimeSetTheta:
            if time > Project.getDeadline():
                continue
            LPModel.addConstr((sum(Project.getStartVars()) == 0), name = D2name)
           
    # constraints (2.6):
    C6name = 'C6_' + str(Project.getID())
    TimeSetTheta = list(range(len(Employees[0].getAvailability())))

    for Project in Projects:
        for Proj1 in range(Project.getID() + 1, (len(Projects))):
            Proj2 = Projects[Proj1]
            for t in TimeSetTheta:
                lambdas = Project.getLambdaVars()[Proj2.getID()-Project.getID() -1]
                somm1 = sum(Project.getStartVars()[max(0, t - Project.getDuration() + 1):t+1]) 
                somm2 = sum(Proj2.getStartVars()[max(0,t-Proj2.getDuration()+1):t+1])
                LPModel.addConstr(((somm1 + (somm2 - 1)) <= lambdas), name = C6name)
            
    # constraints (2.7):
    TimeSetTheta = list(range(len(Employees[0].getAvailability())))
    for emp in Employees:
        for Project in Projects:
            for t in TimeSetTheta:
                Thetasum = sum(Project.getStartVars()[max(0,t-Project.getDuration()+1):t+1])
                nm = 'bsyt_'+str(Project.getID())+'_'+str(emp.getID())+'_'+str(t)
                LPModel.addConstr(Thetasum+Project.getAssignmentVars()[emp.getID()]-1 <= emp.getBusyVars()[t],nm)

    # constraints (2.8):
    C8name = 'C8' + str(emp.getID())
    TimeSetEmp = list(range(len(emp.getAvailability())))
    for Project in Projects:
        for Dob1 in range(Project.getID()+1, (len(Projects))):
            Dob2 = Projects[Dob1]
            for t in TimeSetEmp:
                lambdas = Project.getLambdaVars()
                Xe = Project.getAssignmentVars()
                Xeother = Dob2.getAssignmentVars()
                LPModel.addConstr(((Xe + Xeother + lambdas) <= 2 ), name = C8name)
    
    # constraints (2.9):
    SkillSet = SkillSet = list(range(len(Employees[0].getSkills())))
    
    for Project in Projects:   
        for Skill in SkillSet:
                Sname = 'S'+ str(Project.getID()) + '_' + str(Project.getSkillRequirements()[Skill])
                ProjSkill = int(Project.getSkillRequirements()[Skill])
                EmpSkillAssignment = sum(int(emp.getSkills()[ProjSkill])* Project.getAssignmentVars()[emp.getID()] for emp in Employees)
                ProjStart = sum(Project.getStartVars())
                LPModel.addConstr(EmpSkillAssignment >= (int(Project.getSkillRequirements()[Skill])* ProjStart), name = Sname)
   
    #EmpSkill = list(range(len(emp.getSkills())))
    #ProjSkill = list(range(len(Project.getSkillRequirements())))
    
    #Sname = 'S_' + str(Project.getID())
    
   # for emp in Employees:
    #    som = sum(emp.getSkills() * Project.getAssignmentVars())
        
    #for Project in Projects:
     #   for skill in ProjSkill:
      #      LPModel.addConstr((som) >= (Project.getSkillRequirements() * sum(Project.getStartVars())), name = Sname)
    
        #was een probeersel van eerdere decision variabelen:
                #for emp in Employees:
        #Employeesskills = list(range(len(emp.getSkills())))
        #print ("employeeskills")
                #skills = list(range(len(Project.getSkillRequirements())))
                   
        #intersect = len(intersection(skills, Employeesskills))
        
    # constraints (2.10):
    C10name = 'C10_' + str(Project.getID)
    TimeSetTheta = list(range(len(Employees[0].getAvailability())))
    Projectlist = []
    for Project in Projects:
        Pred = (sum(Project.getPredecessors()[max(0,t - Project.getDuration() + 1):t+1]) for t in TimeSetTheta)
        Projectlist.append(Pred)
        for Pred0 in range(Project.getID()-1):
            Pred0 = Project.getStartVars()
            Projectlist.append(Pred0)
     #       LPModel.addConstrs((((Projectlist - Projectlist[Pred0]) >= (Project.getDuration() - (len(Employees[0].getAvailability()))(*(2 - sum(Project.getStartVars()[max(0, t - Project.getDuration() + 1):t+1]) - sum(Pred.getStartVars()[max(0,t-Pred.getDuration()+1):t+1]))))) for t in TimeSetTheta), name = C10name )

    # constraints (2.11):
    Lname = 'L_' + str(Project.getID())
    TimeSetTheta = list(range(len(Employees[0].getAvailability())))

    sommetjes = []
    for Project in Projects:
        for Proj2 in range(Project.getID() + 1, (len(sommetjes))):
            if Project in sommetjes[Proj2]:
                continue
            for Proj2 in Project.getPredecessors():
                proj = sum(Project.getStartVars() for Project in Projects)
                proj2 = sum(Project.getStartVars() for Proj2 in list(range(Project.getID()) + 1, (len(sommetjes))))
                LPModel.addConstr(proj <= proj2, name = Lname)
    
    # Construct constraints
    
    LPModel.write(problem_name+str(insid)+'.lp')
    print('--------------------------------------------------------------')
    LPModel.update()
    return Projects, Employees, LPModel


####################################################################################

problem_name = "ProjectScheduling"  
timelimit = 60

instances = [1, 2, 3, 4]

print('--> 1BK50 LP Assignment Template<--')
print('--> Important: Uncomment these lines to start working!', problem_name)

for insid in instances:          
    print('Problem instance: ', insid)       
    Projects,Employees = ConstructDataStructure(problem_name, insid)   
    Projects,Employees,LPModel = Question(Projects, Employees, problem_name, insid, timelimit)  
    LPModel,Projects,Employees,feedback,fgrade,varscore, sgrade = SolveLPMOdel(LPModel, Projects, Employees, timelimit, insid)
    
    for feed in feedback:
         print(feed)
         
print('--> Important: Submit your file by making it back commented!')
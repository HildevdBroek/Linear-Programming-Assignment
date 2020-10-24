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

    # constraints (2.2): - Hilde
    #LPModel.addConstr((emp.getAvailability()[emp]*emp.setBusyVars()[emp] for emp in list(range(len(emp.getAvailability())))) <= emp.getAvailability(), 'A_'+str(emp.getID()))
    Aname = 'A_' + str(emp.getID())
    for i in range(len(emp.getBusyVars())):
        LPModel.addConstrs(((emp.getBusyVars()[i] <= emp.getAvailability()[i]) for emp in Employees), name = Aname)
     
    # constraints (2.3):  - Nicole
    M = 10000
    Mname = 'M_' + str(Project.getID())
    for Project in Projects:
        LPModel.addConstr((sum(Project.getAssignmentVars()) <= (M * sum(Project.getStartVars()))), name = Mname)

    # constraints (2.4):  - Nicole
    D1name = 'D1_' + str(Project.getID())
    TimeSetTheta = list(range(len(Employees[0].getAvailability())))
    for Project in Projects:
        for time in TimeSetTheta:
            if time <= Project.getDeadline():
                continue
            LPModel.addConstr((sum(Project.getStartVars()) <= 1), name = D1name)
        
    # constraints (2.5):  - Nicole
    D2name = 'D2' + str(Project.getID())
    TimeSetTheta = list(range(len(Employees[0].getAvailability())))
    for Project in Projects:
        for time in TimeSetTheta:
            if time > Project.getDeadline():
                continue
            LPModel.addConstr((sum(Project.getStartVars()) == 0), name = D2name)
           
    # constraints (2.6): - Hilde
    D6name = 'D6_' + str(Project.getID())
    TimeSetTheta = list(range(len(Employees[0].getAvailability())))

    sommetjes = []
    for Project in Projects:
        sommie = (sum(Project.getStartVars()[max(0, t - Project.getDuration() + 1):t]) for t in TimeSetTheta)
        sommetjes.append(sommie)
    
   #     index = 0
        for Proj2 in range(Project.getID()+1, (len(sommetjes))):
            if sommetjes[Proj2] != sommetjes:
                continue
            if Proj2 not in Project.getCoincidingProject():
                continue
            for Project in Projects:
                  #      som = sommetjes[index]
                lambdas = Project.getLambdaVars()
                      #  index += 1
                    #    for z in range(index+1, (len(sommetjes))):
                LPModel.addConstr(((sommetjes + (sommetjes - 1)) <= lambdas), name = D6name)
            
    # constraints (2.7):  - Nicole
    timelist = []
    for time in TimeSetTheta:
        timelist.append(time)
        
        #for t2 in range(Project.getID() + 1, len(insid.getStartVars())):
         #   time2 = insid.getStartVars()[t2]
          #  if time2.getStartVars() == (Project.getStartVars()[max(0, time - Project.getDuration() + 1]):
           #     continue
            #for Project in Projects:
             #   Kname = 'K_' + str(Project.getID()) + str(time.getID()) + str(time2.getID())
               # LPModel.addConstr(sum(Project.getStartVars()) + Project.getAssignmentVars() - 1 <= emp.getBusyVars(), name = Kname)
        
             
    # constraints (2.8):   - Hilde
    TimeSetEmp = list(range(len(emp.getAvailability())))
    D8name = 'D8' + str(emp.getID())
    Double = []
    for Project in Projects:
        Dob = (sum(Project.getStartTime()[max(0, t - Project.getDuration() + 1):t]) for t in TimeSetTheta)
        Double.append(Dob)
        for Dob1 in range(Project.getID()+1):
            Dob1 = Project.getStartTime()
            Double.append(Dob1)
          #  if (Double[Dob] in Double[Dob1]) or (Double[Dob1] in Double[Dob]):
           #     continue
           #     for employee in Employees: 
                    #lambdas = Project.getLambdaVars()                          
         #   for projnext in range (proj+1, len(Projects)):
            #        LPModel.addConstr(((Double[Dob].getAssignmentVars() + Double[Dob1].getAssignmentVars() + Project.getLambdaVars() ) <= 2), name = D8name)

    
    # constraints (2.9):  - Nicole
    EmpSkill = list(range(len(emp.getSkills())))
    ProjSkill = list(range(len(Project.getSkillRequirements())))
    
    Sname = 'S_' + str(Project.getID())
    for emp in Employees:
        if (EmpSkill in ProjSkill) or (ProjSkill in EmpSkill):
            continue
        #LPModel.addConstr(sum(emp.getSkills() * Project.getAssignmentVars()) >= Project.getSkillRequirements * sum(Project.getStartVars()))
    
        #was een probeersel van eerdere decision variabelen:
                #for emp in Employees:
        #Employeesskills = list(range(len(emp.getSkills())))
        #print ("employeeskills")
                #skills = list(range(len(Project.getSkillRequirements())))
                   
        #intersect = len(intersection(skills, Employeesskills))
        
    # constraints (2.10):  - Hilde
    d10name = 'D10_' + str(Project.getID)
    TimeSetTheta = list(range(len(Employees[0].getAvailability())))
    Projectlist = []
    for Project in Projects:
        Pred = (sum(Project.getPredecessors()[max(0,t - Project.getDuration() + 1):t]) for t in TimeSetTheta)
        Projectlist.append(Pred)
        for Pred0 in range(Project.getID()-1):
            Pred0 = Project.getStartVars()
            Projectlist.append(Pred0)
          #  LPModel.addConstrs(((Projectlist >= Projectlist[Pred0]) for Project in Projects), name = d10name )
          #  print("pred")
              

    # constraints (2.11):  - Nicole
    
                                    
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
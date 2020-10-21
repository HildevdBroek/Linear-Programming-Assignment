# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 21:37:05 2020
1BK50-2020 LP Assignment Library


"""

import csv
import pandas as pd
import gurobipy as grb
import time
import random

class Project:

    # Initializer / Instance Attributes
    def __init__(self,myid,myduration,mydeadline,myweight):
        self.id = myid
        self.duration = myduration
        self.deadline = mydeadline
        self.weight =  myweight
        self.starttime = -1
        self.SkillRequirements = []
        self.Predecessors = []
        self.AssignmentVars = []
        self.StartVars = []
        self.starttime = -1
        self.LambdaVars = []
        self.EmployeeTeam = []
        self.CoincindingProjects = []
       
    def getID(self):
        return self.id
    
    def getDuration(self):
        return self.duration
    
    def getEmployeeTeam(self):
        return self.EmployeeTeam
    
    def getCoincindingProjects(self):
        return self.CoincindingProjects
    
    
    def getAssignmentVars(self):
        return self.AssignmentVars
    def setAssignmentVars(self,myvars):
        self.AssignmentVars = myvars
        
    def getStartVars(self):
        return self.StartVars
    def setStartVars(self,myvars):
        self.StartVars = myvars
    def getLambdaVars(self):
        return self.LambdaVars
    def setLambdaVars(self,myvars):
        self.LambdaVars = myvars
    
    
    def getSkillRequirements(self):
        return self.SkillRequirements
    
    def getPredecessors(self):
        return self.Predecessors
    
    def getDeadline(self):
        return self.deadline
    
    def getWeight(self):
        return self.weight
    
    def getStartTime(self):
        return self.starttime
    def setStartTime(self,strt):
        self.starttime = strt
    
    def printProject(self):
        print('Project('+str(self.getID())+')-> dur:',self.getDuration(),',due:',self.getDeadline(),',w:',self.getWeight(),', pred',self.getPredecessors(),', sk:',str(self.getSkillRequirements()))
    
class Employee:

    # Initializer / Instance Attributes
    def __init__(self,myid):
        self.id = myid
        self.Skills = []
        self.Availability = []
        self.BusyVars = []
        
    def getBusyVars(self):
        return self.BusyVars
    def setBusyVars(self,myvars):
        self.BusyVars = myvars   
       
    def getID(self):
        return self.id
    
    def getSkills(self):
        return self.Skills
    
    def getAvailability(self):
        return self.Availability
    
    def printEmployee(self):
        print('Employee('+str(self.getID())+')-> sk:',str(self.getSkills()))
  
def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3 


##################################################################################
def SolveLPMOdel(LPModel,Projects,Employees,timelimit,insid):
    
    model = LPModel
    
    
    Optlist = [752.0,944.0,1589.0,1083.0]
    
    feedback = [] 
    
    varscore = 0
    sgrade = 0
    fgrade = 0
    
    pvarproblems = len(Projects)
    pvarnoprobs = len(Projects)
    
    noexpectcons = 0
    
    noexpectcons+= 0.25*((len(Projects))**2)*(len(Employees[0].getAvailability())+len(Employees))  
    noexpectcons+= (len(Projects)+1)*(len(Employees[0].getAvailability())*len(Employees))
    
    noexpectcons+= (len(Projects)+1)*(len(Employees[0].getSkills())+7)
    
    nrconscoefficient = min(1,10*(len(LPModel.getConstrs())/noexpectcons))
    
    #print('expected no constraints',noexpectcons)
    
    feedback.append('--------  1BK50 LP Assignment Feedback ('+str(insid)+')  --------')
  
    for project in Projects:
        nobinaries = 0
        novars = 0
        
            
        
        for startvar in project.getStartVars():
            if startvar.vtype == 'B':
                nobinaries+=1  
        novars+= len(project.getStartVars()) 
        for lambdavar in project.getLambdaVars():
            if lambdavar.vtype == 'B':
                nobinaries+=1  
        novars+= len(project.getLambdaVars()) 
        if len(project.getLambdaVars()) != len(Projects)-(project.getID()+1):
             feedback.append('Lambda Variables of project '+str(project.getID())+' are not in correct number'+str(len(Projects)-(project.getID()+1)))
      
        for assignvar in project.getAssignmentVars():
             if assignvar.vtype == 'B':
                nobinaries+=1     
        novars+= len(project.getAssignmentVars())        
        if nobinaries != len(project.getStartVars())+len(project.getLambdaVars())+len(project.getAssignmentVars()) :
            feedback.append('Start-Assignment-Lambda Variables of project '+str(project.getID())+' are not all binaries!') 
        else: 
            pvarproblems -= 1
            
        if novars == len(Employees)+len(Projects)-(project.getID()+1)+len(Employees[0].getAvailability()):    
            pvarnoprobs -=1
            
            
    if pvarproblems == 0 and pvarnoprobs == 0:    
        feedback.append('Start-Assignment-Lambda variables of projects are correctly created!')
   
     
    varscore += 6.25*(int(pvarproblems == 0))+6.25*(int(pvarnoprobs == 0))
    

    
    evarproblems = len(Employees)
    evarnoprobs = len(Employees)
    for emp in Employees: 
        nobinaries = 0
        
        
        for busyvar in emp.getBusyVars():
             if busyvar.vtype == 'B':
                nobinaries+=1
        if nobinaries != len(emp.getBusyVars()):
            feedback.append('Busy vars of employee '+str(emp.getID())+' are not all binary!')
            continue
        else:
            evarproblems-=1  
        
        if len(emp.getBusyVars()) != len(emp.getAvailability()):
            evarnoprobs+=1
            feedback.append('Busy vars of employee '+str(emp.getID())+' are created not in correct number!')
        else:
            evarnoprobs-=1
            
    if evarproblems == 0 and evarnoprobs == 0:    
        feedback.append('Busy vars of all employees are correctly created!')
    
    varscore += 6.25*(int(evarproblems == 0 ))+6.25*(int(evarnoprobs == 0))
   
    
    
    # write the ILP model inot an lp file
    #model.write('Decisiontree.lp')
    start_time = time.time()
    model.Params.outputFlag = 0
    model.Params.timeLimit = timelimit
    model.optimize() 
    
  

  
    errorpoints  = []
    
    optimal = False
    feasible = False
    
    if model.status == 2: 
        print('--> '+model.ModelName+' model is solved optimally in ',round((time.time()-start_time),2),'secs.')
        print('--> Objective value: ',round(model.objVal,3))

        optimal = True
     
    else:
      
        if model.SolCount > 0:
            print('--> '+model.ModelName+' model solved not-optimally in timelimit',round((time.time()-start_time),2),'secs., solutions ',model.SolCount)
            print('--> Objective value: ',round(model.objVal,3)) #,'Optimality gap',model.MIPGap)
            
            # get the best solution found in the timelimit..
            model.Params.solutionNumber = 0
       
            feasible = True
     
        else:
            if model.status == 3:
                print('--'+model.ModelName+' model is infeasible!!')
            else:
                print('No solution could be found time limit!!')
    
    if not feasible and not optimal:
        
        feedback.append('Variable creation score: '+str(round(varscore,3))+' /25')
        feedback.append('Feasibility score: '+str(round(fgrade,3))+' / 50')
        feedback.append('Solution quality score: '+str(round(sgrade,3))+' / 25')
        
        
        return LPModel,Projects,Employees,feedback,fgrade,varscore,sgrade
    
    employeesprobs = len(Projects)
   
    for project in Projects: 
        selectedstarts = 0
        
        
        projind = project.getID()+1
        for lambdavar in project.getLambdaVars():
            if optimal:        
               if lambdavar.x > 0.5:
                   project.getCoincindingProjects().append(Projects[projind])
                  
            if feasible:
               if lambdavar.xn > 0.5:
                   project.getCoincindingProjects().append(Projects[projind])
                 
            projind+=1
            
        
        strt = 0
        for startvar in project.getStartVars():
        
           if optimal:        
               if startvar.x > 0.5:
                   project.setStartTime(strt)
                   #print('Project',project.getID(),startvar)
                   selectedstarts+=1
           if feasible:
               if startvar.xn > 0.5:
                   project.setStartTime(strt)
                   selectedstarts+=1
           strt +=1
        
        if selectedstarts > 1:
             feedback.append('Infeasibility constraint (2.4): Project '+str(project.getID())+' has more than one start time!')
           
        if project.getStartTime() > project.getDeadline():
             feedback.append('Infeasibility constraint (2.4): Project '+str(project.getID())+' starts later than its deadline!')
            
        
        empind = 0
        for assignvar in project.getAssignmentVars():
            if optimal:        
               if assignvar.x > 0.5:
                   project.getEmployeeTeam().append(Employees[empind])
                   if project.getStartTime() > 0:
                       for t in range(project.getStartTime(),project.getStartTime()+project.getDuration()):
                           if int(Employees[empind].getAvailability()[t]) == 0:
                               feedback.append('Infeasibility: Employee '+str(Employees[empind].getID())+' should work at time '+str(t)+' for project'+str(project.getID())+' but unavailable.')
                               #print('Infeasibility: Employee '+str(Employees[empind].getID())+' should work at time '+str(t)+' for project'+str(project.getID())+' but unavailable.')
                               #print(assignvar,Employees[empind].getBusyVars()[t],project.getStartVars()[project.getStartTime():project.getStartTime()+project.getDuration()])
                               employeesprobs+=1
            if feasible:
               if assignvar.xn > 0.5:
                   project.getEmployeeTeam().append(Employees[empind])
            empind+=1
            
       
        
    unselectedprojs = 0    
    skillsprobs = len(Projects)
  
    precedenceprobs = len(Projects)
    simulempprobs = len(Projects) 
    feedback.append('Selected Projects: ')
    
   
    
    for project in Projects:   
        proj = 'Project-'+str(project.getID())+', start:'+str(project.getStartTime())+', duration:'+str(project.getDuration())+', team: ['
        
        assignedskill = [0 for s in project.getSkillRequirements()]
           
        empid = 0
        for emp in project.getEmployeeTeam():
             for skill in range(len(emp.getSkills())):
                 assignedskill[skill]+=int(emp.getSkills()[skill])
             if empid > 0: 
                 proj+='-'+str(emp.getID())
             else: 
                 proj+=str(emp.getID())
             empid+=1
        proj+='], co-occuring: ['  
         
        
        nopredissue = not (len(project.getPredecessors())>0)
        
        #print('Project',project.getID(),' preds',len(project.getPredecessors()),' start',nopredissue)
      
        okpreds = len(project.getPredecessors())
        for pred in project.getPredecessors():
            mypred = Projects[int(pred)]
     
            
            if mypred.getStartTime() == -1 :   
                if project.getStartTime() > -1:
                    nopredissue = True
                    feedback.append('Infeasibility: Project '+str(project.getID())+' is selected, but its predecessor '+str(mypred.getID())+' is not selected.')
                else:
                    okpreds-=1
            else:
                if project.getStartTime() > -1:
                    if mypred.getStartTime()+mypred.getDuration() > project.getStartTime():
                        feedback.append('Infeasibility: Project '+str(project.getID())+' starts '+str(project.getStartTime())+' before completion of its predecessor '+str(mypred.getID())+', '+str(mypred.getStartTime()+mypred.getDuration()))
                        nopredissue = True
                    else:
                        okpreds-=1
                else:
                   okpreds-=1 
    
        #print('Project',project.getID(),' preds',len(project.getPredecessors()),' start',nopredissue)
        
        if nopredissue or okpreds == 0:
            precedenceprobs-=1
        
              

                
                        
         
        commonemp = False
        lambadvarsprob = 0
        projid = 0
        for myprojid in range(project.getID()+1,len(Projects)):
             myproj = Projects[myprojid]
             if project.getStartTime() == -1:
                 break
             if myproj.getStartTime() == -1 or project.getID() == myproj.getID():
                 continue
    
             if myproj.getStartTime() >= project.getStartTime()+project.getDuration() or project.getStartTime() >= myproj.getStartTime()+myproj.getDuration():
                continue
            
             if myproj not in project.getCoincindingProjects():
                 #print('Lambda var error: projects'+str(project.getID())+' and '+str(myproj.getID())+' coincide, but this is not seen with lambda var')
                 feedback.append('Lambda var error: Projects'+str(project.getID())+' and '+str(myproj.getID())+' coincide, but this is not seen with lambda var')
                 lambadvarsprob+=1
             if len(intersection(project.getEmployeeTeam(), myproj.getEmployeeTeam()))>0:  
                feedback.append('Infeasibility constraints (2.8): Co-occurring projects '+str(project.getID())+' and '+str(myproj.getID())+' have common employees.')
                commonemp = True

             if projid > 0:
                 proj+='-'+str(myproj.getID())
             else: 
                 proj+=str(myproj.getID())
             projid+=1
        if not commonemp:
            simulempprobs-=1
            
            
        proj+=']'
        
        if project.getStartTime() != -1: 
            feedback.append(proj)
            if len(project.getEmployeeTeam())> 0:
                employeesprobs-=1
         
        if project.getStartTime() == -1: 
            unselectedprojs+=1
            skillsprobs-=1
        
            if len(project.getEmployeeTeam())> 0: 
                feedback.append('Infeasibility constraints (2.3): Project'+str(project.getID())+' has assigned employees, but not selected!')
            else:
                employeesprobs-=1
            continue
        # check the total skills
        skillssatisfied = 0
        for s in range(len(project.getSkillRequirements())):
             if int(project.getSkillRequirements()[s]) <= assignedskill[s]:
                 skillssatisfied += 1
        if skillssatisfied < len(project.getSkillRequirements()):
            
            feedback.append('Infeasibility constraints (2.9): Project'+str(project.getID())+' skills are not completely satisfied!')
        else:
            skillsprobs-=1
            

    #print('simulempprobs',simulempprobs,'skillsprobs',skillsprobs,'employeesprobs',employeesprobs,'precedenceprobs',precedenceprobs)  
    fgrade+= 10*int(simulempprobs == 0)+10*int(skillsprobs == 0)+10*int(employeesprobs == 0)+10*int(precedenceprobs==0)
        
    

    
    feedback.append('Number of unselected projects: '+str(unselectedprojs))
        
    probemps = len(Employees)
    
    for emp in Employees:
        availbltyprobs = 0
        varind = 0
        busyrow = ''
        for var in emp.getBusyVars():
            if optimal:      
                if var.x > 0.5: 
                    busyrow+=',1'
                    if int(emp.getAvailability()[varind]) == 0:
                        feedback.append('Infeasibility constraint (2.2): Employee '+str(emp.getID())+' should work at time '+str(varind+1)+' but unavailable.')
                        availbltyprobs+=1    
                else:
                    busyrow+=',0'
            if feasible:
                if var.xn > 0.5:  
                    if int(emp.getAvailability()[varind]) == 0:
                        feedback.append('Infeasibility constraint (2.2): Employee'+str(emp.getID())+' should work at time '+str(varind+1)+' but unavailable.')  
                        availbltyprobs+=1             
            varind+=1
                 
        if availbltyprobs > 0:        
            feedback.append('Infeasibility constraint (2.2): Employee'+str(emp.getID())+' has is planned to work at times, but unavailable.')
        else:
            probemps-=1
        #print('Employee'+str(emp.getID())+': '+busyrow)
        #print(emp.getAvailability())
       
    print('probemps',probemps)
    fgrade += 10*int(probemps == 0 )
    
   
 
    
    fgrade = nrconscoefficient*fgrade
        
    #print('model obj: ',model.objVal,', reference value: ',Optlist[insid-1])
    
    if insid >= 0 and insid <= len(Optlist):
        if fgrade >= 50 - 10**-4:
            sgrade = 25*min(model.objVal,Optlist[insid-1])/Optlist[insid-1]
        else:
            if model.objVal <= Optlist[insid-1]:
                sgrade = 25*max(0,((model.objVal - 0.75*Optlist[insid-1])/(0.25*Optlist[insid-1])))
                
    sgrade = (fgrade/50)*sgrade
    
    feedback.append('Variable creation score: '+str(round(varscore,3))+' /25')
    feedback.append('Feasibility score: '+str(round(fgrade,3))+' / 50')
    feedback.append('Solution quality score: '+str(round(sgrade,3))+' / 25')
        
    print('----- Solution: decision checks and predictions   ----')
    
    
    return LPModel,Projects,Employees,feedback,fgrade,varscore,sgrade
 #################################################################################




##########################################################################################

def ConstructDataStructure(problem_name,insid):
    
    Projects = []
    Employees = []
 
    pfile = problem_name+'_Projects'+str(insid)+'.csv'
    projectdata = pd.read_csv(pfile)
    efile = problem_name+'_Employees'+str(insid)+'.csv'
    employeedata = pd.read_csv(efile)
 
    
   
    for proj in range(len(projectdata)):
             
        projectprops = projectdata.iloc[proj].tolist()
        
        myproj = Project(proj,projectprops[0],projectprops[1],projectprops[2])
        
        if str(projectprops[3]) != 'nan':
            skreqs = str(projectprops[3]).split('-')
            
            for skillval in skreqs:
                myproj.getSkillRequirements().append(skillval)
        
        
        if str(projectprops[4]) != 'nan':
            preds = str(projectprops[4]).split('-')
            
            for predid in preds:
                myproj.getPredecessors().append(int(predid))
                
        Projects.append(myproj)
                
            
            
    for proj in Projects:
        proj.printProject()
        
    for emp in range(len(employeedata)):
        
        empprops = employeedata.iloc[emp].tolist()
        
        myemp = Employee(emp)
        
         
        if str(empprops[0]) != 'nan':
            skills = str(empprops[0]).split('-')
            
            for skillval in skills:
                myemp.getSkills().append(int(skillval))
        
        #print(empprops[1])
        if str(empprops[1]) != 'nan':
            avail = str(empprops[1]).split('-')
            
            for avl in avail:
                myemp.getAvailability().append(int(avl))
                
        Employees.append(myemp)
      
        
    for emp in Employees:
        emp.printEmployee()  


    return Projects,Employees



 # -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 21:37:05 2020
1BK50-2020 LP Assignment Library


"""

import csv
import pandas as pd
import gurobipy as grb
import time
import random

class Project:

    # Initializer / Instance Attributes
    def __init__(self,myid,myduration,mydeadline,myweight):
        self.id = myid
        self.duration = myduration
        self.deadline = mydeadline
        self.weight =  myweight
        self.starttime = -1
        self.SkillRequirements = []
        self.Predecessors = []
        self.AssignmentVars = []
        self.StartVars = []
        self.starttime = -1
        self.LambdaVars = []
        self.EmployeeTeam = []
        self.CoincindingProjects = []
       
    def getID(self):
        return self.id
    
    def getDuration(self):
        return self.duration
    
    def getEmployeeTeam(self):
        return self.EmployeeTeam
    
    def getCoincindingProjects(self):
        return self.CoincindingProjects
    
    
    def getAssignmentVars(self):
        return self.AssignmentVars
    def setAssignmentVars(self,myvars):
        self.AssignmentVars = myvars
        
    def getStartVars(self):
        return self.StartVars
    def setStartVars(self,myvars):
        self.StartVars = myvars
    def getLambdaVars(self):
        return self.LambdaVars
    def setLambdaVars(self,myvars):
        self.LambdaVars = myvars
    
    
    def getSkillRequirements(self):
        return self.SkillRequirements
    
    def getPredecessors(self):
        return self.Predecessors
    
    def getDeadline(self):
        return self.deadline
    
    def getWeight(self):
        return self.weight
    
    def getStartTime(self):
        return self.starttime
    def setStartTime(self,strt):
        self.starttime = strt
    
    def printProject(self):
        print('Project('+str(self.getID())+')-> dur:',self.getDuration(),',due:',self.getDeadline(),',w:',self.getWeight(),', pred',self.getPredecessors(),', sk:',str(self.getSkillRequirements()))
    
class Employee:

    # Initializer / Instance Attributes
    def __init__(self,myid):
        self.id = myid
        self.Skills = []
        self.Availability = []
        self.BusyVars = []
        
    def getBusyVars(self):
        return self.BusyVars
    def setBusyVars(self,myvars):
        self.BusyVars = myvars   
       
    def getID(self):
        return self.id
    
    def getSkills(self):
        return self.Skills
    
    def getAvailability(self):
        return self.Availability
    
    def printEmployee(self):
        print('Employee('+str(self.getID())+')-> sk:',str(self.getSkills()))
  
def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3 


##################################################################################
def SolveLPMOdel(LPModel,Projects,Employees,timelimit,insid):
    
    model = LPModel
    
    
    Optlist = [756.0,944.0,1710.0,1024.0]
    
    feedback = [] 
    
    varscore = 0
    sgrade = 0
    fgrade = 0
    
    pvarproblem = 0
    pvarnoprobs = 0
    
    noexpectcons = 0
    
    noexpectcons+= 0.25*((len(Projects))**2)*(len(Employees[0].getAvailability())+len(Employees))  
    noexpectcons+= (len(Projects)+1)*(len(Employees[0].getAvailability())*len(Employees))
    
    noexpectcons+= (len(Projects)+1)*(len(Employees[0].getSkills())+7)
    
    nrconscoefficient = min(1,10*(len(LPModel.getConstrs())/noexpectcons))
    
    print('expected no constraints',noexpectcons)
    
    feedback.append('--------  1BK50 LP Assignment Feedback ('+str(insid)+')  --------')
  
    for project in Projects:
        nobinaries = 0
        novars = 0
        
            
        
        for startvar in project.getStartVars():
            if startvar.vtype == 'B':
                nobinaries+=1  
        novars+= len(project.getStartVars()) 
        for lambdavar in project.getLambdaVars():
            if lambdavar.vtype == 'B':
                nobinaries+=1  
        novars+= len(project.getLambdaVars()) 
        if len(project.getLambdaVars()) != len(Projects)-(project.getID()+1):
             feedback.append('Lambda Variables of project '+str(project.getID())+' are not in correct number'+str(len(Projects)-(project.getID()+1)))
      
        for assignvar in project.getAssignmentVars():
             if assignvar.vtype == 'B':
                nobinaries+=1     
        novars+= len(project.getAssignmentVars())        
        if nobinaries != len(project.getStartVars())+len(project.getLambdaVars())+len(project.getAssignmentVars()) :
            feedback.append('Start-Assignment-Lambda Variables of project '+str(project.getID())+' are not all binaries!') 
            pvarproblem+=1
        if novars != len(Employees)+len(Projects)-(project.getID()+1)+len(Employees[0].getAvailability()):    
            pvarnoprobs+=1
            
            
    if pvarproblem == 0 and pvarnoprobs == 0:    
        feedback.append('Start-Assignment-Lambda variables of projects are correctly created!')
   
     
    varscore += 12.5*(1 - (max(pvarproblem,pvarnoprobs)/len(Projects)) )    
     
    evarproblem = 0
    evarnoprobs = 0
    for emp in Employees: 
        nobinaries = 0
        
        for busyvar in emp.getBusyVars():
             if busyvar.vtype == 'B':
                nobinaries+=1
        if nobinaries != len(emp.getBusyVars()):
            feedback.append('Busy vars of employee '+str(emp.getID())+' are not all binary!')
            evarproblem+=1   
        if len(emp.getBusyVars()) != len(emp.getAvailability()):
            evarnoprobs+=1
            feedback.append('Busy vars of employee '+str(emp.getID())+' are created not in correct number!')
           
            
    if evarproblem == 0 and evarnoprobs == 0:    
        feedback.append('Busy vars of all employees are correctly created!')
    
    varscore += (12.5)*(1 - max(evarproblem,evarnoprobs)/len(Employees) )   
    
    
    # write the ILP model inot an lp file
    #model.write('Decisiontree.lp')
    start_time = time.time()
    model.Params.outputFlag = 0
    model.Params.timeLimit = timelimit
    model.optimize() 
    
  

  
    errorpoints  = []
    
    optimal = False
    feasible = False
    
    if model.status == 2: 
        print('--> '+model.ModelName+' model is solved optimally in ',round((time.time()-start_time),2),'secs.')
        print('--> Objective value: ',round(model.objVal,3))

        optimal = True
     
    else:
      
        if model.SolCount > 0:
            print('--> '+model.ModelName+' model solved not-optimally in timelimit',round((time.time()-start_time),2),'secs., solutions ',model.SolCount)
            print('--> Objective value: ',round(model.objVal,3)) #,'Optimality gap',model.MIPGap)
            
            # get the best solution found in the timelimit..
            model.Params.solutionNumber = 0
       
            feasible = True
     
        else:
            if model.status == 3:
                print('--'+model.ModelName+' model is infeasible!!')
            else:
                print('No solution could be found time limit!!')
    
    if not feasible and not optimal:
        
        feedback.append('Variable creation score: '+str(round(varscore,3))+' /25')
        feedback.append('Feasibility score: '+str(round(fgrade,3))+' / 50')
        feedback.append('Solution quality score: '+str(round(sgrade,3))+' / 25')
        
        
        return LPModel,Projects,Employees,feedback,fgrade,varscore,sgrade
    
   
    for project in Projects: 
        selectedstarts = 0
        
        
        projind = project.getID()+1
        for lambdavar in project.getLambdaVars():
            if optimal:        
               if lambdavar.x > 0.5:
                   project.getCoincindingProjects().append(Projects[projind])
                  
            if feasible:
               if lambdavar.xn > 0.5:
                   project.getCoincindingProjects().append(Projects[projind])
                 
            projind+=1
            
        
        strt = 1 
        for startvar in project.getStartVars():
        
           if optimal:        
               if startvar.x > 0.5:
                   project.setStartTime(strt)
                   selectedstarts+=1
           if feasible:
               if startvar.xn > 0.5:
                   project.setStartTime(strt)
                   selectedstarts+=1
           strt +=1
        
        if selectedstarts > 1:
             feedback.append('Infeasibility constraint (2.4): Project '+str(project.getID())+' has more than one start time!')
           
        if project.getStartTime() > project.getDeadline():
             feedback.append('Infeasibility constraint (2.4): Project '+str(project.getID())+' starts later than its deadline!')
            
        
        empind = 0
        for assignvar in project.getAssignmentVars():
            if optimal:        
               if assignvar.x > 0.5:
                   project.getEmployeeTeam().append(Employees[empind])
            if feasible:
               if assignvar.xn > 0.5:
                   project.getEmployeeTeam().append(Employees[empind])
            empind+=1
            
       
        
    unselectedprojs = 0    
    skillsprobs = 0
    employeesprobs = 0
    precedenceprobs = 0
    feedback.append('Selected Projects: ')
    for project in Projects:   
        proj = 'Project-'+str(project.getID())+', start:'+str(project.getStartTime())+', duration:'+str(project.getDuration())+', team: ['
        
        assignedskill = [0 for s in project.getSkillRequirements()]
           
        empid = 0
        for emp in project.getEmployeeTeam():
             for skill in range(len(emp.getSkills())):
                 assignedskill[skill]+=int(emp.getSkills()[skill])
             if empid > 0: 
                 proj+='-'+str(emp.getID())
             else: 
                 proj+=str(emp.getID())
             empid+=1
        proj+='], co-occuring: ['  
         
       
        
        for pred in project.getPredecessors():
            mypred = Projects[int(pred)]
            
            if mypred.getStartTime() == -1 and project.getStartTime() > -1:
                  precedenceprobs+=1
                  feedback.append('Infeasibility: Project '+str(project.getID())+' is selected, but its predecessor '+str(mypred.getID())+' is not selected.')
            else:
                if mypred.getStartTime() != -1 and project.getStartTime() != -1:
                    if mypred.getStartTime()+mypred.getDuration() > project.getStartTime():
                        feedback.append('Infeasibility: Project '+str(project.getID())+' starts '+str(project.getStartTime())+' before completion of its predecessor '+str(mypred.getID())+', '+str(mypred.getStartTime()+mypred.getDuration()))
                        precedenceprobs+=1
                        
         
        intersectons = 0
        projid = 0
        for myprojid in range(project.getID()+1,len(Projects)):
             myproj = Projects[myprojid]
             if project.getStartTime() == -1:
                 break
             if myproj.getStartTime() == -1 or project.getID() == myproj.getID():
                 continue
    
             if myproj.getStartTime() >= project.getStartTime()+project.getDuration() or project.getStartTime() >= myproj.getStartTime()+myproj.getDuration():
                continue
            
             if myproj not in project.getCoincindingProjects():
                 print('projects'+str(project.getID())+' and '+str(myproj.getID())+' coincide, but this is not seen with lambda var')
            
             if len(intersection(project.getEmployeeTeam(), myproj.getEmployeeTeam()))>0:
                intersectons+=1  
                feedback.append('Infeasibility constraints (2.8): Co-occurring projects '+str(project.getID())+' and '+str(myproj.getID())+' have common employees.')
           
             if projid > 0:
                 proj+='-'+str(myproj.getID())
             else: 
                 proj+=str(myproj.getID())
             projid+=1
    
        proj+=']'
        
        if project.getStartTime() != -1: 
            feedback.append(proj)
         
        if project.getStartTime() == -1: 
            unselectedprojs+=1
            if len(project.getEmployeeTeam()) > 0:
                employeesprobs+=1
                feedback.append('Infeasibility constraints (2.3): Project'+str(project.getID())+' has assigned employees, but not selected!')
            continue
        # check the total skills
        skillssatisfied = 0
        for s in range(len(project.getSkillRequirements())):
             if int(project.getSkillRequirements()[s]) <= assignedskill[s]:
                 skillssatisfied += 1
        if skillssatisfied < len(project.getSkillRequirements()):
             skillsprobs+=1
             feedback.append('Infeasibility constraints (2.9): Project'+str(project.getID())+' skills are not completely satisfied!')
         
        if skillsprobs > 0:
            feedback.append(str(skillsprobs)+' projects have unsatisfied skills!')
       
      
    fgrade+=25*(1-max(skillsprobs+employeesprobs+precedenceprobs,pvarproblem,pvarnoprobs)/(len(Projects)))  
    

    
    feedback.append('Number of unselected projects: '+str(unselectedprojs))
        
    probemp = 0
    for emp in Employees:
        availbltyprobs = 0
        varind = 0
        for var in emp.getBusyVars():
            if optimal:      
                if var.x > 0.5:             
                    if int(emp.getAvailability()[varind]) == 0:
                        feedback.append('Infeasibility constraint (2.2): Employee '+str(emp.getID())+' should work at time '+str(varind+1)+' but unavailable.')
                        availbltyprobs+=1    
      
            if feasible:
                if var.xn > 0.5:  
                    if int(emp.getAvailability()[varind]) == 0:
                        feedback.append('Infeasibility constraint (2.2): Employee'+str(emp.getID())+' should work at time '+str(varind+1)+' but unavailable.')  
                        availbltyprobs+=1             
            varind+=1
                 
        if availbltyprobs > 0:
            probemp+=1
            feedback.append('Infeasibility constraint (2.2): Employee'+str(emp.getID())+' has is planned to work at times, but unavailable.')
        
    fgrade += 25*(1 - max(evarproblem,probemp,evarnoprobs)/len(Employees))
    
 
    
    fgrade = nrconscoefficient*fgrade
        
    
    if insid >= 0 and insid <= len(Optlist):
        if fgrade >= 50 - 10**-4:
            sgrade = 25*min(model.objVal,Optlist[insid-1])/Optlist[insid-1]
        else:
            if model.objVal <= Optlist[insid-1]:
                sgrade = 25*model.objVal/Optlist[insid-1]
                
  
    
    feedback.append('Variable creation score: '+str(round(varscore,3))+' /25')
    feedback.append('Feasibility score: '+str(round(fgrade,3))+' / 50')
    feedback.append('Solution quality score: '+str(round(sgrade,3))+' / 25')
        
    print('----- Solution: decision checks and predictions   ----')
    
    
    return LPModel,Projects,Employees,feedback,fgrade,varscore,sgrade
 #################################################################################




##########################################################################################

def ConstructDataStructure(problem_name,insid):
    
    Projects = []
    Employees = []
 
    pfile = problem_name+'_Projects'+str(insid)+'.csv'
    projectdata = pd.read_csv(pfile)
    efile = problem_name+'_Employees'+str(insid)+'.csv'
    employeedata = pd.read_csv(efile)
 
    
   
    for proj in range(len(projectdata)):
             
        projectprops = projectdata.iloc[proj].tolist()
        
        myproj = Project(proj,projectprops[0],projectprops[1],projectprops[2])
        
        if str(projectprops[3]) != 'nan':
            skreqs = str(projectprops[3]).split('-')
            
            for skillval in skreqs:
                myproj.getSkillRequirements().append(skillval)
        
        
        if str(projectprops[4]) != 'nan':
            preds = str(projectprops[4]).split('-')
            
            for predid in preds:
                myproj.getPredecessors().append(int(predid))
                
        Projects.append(myproj)
                
            
            
    for proj in Projects:
        proj.printProject()
        
    for emp in range(len(employeedata)):
        
        empprops = employeedata.iloc[emp].tolist()
        
        myemp = Employee(emp)
        
         
        if str(empprops[0]) != 'nan':
            skills = str(empprops[0]).split('-')
            
            for skillval in skills:
                myemp.getSkills().append(int(skillval))
        
        #print(empprops[1])
        if str(empprops[1]) != 'nan':
            avail = str(empprops[1]).split('-')
            
            for avl in avail:
                myemp.getAvailability().append(int(avl))
                
        Employees.append(myemp)
      
        
    for emp in Employees:
        emp.printEmployee()  


    return Projects,Employees



 
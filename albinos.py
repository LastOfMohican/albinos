from AlbinosProvider import *
from LogicConfig import *
import sys
import os.path
import argparse
import datetime
import time
DEFAULT_LOGIC="Lukasiewicz"

def getAlbinosFileName(logicName):
    return "Albinos_"+logicName+".alc"

def getLogicFileName(logicName):
    return logicName+".albc"

def createAlbinosConfig(file_name):
    return AlbinosProvider.createAlbinosConfigFromFile(getLogicFileName(file_name))


def fileExist(file_name):
    return os.path.isfile(file_name)

def searchAlbinosConfig(logicName):
    file_name=getAlbinosFileName(logicName)
    if fileExist(file_name):
        return file_name


def searchLogicConfig(logicName):
    file_name=getLogicFileName(logicName)
    if fileExist(file_name):
        return file_name

def getAlbinosConfig(logicName):
    alb=searchAlbinosConfig(logicName)
    if alb == None:
        lc=searchLogicConfig(logicName)
        if lc==None:
            if logicName==DEFAULT_LOGIC:
                lc=LogicConfig.getDefaultConfig()
                lc.write_to_file(DEFAULT_LOGIC+".albc")
            else:
                txt=f'Not found logic file: '+getLogicFileName(logicName)
                raise Exception(txt)
        alb=createAlbinosConfig(logicName)
    return AlbinosProvider.loadAlbinosConfigFromFile(alb)

def getBasicInfo(info):
    txt=""
    txt+='Expected result: ' +str(info['args'].value)+'\n'
    txt+='Formula: \n'+str(info['albinos'].formula)+'\n'
    txt+='\nLogic: '+str(info['args'].logic)+'\n'
    txt+='\nValuation: \n'+str(info['albinos'].str_result)+'\n'   
    txt+='CPU time: '+str(info['cpu_time'])+'\n'
    txt+='Elapsed time: '+str(info['wallclock_time'])+'\n' 
    return txt


def printAllToFIle(info,fileName):
    txt=getAllInfo(info)
    with open(fileName, 'w') as file:
        file.write(txt)

def getAllInfo(info):
    txt=""
    txt+=getBasicInfo(info)
    txt+='SatSolver Valuation:\n'+str(info['albinos'].SatSolverValuationResult)+"\n\n"
    txt+='Formula Tree:\n'+str(info['albinos'].FormulaTreeResult)+"\n\n"
    txt+='Clauses:\n'+ str(info['albinos'].AlbinosClausesResult)+"\n\n"
    return txt
def logInfo(info):
    if info['args'].all:
        print(getAllInfo(info))
        return
    print(getBasicInfo(info))
    if info['args'].save:
        current_datetime = datetime.datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d-%H:%M:%S")
        fileName='Albinos_log_'+info['args'].logic+formatted_datetime+'.txt'
        printAllToFIle(info,fileName)
    if info['args'].tree:
        print('Formula Tree:\n'+str(info['albinos'].FormulaTreeResult)+"\n\n")
    if info['args'].result:
        print('SatSolver Valuation:\n'+str(info['albinos'].SatSolverValuationResult)+"\n\n")
    if info['args'].clause:
        print('Clauses:\n'+ str(info['albinos'].AlbinosClausesResult)+"\n\n")



def __main__(args):
    if not args.formula:
        print("Formula is empty")
        return 1

    cpu_start_time = time.process_time()
    wallclock_start_time = time.time()
    result=run(args.formula,args.logic,args.value)
    cpu_end_time = time.process_time()

    wallclock_end_time = time.time()
    cpu_time = cpu_end_time - cpu_start_time
    wallclock_time = wallclock_end_time - wallclock_start_time

    info={
        "args":args,
        "cpu_time":cpu_time,
        "wallclock_time":wallclock_time,
        "albinos":result
    }
    logInfo(info)
    return 0

def run(formula:str,logicName:str,ExpectedResult:str):
    albinos=getAlbinosConfig(logicName)
    albinos.evaluateFromula(formula,ExpectedResult)
    return albinos
def getTestArgs(args):
    #args.logic="Kleene"
    #args.value="F"
    args.formula="#a"
    #args.formula="a and b"    
    args.formula="((a or ~a) => (a and ~a))"
    a=args.formula
    args.formula=f"({a} or ~{a}) => ({a} and ~{a})"
    #args.result=True

    #args.logic="Kleene"
    args.value='U'
    args.result=True
    #args.clause=True
    args.save=True
    args.tree=True
    return args
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Albinos 0.0.1')
    parser.add_argument("formula_args", nargs='?', help="Formula sequence")
    parser.add_argument("-f", "--formula", nargs='?', const='',help="Formula sequence")
    parser.add_argument("-l", "--logic",default=DEFAULT_LOGIC, help="Logic name")
    parser.add_argument("-v", "--value", default="T",help="Value expected result")
    parser.add_argument("-s", "--save", action='store_true',help="Save all info to file")   
    parser.add_argument("-t", "--tree", action='store_true',help="Print tree formula")  
    parser.add_argument("-c", "--clause",action='store_true', help="Print all clause")    
    parser.add_argument("-r", "--result", action='store_true',help="Print result valuation")   
    parser.add_argument("-a", "--all", action='store_true',help="Print all info")   

    args=parser.parse_args()
    Test=False
    if Test:
       args=getTestArgs(args)
    if args.formula_args:
        args.formula=args.formula_args
    sys.exit(__main__(args))





import sys
from AlbinosConfig import *
from AlbinosSolver import *
from SatSolver import *

FILE_EXTENSION="alc"
FILE_PRENAME="Albinos_"
class AlbinosProvider:
    def __init__(self,albinos_config:AlbinosConfig):
        self.albinos_config=albinos_config
      
    @classmethod
    def loadAlbinosConfigFromFile(cls,file_path:str):
        return cls(albinos_config=AlbinosConfig.load_from_file(file_path))

    @staticmethod
    def createAlbinosConfigFromFile(file_path:str):
        logicConfig=LogicConfig.read_from_file(file_path)
        return AlbinosProvider.createAlbinosConfigFromLogicConfig(logicConfig)
    @staticmethod
    def createAlbinosConfigFromLogicConfig(logicConfig:LogicConfig):
        albinos_config=AlbinosConfig.fromLogicConfig(logicConfig)
        fileName=FILE_PRENAME+logicConfig.NAME+"."+FILE_EXTENSION
        albinos_config.save_to_file(fileName)
        return fileName
 

    def evaluateFromula(self,formula:str,ExpectedResult:str):
        if self.albinos_config==None:
            raise ValueError("Not found albinos config")
   
        albinos=AlbinosSolver(formula,self.albinos_config)
        self.formula=albinos.strformula
        result=albinos.solve(ExpectedResult)
        s=SatSolver()
        res=s.solve(result)
        self.FormulaTreeResult=self.toTreeResult(albinos)
        self.AlbinosClausesResult=self.toTextClause(result)
        self.SatSolverValuationResult=res
        self.str_result=None
        if res==None:
            return "None"
        self.str_result=self.toTextResults(res, albinos)
        return self.str_result

    def toTreeResult(self,albinos):
        txt=""
        for key,value in albinos.variable_dict.items():


            if isinstance(key,int):
                txt+=str(key)+" : "+str(value)+"\n"
        return txt

    def toTextClause(self,clause):
        txt=""
        for c in clause:
            txt+=str(c)+"\n"
        return txt
    def toTextResults(self,res,albinos):
        stack=[]
        txt=""
        for e in res:
            stack.append(e)
            if len(stack)<2:
                continue
            el=stack.pop()
            elstr=albinos.variable_dict[abs(el)]
            if e!=res[-1] and not( elstr.right==None and elstr.left==None):
                stack=[]
                continue
            
            v1=el
            v2=stack.pop()
            result=""
            value=elstr.value
            if e==res[-1]:
                value="Result"
            if v1>0 and v2>0:
                result="T"
            elif v1<0 and v2<0:
                result="F"
            else:
                result ="U"
            txt+=(value+" : "+result+"\n")
        return txt
import numpy as np
from Operator import *
from LogicConfig import *
from TruthTableProvider import *
class FormulaOperator:
    def __init__(self,chars:list[str],F1:list[list],F2:list[list],isNonBinary,priority):
        self.chars=chars
        self.F1=F1
        self.F2=F2
        self.priority=priority
        self.isNonBinary=isNonBinary


    def setPriority(self,priority:int):
        self.priority=priority
        return self

    def setBinary(self):
        self.isNonBinary=True
        return self

    def to_dict(self):
            return {
            'chars': self.chars,
            'F1': self.F1,
            'F2': self.F2,
            'priority': self.priority,
            'isNonBinary': self.isNonBinary
        }
    @classmethod
    def from_dict(cls, data: dict):
        return cls(data['chars'], data['F1'],data['F2'],data['isNonBinary'],data['priority'])

    def solveFormula1(self,vars):
        return self.solveByFormula(self.F1, vars)
    def solveFormula2(self,vars):
        return self.solveByFormula(self.F2, vars)

    def solveByFormula(self,F,vars):
        new_array=[]
        for row in F:
            r=[]
            for i, x in enumerate(vars):
                r.append(row[i]* x)
            new_array.append(r)
        return new_array

    @classmethod
    def fromOperator(cls,operator,logicConfig):
        ttp=TruthTableProvider(logicConfig)
        truth_table = ttp.convertToBinaryTable(operator)
        F1=FormulaOperator.setFormula(-1,truth_table)
        F2=FormulaOperator.setFormula(-2,truth_table)

       
        return cls(operator.chars,F1,F2,operator.isNonBinary,operator.Priority)

  


    @staticmethod   
    def setFormula(excludeIndex,truth_table):
        arr=np.delete(truth_table,excludeIndex,axis=1)
        newArr=[]
        for row in arr:
            nrow = [-1 if val else 1 for val in row]
            if row[-1]:
                nrow[-1]=1   
            else:
                nrow[-1]=-1
            newArr.append(nrow)
        return newArr
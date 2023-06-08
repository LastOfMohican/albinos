import sys 
import json
class Operator:
    def __init__(self,chars:list[str],array):
        self.chars=chars
        self.array=array
        self.isNonBinary=False
        self.Priority=1024
        self.Deepth=self.getDictDepth(array)

    def call(self,stack):
        return self.solve(stack,self.array)
    
    def getDictDepth(self,stack):
        key=next(iter(stack))
        value = stack[key]
        if isinstance(value, dict):
            return self.getDictDepth(value)+1
        return 1
    def solve(self,stack,array):
        key=stack.pop()
        values=array[key]
        if isinstance(values, dict):
            values=self.solve(stack,values)
        return values

    def setIsNonBinary(self):
        self.isNonBinary=True
        return self

    def setPriority(self,priority:int):
        self.Priority=priority
        return self
    def to_dict(self):
        return {
            "chars": self.chars,
            "array": self.array,
            "isNonBinary": self.isNonBinary,
            "Priority": self.Priority
        }


    @staticmethod
    def from_dict(data):
        chars = data["chars"]
        array = data["array"]
        operator = Operator(chars, array)
        operator.isNonBinary = data["isNonBinary"]
        operator.Priority = data["Priority"]
        return operator




    
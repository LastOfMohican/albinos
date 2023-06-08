from typing import List
import itertools
from LogicConfig import *
class TruthTableProvider:
    def __init__(self, logic_config):
        self.logic_config = logic_config

    @staticmethod
    def generateCombnation(num_bits):
        combinations = []
        for i in range(2 ** num_bits):
            bits = []
            for j in range(num_bits):
                bit = (i >> j) & 1
                bits.append(bit)
            combinations.append(bits)
        return combinations

    def getBannedCombination(self):
        split_dict=self.logic_config.TRUTH_VALUES_SPLIT
        values_clause=[]
        for  value in split_dict.values():
            row=[]
            for v in value:
                row.append(self.toBinaryNum(v))
            values_clause.append(row)
        depth=len(split_dict[next(iter(split_dict))])

        combination=TruthTableProvider.generateCombnation(depth)
        arr= [x for x in combination if x not in values_clause]
        result=[]
        for row in arr:
            nrow = [-1 if val else 1 for val in row]
            result.append(nrow)
        return result;


            
    def convertToBinaryTable(self,operator):
        split_dict=self.logic_config.TRUTH_VALUES_SPLIT

        reversed_dict = {}

        for key, values in split_dict.items():
            if values[0] not in reversed_dict:
                reversed_dict[values[0]] = {}
            reversed_dict[values[0]][values[1]] = key
 
        num_bits = operator.Deepth*2  # Number of bits
        combinations=TruthTableProvider.generateCombnation(num_bits)
        maxDepth=0
        for value in split_dict.values():
            maxDepth=max(maxDepth,len(value))

        template=[]
        for row in combinations:
            stackValue=[]
            stack=[]
            row_template=[]
            for el in row:
                row_template.append(el)
                stack.append(el)
                if len(stack)<maxDepth:
                    continue
                value=self.getValue(reversed_dict,stack[::-1])
                stackValue.append(value)
                stack=[]
            if None in stackValue:
                continue
            resultValue=operator.call(stackValue[::-1])
            truth_values=split_dict[resultValue]
            for vt in truth_values:
                row_template.append(self.toBinaryNum(vt))
            template.append(row_template)
            row_template=[]
        return template

 
 
    def getValue(self,rdict,stack):
        if not stack:
            return None
        key=self.toValue(stack.pop())
        if not key in rdict:
            return None;
        value = rdict[key]
        if isinstance(value, dict):
            return self.getValue(value,stack)
        return value


    def toBinaryNum(self,value):
        return {'T':1,'F':0}[value]

  
    def toValue(self,value):
        return {1:'T',0:'F'}[value]
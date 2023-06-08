from Operator import *
import json
from typing import List
class LogicConfig:
    def __init__(self,operators:list[Operator],TRUTH_VALUES,TRUTH_VALUES_SPLIT,NAME):
        self.TRUTH_VALUES=TRUTH_VALUES
        self.operators=operators
        self.TRUTH_VALUES_SPLIT=TRUTH_VALUES_SPLIT
        self.NAME=NAME
        self.prepareOperatorsDict()
    def prepareOperatorsDict(self):
        self.OPERATORS_DICTIONARY={}

        self.operators_list=[]
        for x in self.operators:
            for c in x.chars:
                self.OPERATORS_DICTIONARY.update({c:x})
                self.operators_list.append(c)             


    @staticmethod    
    def getDefaultConfig():
        NAME="Lukasiewicz"
        operators=[]
        chars=['~','¬','not','!']
        operators.append(Operator(chars, array = {
                    'F': 'T',
                    'U': 'U',
                    'T': 'F'
                }).setIsNonBinary().setPriority(50))
        chars=['∨','or','v','||']
        operators.append(Operator(chars, array = {
                    'F': {'T': 'T', 'F': 'F', 'U': 'U'},
                    'U': {'T': 'T', 'F': 'U', 'U': 'U'},
                    'T': {'T': 'T', 'F': 'T', 'U': 'T'}
                }).setPriority(100))
        chars=['&','∧','and','&&']
        operators.append(Operator(chars, array = {
                    'F': {'T': 'F', 'F': 'F', 'U': 'F'},
                    'U': {'T': 'U', 'F': 'F', 'U': 'U'},
                    'T': {'T': 'T', 'F': 'F', 'U': 'U'},
                }).setPriority(120))
        chars=['->','@','→','imp','=>']
        operators.append(Operator(chars, array = {
                    'F': {'F': 'T', 'U': 'T', 'T': 'T'},
                    'U': {'F': 'U', 'U': 'T', 'T': 'T'},
                    'T': {'F': 'F', 'U': 'U', 'T': 'T'}
                }).setPriority(140))
        chars=['#']
        operators.append(Operator(chars, array = {
                    'F': 'F',
                    'U': 'T',
                    'T': 'F'
                }).setIsNonBinary().setPriority(40))        
        TRUTH_VALUES = [ 'F','U','T']
        TRUTH_VALUES_SPLIT={
            'T':['T','T'],
            'F':['F','F'],
            'U':['T','F']
        }
        return LogicConfig(operators=operators,TRUTH_VALUES=TRUTH_VALUES,TRUTH_VALUES_SPLIT=TRUTH_VALUES_SPLIT,NAME=NAME)

    def to_dict(self):
        return {
            'NAME':self.NAME,
            'TRUTH_VALUES': self.TRUTH_VALUES,
            'TRUTH_VALUES_SPLIT':self.TRUTH_VALUES_SPLIT,
            'operators': [operator.to_dict() for operator in self.operators]
        }

    def to_json(self):
        return json.dumps(self.to_dict(), ensure_ascii=False,indent=4)

    @staticmethod
    def from_dict(data):
        operators = [Operator.from_dict(operator_data) for operator_data in data['operators']]
        TRUTH_VALUES = data['TRUTH_VALUES']
        TRUTH_VALUES_SPLIT= data['TRUTH_VALUES_SPLIT']
        NAME=data['NAME']
        return LogicConfig(operators, TRUTH_VALUES,TRUTH_VALUES_SPLIT,NAME)

    @staticmethod
    def from_json(json_str):
        data = json.loads(json_str)
        return LogicConfig.from_dict(data)

    def write_to_file(self, file_path):
        with open(file_path, 'w') as f:
            f.write(self.to_json())

    @staticmethod
    def read_from_file(file_path):
        with open(file_path, 'r') as f:
            json_str = f.read()
        return LogicConfig.from_json(json_str)
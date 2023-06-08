from FormulaOperator import *
import json
from LogicConfig import *
class AlbinosConfig:
    def __init__(self,Name:str,FormulaOperators:list[FormulaOperator],BannedCombination:list):
        self.name=Name
        self.FormulaOperators=FormulaOperators
        self.prepareAlbinosConfig()
        self.BannedCombination=BannedCombination

    def prepareAlbinosConfig(self):
        self.formula_operators_dict={}
        self.operator_priority_dict={}
        self.nonBinary_operators_list=[]
        self.operator_chars=[]
        self.operator_priority_dict=dict(sorted(self.operator_priority_dict.items()))
        for formula_operator in self.FormulaOperators:
            self.operator_priority_dict.update({formula_operator.priority:formula_operator.chars})
 
            for char in formula_operator.chars:
                if formula_operator.isNonBinary:
                    self.nonBinary_operators_list.append(char)

                self.operator_chars.append(char)
                self.formula_operators_dict[char] = formula_operator
        self.operator_priority_dict=dict(sorted(self.operator_priority_dict.items(), reverse=True))

    @classmethod
    def fromLogicConfig(cls,logicConfig:LogicConfig):
        Name="Albinos_"+logicConfig.NAME
        FormulaOperators=[]
        ttp=TruthTableProvider(logicConfig)
        bannedComb=ttp.getBannedCombination()

        for o in logicConfig.operators:
            FormulaOperators.append(FormulaOperator.fromOperator(o,logicConfig))
        return cls(Name,FormulaOperators,bannedComb)

    def to_dict(self):
            return {
            'NAME': self.name,
            'function_operators': [f.to_dict() for f in self.FormulaOperators],
            'BannedCombination': self.BannedCombination
        }
    
    def to_json(self):
        return json.dumps(self.to_dict(), ensure_ascii=False,indent=3,separators=(',', ':'))
    
    def save_to_file(self, file_path: str):
        json=self.to_json()
        with open(str(file_path), 'w') as f:
            f.write(json)
            
    @classmethod
    def from_dict(cls, data):
        name = data['NAME']
        function_operators = [FormulaOperator.from_dict(f) for f in data['function_operators']]
        BannedCombination=data['BannedCombination']
        return cls(name, function_operators,BannedCombination) 
    @classmethod
    def from_json(cls, json_str: str):
        data = json.loads(json_str)
        return cls.from_dict(data)
    
    @classmethod
    def load_from_file(cls, file_path: str):
        with open(file_path, 'r') as f:
            data = json.load(f)
        return cls.from_dict(data)
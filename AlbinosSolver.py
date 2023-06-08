from AlbinosConfig import *
from TreeNode import *
from itertools import groupby

class TreeSolverResult:
    def __init__(self,value1,value2):
        self.value1=value1
        self.value2=value2

class AlbinosSolver:
    def __init__(self,formula:str,config:AlbinosConfig):
        self.config=config
        self.binary_operator=config.nonBinary_operators_list
        self.strformula=self.prepareFormula(formula)

        self.formula=self.create_tree( self.strformula)
        self.clauses_list=[]
        self.variable_dict={}
        self.counter=1


    def prepareFormula(self,formula):
        formula=formula.replace('))',') )')
        formula=formula.replace('((','( (')
        formula=formula.replace('(', ' ( ').replace(')', ' ) ').replace('  ',' ')

        for o in self.config.FormulaOperators:
            c=o.chars[0]
            for char in o.chars:
                formula=formula.replace(char, c)
        for c in self.config.operator_chars:
            formula=formula.replace(f'{c}(','{c} (')
            while formula.count(f'{c}{c}') or formula.count(f'{c} {c}') or formula.count('  '):
               formula=formula.replace(f'{c} {c}', f'{c}').replace(f'{c} {c}', f'{c}')
               formula=formula.replace(f'{c}{c}', f'{c}').replace(f'{c}{c}', f'{c}').replace('  ',' ')
            formula=formula.replace(c, f' {c} ').replace('  ',' ').replace('  ',' ')
            formula=formula.replace(str.upper(c), f'{c}').replace('  ',' ')


        
        return formula


    def getRootNumber(self,root):
        if not root in self.variable_dict:
            number=self.counter
            self.counter+=2
            self.variable_dict.update({root:[number,number+1],number:root,number+1:root})
            for v in self.config.BannedCombination:
                self.clauses_list.append([number*v[0],(number+1)*v[1]])  
        else:
            number=self.variable_dict[root][0]
        return number
        
    def solve_level(self,root:TreeNode):
        if root.right== None and root.right==None:
            number=self.getRootNumber(root)
            return TreeSolverResult(number,number+1)
            
        rightNumbers=self.solve_level(root.right)    
        op=self.config.formula_operators_dict[root.value]

        if root.left==None:
            if not root.value in self.binary_operator:
                raise ValueError("Left node is none and value is not binary operator")
            number=self.getRootNumber(root)
            self.clauses_list+=op.solveFormula1([rightNumbers.value1,rightNumbers.value2,number])
            self.clauses_list+=op.solveFormula2([rightNumbers.value1,rightNumbers.value2,number+1])
            return TreeSolverResult(number, number+1)

        leftNumbers=self.solve_level(root.left)
        number=self.getRootNumber(root)
        self.clauses_list+=op.solveFormula1([leftNumbers.value1,leftNumbers.value2,rightNumbers.value1,rightNumbers.value2,number])
        self.clauses_list+=op.solveFormula2([leftNumbers.value1,leftNumbers.value2,rightNumbers.value1,rightNumbers.value2,number+1])
        return TreeSolverResult(number, number+1)

    def solve(self,ExpectedResult):
        result=self.solve_level(self.formula)
        self.addSearchResult(result, ExpectedResult)
        res = []
        [res.append(x) for x in self.clauses_list if x not in res] 
        return res

    def addSearchResult(self,result,ExpectedResult):
        if(ExpectedResult==None) or not ExpectedResult in ['T','U','F']:
            ExpectedResult='T'
        if ExpectedResult=='T':
            self.clauses_list.append([result.value1])
            self.clauses_list.append([result.value2])
        elif ExpectedResult =='U':
            self.clauses_list.append([result.value1])
            self.clauses_list.append([-result.value2])
        elif ExpectedResult == 'F':
            self.clauses_list.append([-(result.value1)])
            self.clauses_list.append([-(result.value2)])

    def convert_to_tree(self,formula):
        if isinstance(formula, TreeNode):
            return formula
        if len(formula)==1 and isinstance(formula[0], TreeNode):
            return formula[0]
        if len(formula)==1:
            return TreeNode(formula[0])
        stack=[]
        for key,value in self.config.operator_priority_dict.items():
            for char in value:
                if  char in formula:
                    tokens = [list(group) for key, group in groupby(formula, lambda x: x == char) if not key]

                    stack.append(tokens.pop())
                    maxLoop=len(tokens)+2
                    while maxLoop:
                        node=TreeNode(char)
                        node.right=self.convert_to_tree(stack.pop())
                        if not char in self.binary_operator:
                            node.left=self.convert_to_tree(tokens.pop())
                        stack.append(node)
                        if not len(tokens):
                            break
                        maxLoop-=1
                    return stack[0]

        
                

    def create_tree(self,formula):
        tokens=formula.split()
        tokens = [item for item in tokens if item.strip()]
        if (not formula.count(')')) and (not formula.count('(')):
            return self.convert_to_tree(tokens)
        stack=[]
        result=[]
       
        for token in tokens:
            if not len(stack) and token != '(':
                result.append(token)
                continue

            if token=='(':
                stack.append(token)
                continue

            if  token !=')':
                stack.append(token)
                continue

            new_formula=[]

            if stack.count('(') - stack.count(')')!=1:
                stack.append(token)
                continue

            while len(stack):
                el=stack.pop()
                if not stack.count('('):
                    new_formula=new_formula[::-1]
                    node=self.create_tree(' '.join(new_formula))
                    result.append(node)
                    break
                new_formula.append(el)

        return self.convert_to_tree(result)



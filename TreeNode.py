def NotNone(value):
    if value == None:
        return ""
    return value
class TreeNode:
    def __init__(self, value):
        self.left = None
        self.right = None
        self.value = value
    def __str__(self):
        if self.value==None:
            return ""      
        return str(NotNone(self.left))+" "+str(self.value)+" "+str(NotNone(self.right))
     
    def __eq__(self, other):
        return isinstance(other,TreeNode) and self.value == other.value and self.right == other.right and self.left == other.left

    def __hash__(self):
        return hash((self.value,hash(NotNone(self.right)),hash(NotNone(self.left))))

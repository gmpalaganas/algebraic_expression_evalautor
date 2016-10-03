class ASTNode:
    def __init__(self,token_type,value,children=None):
        self.type = token_type
        self.value = value

        if children:
            self.children = children
        else:
            self.children = []
	
    def toString(self,prefix=0):
        
        msg = ""

        if prefix > 0:
            msg += (prefix - 1) * "\t"

        msg = "AST Node \"%s\":\n" % self.type
        msg += prefix * "\t" + "Value: %s\n" % self.value 
        msg +=  prefix * "\t" +"Children:\n"
            
        if len(self.children) == 0:
            msg += prefix * "\t" + "\tNo Children\n"
        else:
            for child in self.children:
                msg += prefix * "\t" + "\t" + child.toString(prefix + 1)
            msg += "\n"

        return msg

    
    def __str__(self):
        return self.toString()

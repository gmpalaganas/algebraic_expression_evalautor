from numbers import Real

class Variable:
    def __init__(self,name,multiplier=1,exponent=1):
        self.name = name
        self.multiplier = multiplier
        self.exponent = exponent

    def __str__(self):
        ret = self.name

        if self.multiplier == 0:
            return '0'
        elif self.exponent == 0:
            return '1'

        if self.multiplier != 1:
            ret = str(self.multiplier) + ret

        if self.exponent != 1:
            ret = ret + '^' + str(self.exponent)

        return ret

    def __neg__(self):
        return Variable(self.name,-self.multiplier,self.exponent)
    
    def __add__(self,rhs):
        if isinstance(rhs,Variable):
            if self.get_exp_name() == rhs.get_exp_name():
                return Variable(self.name,self.multiplier + rhs.multiplier,
                        exponent=self.exponent)
            else:
                exp = AlgebExp()
                exp.add_variable(self)
                exp.add_variable(rhs)
                return exp 
        elif isinstance(rhs,AlgebExp):
            holder = rhs.copy()
            if rhs.variables.has_key(self.get_exp_name()):
                holder.variables[self.name] = rhs.variables[self.name] + self
            else:
                holder.add_variable(self)
            return holder
        elif isinstance(rhs,Real):
            holder = AlgebExp()
            holder = holder + self
            holder = holder + rhs
            return holder

    
    def __radd__(self,lhs):
        return self.__add__(lhs)

    def get_exp_name(self):
        ret = self.name

        if self.exponent != 1:
            ret += '^' + str(self.exponent)

        return ret

class AlgebExp:
    def __init__(self,constant=0,variables=None):
        self.constant = constant
        
        if variables == None:
            self.variables = {}
        else:
            self.variables = variables

    def __str__(self):
        ret = ''
        constant = self.constant
        keys = sorted(self.variables.keys())

        for i, variable in enumerate(keys):
            if str(self.variables[variable]) == '0':
                continue
            elif str(self.variables[variable]) == '1':
                constant += 1
            else:
                ret += str(self.variables[variable])
            
                if i < len(self.variables.keys()) - 1:
                    ret += '+'

        if self.constant != 0:
            ret += '+' + str(self.constant)
        
        return ret

    def __add__(self,rhs):
        if isinstance(rhs,Real):
            holder = self.copy()
            holder.constant += rhs
            return holder
        elif isinstance(rhs,Variable):
            return rhs + self.copy()
        elif isinstance(rhs,AlgebExp):
            holder = AlgebExp()
            holder.constant = rhs.constant + self.constant
            keys = self.variables.keys() + rhs.variables.keys()
            for key in keys:
                if holder.variables.has_key(key):
                    continue
                elif self.variables.has_key(key):
                    holder.add_variable(self.variables[key])

                    if rhs.variables.has_key(key):
                        holder.variables[key] = self.variables[key] + \
                                rhs.variables[key]
                else:
                    holder.add_variable(rhs.variables[key])

                    if self.variables.has_key(key):
                        holder.variables[key] = rhs.variables[key] + \
                                self.variables[key]


            return holder
    
    def add_variable(self,variable):
        if variable.get_exp_name() not in self.variables.keys():
            self.variables[variable.get_exp_name()] = variable
        else:
            raise NameError('Variable name already exists')
    
    def copy(self):
        return AlgebExp(self.constant,self.variables.copy())


x = Variable('x')
x1 = Variable('x',2,2)
x2 = Variable('x',1,3)

exp = x + x1
y = Variable('y')
exp2 = x + y
exp3 = x + x

print exp2.variables.keys()

print exp
print exp2
print exp3
print exp + exp2
print exp + exp3
print exp2 + exp3
print exp + exp2 + exp3

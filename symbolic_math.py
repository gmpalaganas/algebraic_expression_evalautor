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
        elif self.multiplier == -1:
            return '-' + self.name
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
            if self.exponent == rhs.exponent and self.name == rhs.name:
                return Variable(self.name,self.multiplier + rhs.multiplier,
                        exponent=self.exponent)
            else:
                exp = AlgebAddExp()
                exp.add_variable(self)
                exp.add_variable(rhs)
                return exp 
        elif isinstance(rhs,AlgebAddExp):
            holder = rhs.__class__.copy(rhs)
            if rhs.variables.has_key(self.get_exp_name()):
                holder.variables[self.get_exp_name()] = \
                        rhs.variables[self.get_exp_name()] + self
            else:
                holder.add_variable(self)
            return holder
        elif isinstance(rhs,Real):
            holder = AlgebAddExp()
            holder = holder + self
            holder = holder + rhs
            return holder

    def __sub__(self,rhs):
        return self + (-rhs)

    def __mul__(self,rhs):
        if isinstance(rhs,Real):
            holder = self.copy()
            holder.multiplier *= rhs

            if isinstance(holder.multiplier,float) and\
                    holder.multiplier.is_integer():
                holder.multiplier = int(holder.multiplier)

            return holder
        elif isinstance(rhs,Variable):
            holder = self.copy()
            if holder.name == rhs.name:
                holder.multiplier *= rhs.multiplier
                holder.exponent += rhs.exponent
                exp = AlgebMulExp()
                exp.add_variable(holder)
                return exp
            else:
                exp = AlgebMulExp(holder.multiplier * rhs.multiplier)
                exp.add_variable(holder)
                exp.add_variable(rhs)
                return exp
        elif isinstance(rhs,AlgebMulExp):
            exp = AlgebMulExp.copy(rhs)
            if exp.variables.has_key(self.name):
                exp.variables[self.name].exponent += self.exponent
            else:
                exp.add_variable(self)
            exp.constant *= self.multiplier
            return exp

    def __div__(self,rhs):
        if isinstance(rhs,Real):
            return self * (1/rhs)
        elif isinstance(rhs,Variable):
            holder = rhs.get_inverse()
            return self * holder
        elif isinstance(rhs,AlgebMulExp):
            holder = self.copy()
            return holder * rhs.get_inverse()

    def __rdiv__(self,lhs):
        return self.get_inverse() * lhs
 
    def __radd__(self,lhs):
        return self + lhs 

    def __rsub__(self,lhs):
        return lhs + (-self)

    def __rmul__(self,lhs):
        return self * lhs
   
    def get_exp_name(self):
        ret = self.name

        if self.exponent != 1:
            ret += '^' + str(self.exponent)

        return ret

    def get_abs_exp_name(self):
        holder = self.copy()
        holder.exponent = abs(holder.exponent)
        return holder.get_exp_name()

    def get_inverse(self):
        holder = self.copy()
        holder.multiplier = 1/float(holder.multiplier)
        holder.exponent = -holder.exponent
        return holder

    def copy(self):
        return Variable(self.name,self.multiplier,self.exponent)

class AlgebExp(object):

    def __init__(self,constant=0,variables=None):
        self.constant = constant

        if variables == None:
            self.variables = {}
        else:
            self.variables = variables

    
    @classmethod
    def copy(cls,instance):
        ret = cls(instance.constant)

        keys = instance.variables.keys()
        for key in keys:
            new_var = instance.variables[key].copy() 
            ret.add_variable(new_var)

        return ret

class AlgebAddExp(AlgebExp):

    def __init__(self,constant=0,variables=None):
        super(self.__class__, self).__init__(constant,variables)

    def __str__(self):
        ret = ''
        constant = self.constant
        keys = sorted(self.variables.keys())

        for i, key in enumerate(keys):
            if str(self.variables[key]) == '0':
                continue
            elif str(self.variables[key]) == '1':
                constant += 1
            else:
                ret += str(self.variables[key])
            
                if i < len(self.variables.keys()) - 1:
                    next_key = keys[i+1]
                    if self.variables[next_key].multiplier > 0: 
                        ret += '+'

        if self.constant != 0:
            if self.constant > 0:
                ret += '+'

            ret += str(self.constant)
        
        return ret
    
    def __neg__(self):
        holder = AlgebAddExp.copy(self)
        holder.constant = -holder.constant

        for key in holder.variables.keys():
            cur_var = holder.variables[key]
            cur_var.multiplier = -cur_var.multiplier

        return holder

    def __add__(self,rhs):
        if isinstance(rhs,Real):
            holder = AlgebAddExp.copy(self)
            holder.constant += rhs
            return holder
        elif isinstance(rhs,Variable):
            return rhs + AlgebAddExp.copy(self)
        elif isinstance(rhs,AlgebAddExp):
            holder = AlgebAddExp()
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
    
    def __sub__(self,rhs):
        return self + (-rhs)

    def __radd__(self,lhs):
        return self + lhs

    def __rsub__(self,lhs):
        return lhs + (-self)

    def add_variable(self,variable):
        if variable.get_exp_name() not in self.variables.keys():
            self.variables[variable.get_exp_name()] = variable.copy() 
        else:
            raise NameError('Variable name %s already exists' % variable.get_exp_name())

class AlgebMulExp(AlgebExp):

    def __init__(self,constant=1,variables=None):
        super(self.__class__, self).__init__(constant,variables)

    def __str__(self):
        top = ''
        bot = ''

        if self.constant == -1:
            top += '-'
        elif self.constant == 0:
            return '0' 
        elif self.constant != 1:
            top += str(self.constant)

        keys = self.variables.keys()
        
        for key in keys:
            if self.variables[key].exponent != 0:
                str_format = '%s'
                if abs(self.variables[key].exponent) != 1:
                    str_format = '(%s)'

                if self.variables[key].exponent > 0:
                    top += str_format % self.variables[key].get_exp_name()
                else:
                    bot += str_format % self.variables[key].get_abs_exp_name()

        ret = top
        if top == '':
            ret += '1'
        if bot != '':
            ret += '/%s' % bot

        return ret

    def __neg__(self):
        holder= AlgebMulExp.copy(self)
        holder.constant = -holder.constant
        return holder

    def __mul__(self,rhs):
        if isinstance(rhs,Real):
            holder = AlgebMulExp.copy(self)
            holder.constant *= rhs
            return holder
        elif isinstance(rhs,AlgebMulExp):
            holder = AlgebMulExp.copy(self)
            holder.constant *= rhs.constant
            keys = rhs.variables.keys()

            for key in keys:
                if holder.variables.has_key(key):
                    exponent = holder.variables[key].exponent + \
                            rhs.variables[key].exponent
                    holder.variables[key] = Variable(key,1,exponent)
                else:
                    holder.add_variable(rhs.variables[key])

            return holder
        elif isinstance(rhs,Variable):
            return rhs * self

    def __rmul__(self,lhs):
        return self * lhs

    def add_variable(self,variable):
        if variable.name not in self.variables.keys():
            self.variables[variable.name] = variable.copy() 
        else:
            raise NameError('Variable name %s already exists' % variable.name)

    def get_inverse(self):
        holder = AlgebMulExp.copy(self)
        holder.constant = 1/holder.constant

        keys = self.variables.keys()
        for key in keys:
            holder.variables[key].exponent = -holder.variables[key].exponent

        return holder

x    = Variable('x')
x1   = Variable('x',2,2)
x2   = Variable('x',1,3)
x3   = Variable('x',1,-1)
y    = Variable('y')
z    = Variable('z',20,100)
z2   = Variable('z',5,-2)
z3   = Variable('z',5,-1)

exp = x * y
exp2 = x * z
exp3 = x * x2
exp4 = z * z2

print exp.get_inverse()
print exp4.get_inverse()
print x / z3
print 2 / x
print 2 * x

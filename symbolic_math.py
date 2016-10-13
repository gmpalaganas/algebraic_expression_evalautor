from numbers import Real
import re

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
                exp = AddAlgebExp()
                exp.add_variable(self)
                exp.add_variable(rhs)
                return exp 
        elif isinstance(rhs,AddAlgebExp):
            holder = rhs.__class__.copy(rhs)
            if rhs.variables.has_key(self.get_exp_name()):
                holder.variables[self.get_exp_name()] = \
                        rhs.variables[self.get_exp_name()] + self
            else:
                holder.add_variable(self)
            return holder
        elif isinstance(rhs,Real):
            holder = AddAlgebExp()
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
                exp = MulAlgebExp()
                exp.add_variable(holder)
                return exp
            else:
                exp = MulAlgebExp(holder.multiplier * rhs.multiplier)
                exp.add_variable(holder)
                exp.add_variable(rhs)
                return exp
        elif isinstance(rhs,MulAlgebExp):
            exp = MulAlgebExp.copy(rhs)
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
        elif isinstance(rhs,MulAlgebExp):
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

class AddAlgebExp(AlgebExp):

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
        holder = AddAlgebExp.copy(self)
        holder.constant = -holder.constant

        for key in holder.variables.keys():
            cur_var = holder.variables[key]
            cur_var.multiplier = -cur_var.multiplier

        return holder

    def __add__(self,rhs):
        if isinstance(rhs,Real):
            holder = AddAlgebExp.copy(self)
            holder.constant += rhs
            return holder
        elif isinstance(rhs,Variable):
            return rhs + AddAlgebExp.copy(self)
        elif isinstance(rhs,AddAlgebExp):
            holder = AddAlgebExp()
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
    
    def empty(self):
        ret = self.constant == 0
        ret &= len(self.variables) == 0

        return ret


class MulAlgebExp(AlgebExp):

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

        keys = sorted(self.variables.keys())
        
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
        holder= MulAlgebExp.copy(self)
        holder.constant = -holder.constant
        return holder

    def __mul__(self,rhs):
        if isinstance(rhs,Real):
            holder = MulAlgebExp.copy(self)
            holder.constant *= rhs
            return holder
        elif isinstance(rhs,MulAlgebExp):
            holder = MulAlgebExp.copy(self)
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

    def __div__(self,rhs):
        if isinstance(rhs,Real):
            return self * (1/rhs)
        elif isinstance(rhs,Variable):
            return self * rhs.get_inverse()
        elif isinstance(rhs,MulAlgebExp):
            return self * rhs.get_inverse()

    def __rmul__(self,lhs):
        return self * lhs

    def __rdiv__(self,lhs):
        return self.get_inverse() * lhs

    def add_variable(self,variable):
        if variable.name not in self.variables.keys():
            self.variables[variable.name] = variable.copy() 
        else:
            raise NameError('Variable name %s already exists' % variable.name)

    def get_inverse(self):
        holder = MulAlgebExp.copy(self)
        holder.constant = 1/float(holder.constant)

        if isinstance(holder.constant,float) and holder.constant.is_integer():
            holder.constant = int(holder.constant)

        keys = self.variables.keys()
        for key in keys:
            holder.variables[key].exponent = -holder.variables[key].exponent

        return holder

    def empty(self):
        ret = self.constant == 0
        ret |= len(self.variables) == 0

        return ret

class ComplexAlgebExp:

    def __init__(self,add_exp=None,mul_exps=None):
        if add_exp == None:
            self.add_exp = AddAlgebExp()
        else:
            self.add_exp = add_exp

        if mul_exps == None:
            self.mul_exps = []
        else:
            self.mul_exps = mul_exps


    def __str__(self):
        parts = [] 
        
        if not self.add_exp.empty():
            parts = [ str(var) for var in self.add_exp.variables.values() ] 
        
        for mul_exp in self.mul_exps:
            parts.append(str(mul_exp))

        parts = sorted(parts, key=lambda x: re.sub('[^A-Za-z]+','',x))

        ret = parts[0]

        for part in parts[1:]:
            if part[0] != '-':
                ret+='+'

            ret+=part

        return ret

x  = Variable('x')
x1 = Variable('x',2,2)
x2 = Variable('x',1,3)
x3 = Variable('x',1,-1)
y  = Variable('y')
y2 = Variable('y',-2,3)
z  = Variable('z')
z2 = Variable('z',5,-2)
z3 = Variable('z',5,-1)
z4 = Variable('z',20,100)

add_exp = x - y + z
mul_exp = x * y2 * z
mul_exp2 = x * x

mul_exps = [mul_exp,mul_exp2]

complex_exp = ComplexAlgebExp(add_exp,mul_exps)

print add_exp
print mul_exp
print mul_exp2
print complex_exp

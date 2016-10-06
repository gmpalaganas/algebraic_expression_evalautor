# Algebraic Expression Evaluator

Takes an algebraic expression as input then evaluates it.

### Sample Inputs

* 2x + 2y = 2(x+y)
* 2x = x + x
* 2x = 2\*x
* 10 + 2
* 10 / 5
* 10.2 
* \_log(1000)
* 2^10
* 2(x + y\^2) + (2\+z)(xz \+ (2\^5)yz)

### Requirements

* Python 2.7.12 +
* ply 3.9

### Note on Variables

An increasing value for each unique variable is assigned as the original purpose of this program is to check the equality of 2 expressions with variables (i.e. `2x = x*x`)

So for now, expressions like `2x = 2` will return True

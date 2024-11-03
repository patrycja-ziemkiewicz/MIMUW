import math

class fraction:

    def __init__(self, numerator, denominator = 1) :
        assert denominator != 0 , "Denominator can't be 0"

        # Jeśli licznik jest zero, ustawiamy ułamek jako 0/1
        if numerator == 0:
            self.numerator = 0
            self.denominator = 1
        else:
            gcd = math.gcd(numerator, denominator)
            
            self.numerator = numerator // gcd
            self.denominator = denominator // gcd
            
            if self.denominator < 0:
                self.numerator *= -1
                self.denominator *= -1

    
    def __str__(self):
        if (self.denominator != 1):
            return f"{self.numerator}/{self.denominator}"
        else :
            return f"{self.numerator}"
        
    def __repr__(self):
        if (self.denominator != 1):
            return f"{self.numerator}/{self.denominator}"
        else :
            return f"{self.numerator}"

        
    def __add__ (self, other):
        new_denominator = math.lcm(other.denominator, self.denominator)
        new_numerator = (new_denominator // self.denominator) * self.numerator + \
              (new_denominator // other.denominator) * other.numerator
        
        return fraction(new_numerator, new_denominator)
    
    def __sub__ (self, other):
        new_denominator = math.lcm(other.denominator, self.denominator)
        new_numerator = (new_denominator // self.denominator) * self.numerator - \
              (new_denominator // other.denominator) * other.numerator
        
        return fraction(new_numerator, new_denominator)
        
    def __mul__(self, other):
        new_denominator = self.denominator * other.denominator
        new_numerator = self.numerator * other.numerator
        return fraction(new_numerator, new_denominator)
    
    def __truediv__(self, other):
        new_denominator = self.denominator * other.numerator
        new_numerator = self.numerator * other.denominator
        return fraction(new_numerator, new_denominator)
    
    def __eq__(self, other):
        return self.numerator == other.numerator and self.denominator == other.denominator
    
    def __lt__(self, other):
         lcm = math.lcm(other.denominator, self.denominator)
         return (lcm // self.denominator) * self.numerator < (lcm // other.denominator) * other.numerator
    
    def __le__(self, other):
        return self == other or self < other
    
    

def test(fraction1, fraction2):
    addition_result = fraction1 + fraction2
    print(f"{fraction1} + {fraction2} = {addition_result}")  

    # Test subtraction
    subtraction_result = fraction1 - fraction2
    print(f"{fraction1} - {fraction2} = {subtraction_result}")  

    # Test multiplication
    multiplication_result = fraction1 * fraction2
    print(f"{fraction1} * {fraction2} = {multiplication_result}")  

    # Test division
    division_result = fraction1 / fraction2
    print(f"{fraction1} / {fraction2} = {division_result}")  

    # Test comparison
    print(f"{fraction1} == {fraction2} : {fraction1 == fraction2}")  
    print(f"{fraction1} < {fraction2} : {fraction1 < fraction2}")    
    print(f"{fraction1} > {fraction2} : {fraction1 > fraction2}")   

fraction1 = fraction(23, 25) 
fraction2 = fraction(-5, 16)
test(fraction1, fraction2)



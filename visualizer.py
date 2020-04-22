import operator
import string
import numbers
import math

#----------------------------PARTIE CODE ---------------------------------------
class Computer:
    def __init__(self):
        self.operators = {"+": (operator.add, 2, "left"),
                     "-": (operator.sub, 2, "left"),
                     "*": (operator.mul, 3, "left"),
                     "/": (operator.truediv, 3, "left"),
                     "^": (pow, 5, "right"),
                     "sin":(math.sin, 4, "left"),
                     "tan":(math.tan, 4, "left"),
                     "cos":(math.cos, 4, "left"),
                     "exp":(math.exp, 4, "left"),
                     "log":(math.log, 4, "left"),
                     "hex":(self._converter, 4, "left"),
                     "bin":(self._converter, 4, "left"),
                     "oct":(self._converter, 4, "left")}

        self.bases = {"hex" : 16,
             "bin" : 2,
             "oct": 8}

# --------------------METHODES --------------------
#----------CONVERSION DES BASES (HEX, OCT, BIN) A DECIMAL ------------
    def _converter(self, _s, base):
        s = str(_s) 
        dotPos=s.find('.')
        if (dotPos == -1):
            return (int(s, base))
        places = len(s)-dotPos-1
        return (1.0*int(s[:dotPos]+s[dotPos+1:],base)/(base**places))
    
    

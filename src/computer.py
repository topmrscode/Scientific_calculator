'''
Objectif : implementer une calculatrice qui evalue les expressions mathematiques infixes et propose des fonctions mathematiques usuelles
    Methode :
    Shunting-yard algorithm : parse mathematical expressions specified in infix notation
    Librairies importees :
    - tkinter : implementation de l'interface graphique
    - operator : ajouter des operateurs et des bases
    - string : utilise pour sa constante string.digits
    - math : calcul des fonctions usuelles (sin, cos, tan...) 
    - numbers : utilise pour le type numbers.Real
'''
#----------------------------LIBRAIRIES  ---------------------------------------
import operator
import string
import numbers
import math

#----------------------------PARTIE CODE ---------------------------------------
class Computer:
    def __init__(self):
        # Un opérateur (fonction, priorité, associativité)
        self.operators = {
            "+": (operator.add, 2, "left"),
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
            "oct":(self._converter, 4, "left")
        }

        self.bases = {
            "hex" : 16,
            "bin" : 2,
            "oct": 8
        }

# --------------------METHODES --------------------

    '''
    Cette fonction convertie une expression depuis n importe quelle base en un nombre decimal (base 10)
    parametres :
    _s (string) : l'expression saisie
    base (string) : base choisie (Hex, oct, bin)
    return :
    float : valeur retorunee
    '''
    def _converter(self, _s, base):
        s = str(_s) 
        dotPos=s.find('.')
        if (dotPos == -1):
            return (int(s, base))
        places = len(s)-dotPos-1
        return (1.0*int(s[:dotPos]+s[dotPos+1:],base)/(base**places))
    
    '''
    Cette fonction separe les operateurs et les nombres de l'expression  
    
    parametres :
    expr (string) : l'expression 
    -> "123+123/10*cos(2)"
    
    Yield :
    token (generator) : return un generateur 
    -> [123, "+", 123, "/", 10, "*", "cos", "(", 2, ")"]
    '''
    def _separate(self, expr):
        last_is_digit = False 
        while expr != "" :
            if expr[0] in string.digits or expr[0] =="-" and last_is_digit == False: 
                try :
                    token, expr= self._find_digits(expr) 
                    last_is_digit = True
                except ValueError:
                    raise ValueError("error")
            elif expr[:3] in ["cos", "sin", "tan", "log", "exp", "hex", "oct", "bin"] : 
                token = expr[:3]
                expr = expr[3:]
                last_is_digit = False
            else : 
                token = expr[0]
                expr = expr[1:]
                last_is_digit = False
            yield token 

    '''
    Cette fonction gere les erreurs de parentheses (parentheses manquantes, male placees)
    
    parametres :
    tokens (list) : comprend notre expression parsee 
    -> ["(", "(", 10, "+", 10, ")"]
    
    Return :
    False or True (booleen) : False si erreur et True pour pas d erreur 
    '''
    def _check_braces(self, tokens):
        counter = 0
        for token in tokens:
            if token == "(":
                counter += 1
            elif token == ")":
                counter -= 1
            if counter < 0:
                return False
        if counter != 0:
            return False
        return True

    '''
    Cette fonction gere les erreurs (si ce n'est ni un chiffre, ni un operateurs ni une parenthese ouvrante et fermante, si le dernier element est un operateur, si on tape plus de 2 operateurs a la suite)
    parametres :
    tokens (list) : comprend notre expression 
    -> [123, "+", "+", "+", 123]
    Return :
    False or True (booleen) : False si erreur et True pour pas d erreur 
    '''
    def _check_tokens(self, tokens):
        if tokens[-1] in self.operators:
            return False
        ope_counter = 0
        for token in tokens:
            if token in self.operators:
                ope_counter += 1
            else:
                ope_counter = 0
            if ope_counter == 3:
                return False
            if isinstance(token,numbers.Real) == False and (token in self.operators) == False and token != "(" and token != ")":
                return False
        return True

    '''
    Cette fonction est appelee lorsaue l expression commence par un nombre positif ou negatif 
    parametres :
    expr (string) : comprend notre expression 
    -> "123+4"
    
    Return :
    res(int): le premier nombre 
    -> 123
    expr[i:](string) : le reste de notre expression
    -> "+4"
    '''
    def _find_digits(self, expr):
        rst = 0
        i = 0
        dot_found = False 
        is_negative = False
        nb_digits_after_dot = 1 
        if expr[0] == "-" :
            expr = expr[1:]
            is_negative = True
        while i < len(expr) and expr[i] in string.digits + "." :
            if expr[i] in string.digits:
                if dot_found == False :
                    rst = rst * 10 + int(expr[i])
                else :
                    rst = rst + (int(expr[i]) * 10**(-nb_digits_after_dot))  
                    nb_digits_after_dot = nb_digits_after_dot + 1
            else : 
                if dot_found == True :
                    raise ValueError("error")
                dot_found = True
            i = i + 1
        if is_negative == True:
            return rst * (-1), expr[i:]
        return rst, expr[i:]

    '''
    Cette fonction parse une expression mathematique en notation polonaise  
    parametres :
    expr (generator) : comprend notre expression
    remarque : le contenu du generateur va etre "copie" dans une liste afin de le parcourir 
    -> "123+4/2*cos(1)"
    
    Return :
    output(list): l expression en NPI 
    -> [123, 4, 2, "/", 1, "cos", "*", "+"]
    "" (string) : Indique si il y a une erreur ou non (Pas d erreur si vide) 
    '''
    def _shunting_yard(self, expr):
        output = []
        stack = []
        try :
            toks = self._separate(expr) 
            tokens = []
            for tok in toks :
                tokens.append(tok)
        except ValueError:
            return None, "Too many dots"
        #----- gestion derreurs -------
        if self._check_braces(tokens) == False:
            return None, "Mismatched braces"
        if self._check_tokens(tokens) == False:
            return None, "Malformated formula"
        #------------
        for token in tokens :
            if isinstance(token, numbers.Real) :
                output.append(token)
            elif token == "(":
                stack.append(token)
            elif token ==")":
                while stack[-1] !="(": 
                    output.append(stack.pop())
                stack.pop()
            elif token in self.operators.keys() :  
                fct, prior, assoc = self.operators[token] 
                while stack != [] and stack[-1] in self.operators.keys(): 
                    fct1, prior1, assoc1 = self.operators[stack[-1]] 
                    if assoc == "left" and prior <= prior1 or assoc == "right" and prior < prior1 :
                        output.append(stack.pop())
                    else :
                        break
                stack.append(token)
        while stack != []:
            output.append(stack.pop())
        return output, ""

    '''
    Cette fonction fait le calcul des operations
    parametres :
    output (list) : comprend notre expression en NPI
    -> [2, 2, "*", 3, "+"]
    
    Return :
    rst[0](float) : le resultat de l operation
    -> 7.0
    "" (string) : indique une erreur ou non
    -> "Malformated Formula", dans ce cas on returnera None
    '''
    def _calculate(self, output):
        rst = []
        for token in output :
            if token in self.operators.keys():
                if token in ["cos", "sin", "tan", "log", "exp"] :
                    try :
                        elem1 = rst.pop()
                    except IndexError :
                        return None, "Malformated Formula"
                    res = self.operators[token][0](elem1)
                    rst.append(res) 
                elif token in ["hex", "oct", "bin"] :
                    try :
                        elem1 = rst.pop()
                    except IndexError:
                        return None, "Malformated Formula"
                    res = self.operators[token][0](elem1, self.bases[token])
                    rst.append(res) 
                else:
                    try :
                        elem1 = rst.pop()  
                        elem2 = rst.pop() 
                    except IndexError:
                        return None, "Malformated Formula"
                    res = self.operators[token][0](elem2, elem1)
                    rst.append(res) 
            else :
                rst.append(float(token)) 
        return rst[0], ""
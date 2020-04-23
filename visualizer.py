from tkinter import *
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
    
    # etape 2 : SEPARER LES DIFFERENTS TOKENS (operateurs et nombres) -------------------------------
    def _separate(self, expr):
        last_is_digit = False # sert a gerer si le "- " est un negatif ou un operateur
        while expr != "" :
            if expr[0] in string.digits or expr[0] =="-" and last_is_digit == False: # si notre token a l index 0 est un nombre ou un -
                    token, expr= self._find_digits(expr) # token = -47.28 et expr = + 78 (cf. exemple)
                    last_is_digit = True
            elif expr[:3] in ["cos", "sin", "tan", "log", "exp", "hex", "oct", "bin"] : # je gere les sin cos et tan
                token = expr[:3]
                expr = expr[3:]
                last_is_digit = False
            else : # alors c est un operateur que l on stocke dans token et on le vire de notre input
                token = expr[0]
                expr = expr[1:]
                last_is_digit = False
            yield token # j ajoute mon token (nomnre si if ou operateur (else) ) a une liste "imaginaire"


    # etape 1 bis : Cette fonction est appeler a chaque fois que je sais que l input commence par un nombre positif ou negatif, 
    # elle renvoit le premier nombre ainsi que le reste de l expression

    # exemple : -47.28 + 78 
    # res = 0
    # on trouve un '-' -> on le supprime de notre chaine et retiens que l'on a eu un '-'
    # on trouve un 4 -> res = res * 10 (0) + 4 // res = 4
    # on trouve un 7 -> res = res * 10 (40) + 7 // res = 47
    # on trouve un . -> on le retiens pour la suite
    # on trouve un 2 -> on a trouve un point avant alors res = res + (2 * le nombre de chiffres apres la virgule ^ -10)
    # on trouve un 8 -> on a trouve un point avant alors res = res + (8 * le nombre de chiffres apres la virgule ^ -10)

    #enfin on a trouve un signe - au debut, alors on renvoie res * -1
    def _find_digits(self, expr):
        rst = 0
        i = 0
        dot_found = False 
        is_negative = False
        nb_digits_after_dot = 1 # nombre de chiffre apres la virgule
        if expr[0] == "-" :
            expr = expr[1:]
            is_negative = True
        while i < len(expr) and expr[i] in string.digits + "." :# tant que je parcour mon imput et que mon token a l edex i est un chiffre ou un point
            if expr[i] in string.digits:
                if dot_found == False :
                    rst = rst * 10 + int(expr[i])
                else :
                    rst = rst + (int(expr[i]) * 10**(-nb_digits_after_dot))  # rseltat + la puissance de 10 ^ nombre de chiffres apres virgules enregistrees
                    nb_digits_after_dot = nb_digits_after_dot + 1
            else : 
                if dot_found == True :
                    raise ValueError("error")
                dot_found = True
            i = i + 1
        if is_negative == True:
            return rst * (-1), expr[i:]
        return rst, expr[i:]

    #etape 3 : shunting_yard => 2 listes output et tmp = liste temporaire
    def _shunting_yard(self, expr):
        output = []
        stack = []
            toks = self._separate(expr) # toks est un generateur ( je ne peux la ppeler qune seule fois donc je le copie dans une liste)
            tokens = []
            for tok in toks :
                tokens.append(tok)
   
        # a : parcourir tous mes tokens
        for token in tokens :
            #b : 4 possibilites : 
                # - mom token est un nombre
                # - mom token est un operateur
                # - mom token est une parenthese ouvrante
                # - mom token est une parenthese fermante
            if isinstance(token, numbers.Real) :
                output.append(token)
            elif token == "(":
                stack.append(token)
            elif token ==")":
                while stack[-1] !="(": # tant que dans ma stack je trouve pas de parenthese ouvrante, je prend mon token (je destack ) et je le met dans l output
                    output.append(stack.pop())
                stack.pop()
            elif token in self.operators.keys() : # je regarde dans le dictionnaire operators et si mon token est une clefs 
                fct, prior, assoc = self.operators[token] # je recuperes les 3 valeurs de la clef qui correspond au token 
                while stack != [] and stack[-1] in self.operators.keys(): # tant que ma stack n est pas vide et que le dernier element est un operateur
                    fct1, prior1, assoc1 = self.operators[stack[-1]] # je recupere la fonction la prioriter et lasscoativite lie a cet operateur 
                    if assoc == "left" and prior <= prior1 or assoc == "right" and prior < prior1 :
                        output.append(stack.pop())
                    else :
                        break
                stack.append(token)
        # c: j ai parcouru tous mes tokens, je met les operateurs restants que j avais stocke dans la stack a la fin de  loutput 
        while stack != []:
            output.append(stack.pop())
        return output, ""

    #etape 4 : parcourir l output et faire les operations
    #  a : je parcours mon output,  2 posiibilites : des que je trouve un nombre je le met dans une liste result, des que je trouve un operateur je prend les derniers elements
    # de ma liste result et je fais loperation lie a l operateur
    def _calculate(self, output):
        rst = []
        for token in output :
            if token in self.operators.keys():
                if token in ["cos", "sin", "tan", "log", "exp"] :
                    elem1 = rst.pop()
                    res = self.operators[token][0](elem1)
                    rst.append(res) 
                elif token in ["hex", "oct", "bin"] :
                    elem1 = rst.pop()
                    res = self.operators[token][0](elem1, self.bases[token])
                    rst.append(res) 
                else:
                     elem1 = rst.pop() # je sors le premier element de ma list result 
                    elem2 = rst.pop() # idem pour le deuxieme
                    res = self.operators[token][0](elem2, elem1)
                    rst.append(res) # je recupere la fonction associe du dico et je lui donne en parametre les deux digits et je l ajoute dans mon result
            else :
                rst.append(float(token)) # float= ca fait un nombre decimal
        return rst[0], ""
            
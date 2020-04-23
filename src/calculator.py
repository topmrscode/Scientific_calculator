
#----------------------------LIBRAIRIES  ---------------------------------------
from tkinter import *
import computer

class Calculator:
    def _click_button(self,numbers):
        global operator
        global var
        self.operator = self.operator + str(numbers)
        self.var.set(self.operator)

    def _clear(self):
        self.entry.delete(0,END)
        self.operator =""

    def _evaluate(self):
        tokens, err = self.computer._shunting_yard(self.entry.get()) # je recupere l input et jappelle shunting yard
        if err != "": # shunting yard renvoit deux choses, le resultat et l erreur si l erreur est pas vide c est qui ya une erreur 
            self.answer = err # donc on veux pas aller plus loin
        else:
            res, err = self.computer._calculate(tokens) #sinon j appelle calculate qui renvoit un resultat et un erreur 
            if err != "":
                self.answer = err 
            else :
                self.answer = res
        self.var.set(self.answer)
        self.operator = str(self.answer)

    def _create_button(self, group, row, column, text, fnc):
        label_key = Label(group, bg='black')
        label_key.grid(row=row, column=column, padx=2, pady=2)
        button_key = Button(label_key ,text=text, font=('Helvetica', '16'), height=2, width=8,command=fnc)
        button_key.pack(side=LEFT)

    def _start(self):
        window.mainloop()

    def __init__(self,master):
        self.window = master
        self.computer = computer.Computer()

        self.operator = ""
        self.var = StringVar()
        frame_s = Frame(master, height=400, width=45 )
        frame_s.pack(side=TOP, fill=BOTH, expand=True)
        self.entry = Entry(frame_s,textvariable=self.var,bg='grey',width=70,bd=20,insertwidth=4,justify='right',font=('arial',16,'bold'))
        self.entry.pack()
        self.t = Text(self.entry,height=100)

        # -----group -----
        label_key = Label(window, height=15, width=30,bg='gray50')
        label_key.pack(side=LEFT, fill=BOTH, expand=True)

        label_fkey = Label(window, height=15, width=30, bg='gray25')
        label_fkey.pack(fill=BOTH, expand=True)

        # ------ boutton de gauche --------------------------------------------
        self._create_button(label_key, 0, 0, '7', lambda: self._click_button('7'))
        self._create_button(label_key, 0, 1, '8', lambda: self._click_button('8'))
        self._create_button(label_key, 0, 2, '9', lambda: self._click_button('9'))
        self._create_button(label_key, 1, 0, '4', lambda: self._click_button('4'))
        self._create_button(label_key, 1, 1, '5', lambda: self._click_button('5'))
        self._create_button(label_key, 1, 2, '6', lambda: self._click_button('6'))
        self._create_button(label_key, 2, 0, '1', lambda: self._click_button('1'))
        self._create_button(label_key, 2, 1, '2', lambda: self._click_button('2'))
        self._create_button(label_key, 2, 2, '3', lambda: self._click_button('3'))
        self._create_button(label_key, 3, 0, '0', lambda: self._click_button('0'))
        self._create_button(label_key, 3, 1, '.', lambda: self._click_button('.'))
        self._create_button(label_key, 3, 2, '=', self._evaluate)
        
        # button clear
        label_c = Label(label_key, bg='blue')
        label_c.grid(row=4, column=0, columnspan=3, pady=2)
        button_c = Button(label_c, text='Clear', font=('Helvetica', '16'), height=2, width=33,command= self._clear)
        button_c.pack(side=LEFT)

         # -----------  boutton de droite --------------------------------------------
        self._create_button(label_fkey, 0, 0, 'bin', lambda: self._click_button('bin('))
        self._create_button(label_fkey, 0, 1, 'oct', lambda: self._click_button('oct('))
        self._create_button(label_fkey, 0, 2, 'hex', lambda: self._click_button('hex('))
        self._create_button(label_fkey, 1, 0, 'sin', lambda: self._click_button('sin('))
        self._create_button(label_fkey, 1, 1, 'cos', lambda: self._click_button('cos('))
        self._create_button(label_fkey, 1, 2, '(', lambda: self._click_button('('))
        self._create_button(label_fkey, 2, 0, 'tan', lambda: self._click_button('tan('))
        self._create_button(label_fkey, 2, 1, 'log', lambda: self._click_button('log('))
        self._create_button(label_fkey, 2, 2, ')', lambda: self._click_button(')'))
        self._create_button(label_fkey, 3, 0, '+', lambda: self._click_button('+'))
        self._create_button(label_fkey, 3, 1, '-', lambda: self._click_button('-'))
        self._create_button(label_fkey, 3, 2, '^', lambda: self._click_button('^'))
        self._create_button(label_fkey, 4, 0, '*', lambda: self._click_button('*'))
        self._create_button(label_fkey, 4, 1, '/', lambda: self._click_button('/'))
        self._create_button(label_fkey, 4, 2, 'exp', lambda: self._click_button('exp('))

if __name__ == '__main__':
    window = Tk()
    window.title("My Calculator")

    c = Calculator(window)
    c._start()
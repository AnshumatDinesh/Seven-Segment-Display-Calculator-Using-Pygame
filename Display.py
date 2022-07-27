import pygame


def check(display_content):
    '''This Funtion checks if the numbers are exceeding the limit of the display'''
    if len(display_content) > 8:  # The seven segment display can only place 8 digits
        try:  # trying to adjust the number into scientific notation
            display_content = "{:.3e}".format(float(display_content))
        except OverflowError:  # if number is too big we replace with error
            display_content = "error"
    return display_content


class calc:
    '''A class for an instance of the calculator'''

    def __init__(self) -> None:
        self.info = {
            "Sprites": {
                "Horizontal bar": pygame.image.load("images\horizontal_bar.png"),
                "Vertical bar": pygame.image.load("images\Vertical_bar.png"),
                "Dot": pygame.image.load("images\dot.png"),
                "bg": pygame.image.load("images\Bg.png")
            },
            "Positions": {
                "A": ("Horizontal bar", (40, 10)),
                "B": ("Vertical bar", (84, 21)),
                "C": ("Vertical bar", (84, 75)),
                "D": ("Horizontal bar", (40, 118)),
                "E": ("Vertical bar", (29, 75)),
                "F": ("Vertical bar", (29, 21)),
                "G": ("Horizontal bar", (40, 64)),
                "DP": ("Dot", (100, 118))
            },
            "numbers": {
                "1": [False, True, True, False, False, False, False, False],
                "2": [True, True, False, True, True, False, True, False],
                "3": [True, True, True, True, False, False, True, False],
                "4": [False, True, True, False, False, True, True, False],
                "5": [True, False, True, True, False, True, True, False],
                "6": [True, False, True, True, True, True, True, False],
                "7": [True, True, True, False, False, False, False, False],
                "8": [True, True, True, True, True, True, True, False],
                "9": [True, True, True, True, False, True, True, False],
                "0": [True, True, True, True, True, True, False, False],
                ".": [False, False, False, False, False, False, False, True],
                "e": [True, False, False, True, True, True, True, False],
                "r": [False, False, False, False, True, False, True, False],
                "o": [False, False, True, True, True, False, True, False],
                "h": [False, True, True, False, True, True, True, False],
                "l": [False, False, False, True, True, True, False, False]
            },
            "implst": [["A", "B", "C", "D", "E", "F", "G", "DP"], ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]],
            "onscreen": "hell0"

        }
        self.run = True  # means calculator programm is working
        pygame.init()
        self.screen = pygame.display.set_mode((900, 500))
        self.screen.blit(self.info["Sprites"]["bg"],
                         (0, 0))  # placing the background
        self.n = ""
        self.write()
        pygame.display.update()

    def delete(self):
        '''Method To delete the contents of the display'''
        self.info["onscreen"] = ""
        self.screen.blit(self.info["Sprites"]["bg"], (0, 0))
        pygame.display.update()

    def correct(self):
        '''This function rectifies the erroneous placements of decimal points'''
        dup = list(self.info["onscreen"]
                   )  # storing the display string as a list
        b = ""
        for i in dup:
            b += i  # copying display string to b
        l = len(b)
        dot = False
        to_remove = []
        for i in range(0, l):
            # if a user has entered a decimal pint whilst one being present its location
            if dot and b[i] == ".":
                to_remove.append(i)  # is recorded in a list
            # if this is the first instance of dot the dot boolean is set to true
            elif not dot and b[i] == ".":
                dot = True
        ret = ""
        for i in to_remove:
            dup.pop(i)
        for i in dup:
            ret += i
        self.info["onscreen"] = ret

    def pow(self, n):
        '''Calculates power of number'''
        a = float(self.info["onscreen"])
        self.delete()
        self.info["onscreen"] = str(round(a**n, 2))
        self.write()

    def fact(self):
        '''Calculates the  factorial'''
        if(self.info["onscreen"] == ""):  # if no number is typed the value is taken as 0
            a = 0
        else:
            a = int(round(float(self.info["onscreen"])))
        self.delete()  # clearing the display
        fact = 1
        for i in range(1, a+1):
            fact *= i
        self.info["onscreen"] = str(fact)
        self.write()  # calling the write function

    def TurnOn(self, name, n=0):
        '''Truns on an segment in the display'''
        sprite = self.info["Positions"][name][0]
        self.screen.blit(self.info["Sprites"][sprite], (self.info["Positions"]
                         [name][1][0]+(105*n), self.info["Positions"][name][1][1]))
        pygame.display.update()

    def adddecimal(self, n=0):
        '''Turns on the decimal point LED'''
        if n > 0:
            sprite = self.info["Positions"]["DP"][0]
            self.screen.blit(self.info["Sprites"][sprite], (self.info["Positions"]
                             ["DP"][1][0]+(105*(n-1)), self.info["Positions"]["DP"][1][1]))
            pygame.display.update()

    def write(self):
        '''This Function writes the display string in Seven segment format'''
        lst = self.info["implst"][0]  # taking the names of LEDs into a list
        self.correct()  # rectifying mistakes in display string
        x = check(self.info["onscreen"])
        l = len(x)
        f = 0
        dec = 0
        for j in range(0, l):
            if x[j] == ".":
                if dec != 0:
                    f += 1
                else:
                    self.adddecimal(j)
                    f = 1
                    dec += 1
                continue
            for i in range(0, 8):
                if(x[j] != '+'):
                    if self.info["numbers"][x[j]][i]:
                        self.TurnOn(lst[i], j-(1*f))

    def store(self, op):
        "Stores the operation called"
        self.n += self.info["onscreen"]
        self.n += op
        self.delete()

    def equal(self):
        '''Evaluates the value after binary operations'''
        if self.info["onscreen"] == "":  # if only one number is provides ie in a+b only a is provided
            if self.n != "":
                # since the last letter was the operator we ommit
                self.info["onscreen"] == self.n[0:len(self.n)-1]
                self.write()  # that and write the a(first number) as it is
        else:
            self.n += self.info["onscreen"]
            self.delete()
            self.info["onscreen"] = str(eval(self.n))
            self.n = ""
            self.write()

    def button_press(self, pos):
        '''Detects which button is pressed by getting the loctaion of mouse'''
        if (pos[0] > 10 and pos[0] < 215):
            if pos[1] > 205 and pos[1] < 240:
                self.fact()
            elif pos[1] > 255 and pos[1] < 290:
                self.pow(-1)
            elif pos[1] > 305 and pos[1] < 340:
                self.info["onscreen"] += "7"
                self.write()
            elif pos[1] > 355 and pos[1] < 390:
                self.info["onscreen"] += "4"
                self.write()
            elif pos[1] > 405 and pos[1] < 440:
                self.info["onscreen"] += "1"
                self.write()
            elif pos[1] > 455 and pos[1] < 490:
                self.info["onscreen"] += "00"
                self.write()
        elif (pos[0] > 230 and pos[0] < 435):
            if pos[1] > 205 and pos[1] < 240:
                self.pow(3)
            elif pos[1] > 255 and pos[1] < 290:
                self.pow(2)
            elif pos[1] > 305 and pos[1] < 340:
                self.info["onscreen"] += "8"
                self.write()
            elif pos[1] > 355 and pos[1] < 390:
                self.info["onscreen"] += "5"
                self.write()
            elif pos[1] > 405 and pos[1] < 440:
                self.info["onscreen"] += "2"
                self.write()
            elif pos[1] > 455 and pos[1] < 490:
                self.info["onscreen"] += "0"
                self.write()
        elif (pos[0] > 450 and pos[0] < 655):
            if pos[1] > 205 and pos[1] < 240:
                self.pow(1/3)
            elif pos[1] > 255 and pos[1] < 290:
                self.pow(1/2)
            elif pos[1] > 305 and pos[1] < 340:
                self.info["onscreen"] += "9"
                self.write()
            elif pos[1] > 355 and pos[1] < 390:
                self.info["onscreen"] += "6"
                self.write()
            elif pos[1] > 405 and pos[1] < 440:
                self.info["onscreen"] += "3"
                self.write()
            elif pos[1] > 455 and pos[1] < 490:
                self.info["onscreen"] += "."
                self.write()
        elif (pos[0] > 670 and pos[0] < 875):
            if pos[1] > 205 and pos[1] < 240:
                self.delete()
            elif pos[1] > 255 and pos[1] < 290:
                self.store("/")
            elif pos[1] > 305 and pos[1] < 340:
                self.store("*")
            elif pos[1] > 355 and pos[1] < 390:
                self.store("+")
            elif pos[1] > 405 and pos[1] < 440:
                self.store("-")
            elif pos[1] > 455 and pos[1] < 490:
                self.equal()


inst = calc()
while inst.run:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                inst.run = False
            elif event.unicode == "0":
                inst.info["onscreen"] += "0"
                inst.write()
            elif event.unicode == "1":
                inst.info["onscreen"] += "1"
                inst.write()
            elif event.unicode == "2":
                inst.info["onscreen"] += "2"
                inst.write()
            elif event.unicode == "3":
                inst.info["onscreen"] += "3"
                inst.write()
            elif event.unicode == "4":
                inst.info["onscreen"] += "4"
                inst.write()
            elif event.unicode == "5":
                inst.info["onscreen"] += "5"
                inst.write()
            elif event.unicode == "6":
                inst.info["onscreen"] += "6"
                inst.write()
            elif event.unicode == "7":
                inst.info["onscreen"] += "7"
                inst.write()
            elif event.unicode == "8":
                inst.info["onscreen"] += "8"
                inst.write()
            elif event.unicode == "9":
                inst.info["onscreen"] += "9"
                inst.write()
            elif event.unicode == "+":
                inst.store("+")
            elif event.unicode == "-":
                inst.store("-")
            elif event.unicode == "*":
                inst.store("*")
            elif event.unicode == "/":
                inst.store("/")
            elif event.unicode == "=":
                inst.equal()
            elif event.unicode == "!":
                inst.fact()
            elif event.key == pygame.K_BACKSPACE:
                inst.delete()
        elif event.type == pygame.QUIT:
            inst.run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            inst.button_press(pygame.mouse.get_pos())

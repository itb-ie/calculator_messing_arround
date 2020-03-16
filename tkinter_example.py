import tkinter as tk
from functools import partial


class Calc(object):
    def __init__(self, window):
        self.window = window
        self.window.title("My calc")
        self.window.geometry("400x500")

        # what is the expression we want to compute?
        self.expression = ""
        self.new_number = True

        self.font_big = ("Courier", 30)
        self.font_small = ("Courier", 10)

        self.small_text_text = tk.StringVar()
        self.small_text = tk.Label(master=self.window, textvariable=self.small_text_text, font=self.font_small, width=30, anchor=tk.E)

        self.small_text_text.set("")

        self.big_text_text = tk.StringVar()
        self.big_text = tk.Label(master=self.window, textvariable=self.big_text_text, font=self.font_big, width=10, anchor=tk.E)

        self.big_text_text.set("0")

        # now add the buttons
        self.numbers_buttons = []
        for i in range(10):
            self.numbers_buttons.append(tk.Button(master=self.window, text=str(i), font=self.font_big, command=partial(self.number_press, str(i))))

        # add the operations
        self.oper = {"+": "+", "-": "-", "X": "*", "/": "//", "=": "="}
        self.oper_buttons = []
        for i in self.oper:
            self.oper_buttons.append(tk.Button(master=self.window, text=i, font=self.font_big, command=partial(self.oper_press, self.oper[i])))


        #layout
        self.small_text.grid(row=0, column=0, columnspan=4, pady=(20,0), sticky=tk.E)
        self.big_text.grid(row=1, column=0, columnspan=4, pady=(0,20), sticky=tk.E)
        for i in range(10):
            self.numbers_buttons[i].grid(column=i%3, row=i//3 + 2)
        for i, but in enumerate(self.oper_buttons):
            but.grid(column=3, row=i+2)

    def number_press(self, value="1"):
        if self.new_number:
            self.new_number = False
            self.big_text_text.set(value)
            return

        cur_value = int(self.big_text_text.get().replace(",", "")) * 10 + int(value)
        str_value = self.put_commas(cur_value)
        self.big_text_text.set(str_value)

    def oper_press(self, oper):

        self.expression = self.expression + self.big_text_text.get()
        if oper == "=":
            temp_expression = self.expression.replace(",", "")
            try:
                value = eval(temp_expression)
                self.big_text_text.set(self.put_commas(value))
            except ZeroDivisionError:
                self.big_text_text.set("Zero div")
            self.small_text_text.set(self.expression + oper + self.big_text_text.get())
            self.expression = ""
        else:
            self.expression = self.expression + oper
            self.small_text_text.set(self.expression)
        self.new_number = True

    def put_commas(self, cur_value):
        if cur_value < 0:
            negative = True
            cur_value = abs(cur_value)
        else:
            negative = False
        str_value = ""
        while cur_value:
            temp = str(cur_value % 1000)
            if cur_value >= 1000:
                if len(temp) == 1:
                    temp = "00" + temp
                elif len(temp) == 2:
                    temp = "0" + temp
            str_value = temp + "," + str_value
            cur_value = cur_value // 1000
        str_value = str_value[:-1]
        if negative:
            str_value = "-" + str_value
        return str_value


window = tk.Tk()
calc = Calc(window)
window.mainloop()

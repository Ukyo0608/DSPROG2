import flet as ft
import math

class CalcButton(ft.ElevatedButton):
    def __init__(self, text, button_clicked, expand=1):
        super().__init__()
        self.text = text
        self.expand = expand
        self.on_click = button_clicked
        self.data = text


class DigitButton(CalcButton):
    def __init__(self, text, button_clicked, expand=1):
        super().__init__(text, button_clicked, expand)
        self.bgcolor = ft.colors.WHITE24
        self.color = ft.colors.WHITE


class ActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        super().__init__(text, button_clicked)
        self.bgcolor = ft.colors.ORANGE
        self.color = ft.colors.WHITE


class ExtraActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        super().__init__(text, button_clicked)
        self.bgcolor = ft.colors.BLUE_GREY_100
        self.color = ft.colors.BLACK


class CalculatorApp(ft.Container):
    def __init__(self):
        super().__init__()
        self.reset()
        self.result = ft.Text(value="0", color=ft.colors.WHITE, size=40)
        self.width = 480
        self.bgcolor = ft.colors.BLACK
        self.border_radius = ft.border_radius.all(20)
        self.padding = 20

        self.content = ft.Column(
            controls=[
                ft.Row(controls=[self.result], alignment="end"),
                ft.Row(
                    controls=[
                        ExtraActionButton("AC", self.button_clicked),
                        ExtraActionButton("+/-", self.button_clicked),
                        ExtraActionButton("%", self.button_clicked),
                        ActionButton("/", self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton("7", self.button_clicked),
                        DigitButton("8", self.button_clicked),
                        DigitButton("9", self.button_clicked),
                        ActionButton("*", self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton("4", self.button_clicked),
                        DigitButton("5", self.button_clicked),
                        DigitButton("6", self.button_clicked),
                        ActionButton("-", self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton("1", self.button_clicked),
                        DigitButton("2", self.button_clicked),
                        DigitButton("3", self.button_clicked),
                        ActionButton("+", self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton("0", 2, self.button_clicked),
                        DigitButton(".", self.button_clicked),
                        ActionButton("=", self.button_clicked),
                    ]
                ),
                # Adding new row for trigonometric and other functions
                ft.Row(
                    controls=[
                        ActionButton("sin", self.button_clicked),
                        ActionButton("cos", self.button_clicked),
                        ActionButton("tan", self.button_clicked),
                        ActionButton("π", self.button_clicked),
                        ActionButton("x²", self.button_clicked),
                    ]
                ),
            ]
        )

    def button_clicked(self, e):
        data = e.control.data
        if self.result.value == "Error" or data == "AC":
            self.result.value = "0"
            self.reset()
        elif data in "0123456789.":
            if self.result.value == "0" or self.new_operand:
                self.result.value = data
            else:
                self.result.value += data
            self.new_operand = False
        elif data in "+-*/":
            if not self.new_operand:
                self.result.value = str(self.calculate(self.operand1, float(self.result.value), self.operator))
            self.operand1 = float(self.result.value)
            self.operator = data
            self.new_operand = True
        elif data == "=":
            if not self.new_operand:
                self.result.value = str(self.calculate(self.operand1, float(self.result.value), self.operator))
            self.reset()
        elif data == "%":
            self.result.value = str(float(self.result.value) / 100)
        elif data == "+/-":
            if float(self.result.value) != 0:
                self.result.value = str(-float(self.result.value))
        elif data == "π":
            self.result.value = str(math.pi)
        elif data == "x²":
            self.result.value = str(float(self.result.value) ** 2)
        elif data in ["sin", "cos", "tan"]:
            angle_rad = math.radians(float(self.result.value))
            if data == "sin":
                self.result.value = str(math.sin(angle_rad))
            elif data == "cos":
                self.result.value = str(math.cos(angle_rad))
            elif data == "tan":
                self.result.value = str(math.tan(angle_rad))
        self.update()

    def calculate(self, operand1, operand2, operator):
        if operator == '+':
            return operand1 + operand2
        elif operator == '-':
            return operand1 - operand2
        elif operator == '*':
            return operand1 * operand2
        elif operator == '/':
            return operand1 / operand2 if operand2 != 0 else "Error"

    def reset(self):
        self.operator = "+"
        self.operand1 = 0
        self.new_operand = True


def main(page: ft.Page):
    page.title = "Calc App"
    calc = CalculatorApp()
    page.add(calc)


ft.app(target=main)
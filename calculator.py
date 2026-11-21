def calculator():
    print("Калькулятор")
    print("Доступные операции: +, -, *, /")

    try:
        first_number = float(input("Введите первое число: "))
        operation = input("Введите операцию (+, -, *, /): ")
        second_number = float(input("Введите второе число: "))

        if operation == "+":
            result = first_number + second_number
        elif operation == "-":
            result = first_number - second_number
        elif operation == "*":
            result = first_number * second_number
        elif operation == "/":
            if second_number == 0:
                print("Ошибка: деление на ноль!")
                return
            result = first_number / second_number
        else:
            print("Ошибка: неизвестная операция.")
            return

        print("Результат:", result)

    except ValueError:
        print("Ошибка: введено некорректное число.")


if __name__ == "__main__":
    calculator()

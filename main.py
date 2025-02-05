""" Generate Password """

import random


LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
           'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E',
           'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
           'V', 'W', 'X', 'Y', 'Z']
NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
SYMBOLS = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

print("Welcome to the PyPassword Generator!")
nr_letters = int(input("How many letters would you like in your password?\n"))
nr_symbols = int(input("How many symbols would you like?\n"))
nr_numbers = int(input("How many numbers would you like?\n"))

password_string = ""


while True:
    random_type = random.randint(1, 3)

    if random_type == 1 and nr_letters > 0:
        password_string += random.choice(LETTERS)
        nr_letters -= 1

    if random_type == 2 and nr_numbers > 0:
        password_string += random.choice(NUMBERS)
        nr_numbers -= 1

    if random_type == 3 and nr_symbols > 0:
        password_string += random.choice(SYMBOLS)
        nr_symbols -= 1

    if nr_letters == nr_numbers == nr_symbols == 0:
        break

print(password_string)

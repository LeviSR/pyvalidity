from pyvalidity.Parser import Parser

print("Please enter an l-group (in)equation using the characters '^', 'v' for ",
      "meets, joins, respectively, prefixed '-' for inverses, and one-character ",
      "variables and capital letters for their inverse.")
print("E.g.: \nX v Y = -(x ^ y)\n(x ^ e)(x ^ e) <= Y(x ^ e)y")
print("\nYour Input: ")

while True:
    string = input()
    parsed = Parser(string).parse()
    print("The formula ", str(parsed), " you entered is " + "valid." if parsed.is_valid() else "invalid.")
    print("\nYour Input: ")

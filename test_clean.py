
from scientist import clean_python_code

test = "PLACEHOLDER"

test = test.replace("PLACEHOLDER", chr(96) * 3 + "python\nprint(123)\n" + chr(96) * 3)

result = clean_python_code(test)

print(repr(result))


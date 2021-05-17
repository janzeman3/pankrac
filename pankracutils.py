import datetime

## zjistií, jeslti jeden z listu je v textu
def obsahuje(word_list, expression):
    return any([True for word in word_list if word in expression])

## vrátí datum a čas v řetězci
def now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

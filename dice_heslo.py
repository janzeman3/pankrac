## diceware generování hesla
#  5x hodíš kostkou a podle toho, co Ti padne vybereš slovo
#  tohle uděláš 4x a v 80% mezer dáš čísla do 30
#  Celkově to je slušně zapamatovatelné heslo, které má sílu asi jako 10 znaků klasického nečitelného hesla
def get_password():
    dice_words = {}
    with open("diceware_wordlist_cz.txt", encoding="utf-8") as infile:
        for line in infile:
            key = line.split(" ")[0]
            if "\ufeff" in key:
                key = key.split("\ufeff")[1]
            word = line.split(" ")[1].split("\n")[0]
            dice_words[key] = word

    from random import random

    word_count = 4
    max_number = 30
    password = ""

    password = ""
    for words in range(word_count):
        key = ""
        for i in range(5):
            key = key + str(int(1+random()*6))
        password = password + dice_words[key] + " "

        if random()>0.75:
            password = password + str(int(random()*(max_number+1))) + " "
    return password

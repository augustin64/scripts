#!/usr/bin/python3
# max_score:392
import random
try:
    import enquiries
    choose = enquiries.choose
except:         # On offre une autre option si le module enquiries n'est pas installé
                # ce module n'étant pas compatible égaleent sur toutes les plateformes
    def choose(query,options):
        print(query)
        print("\n".join(["{}. {}".format(i+1,options[i]) for i in range(len(options))]))
        response = int(input("> "))
        return options[response-1]

morse = {
    "a":".-",
    "b":"-...",
    "c":"-.-.",
    "d":"-..",
    "e":".",
    "f":"..-.",
    "g":"--.",
    "h":"....",
    "i":"..",
    "j":".---",
    "k":"-.-",
    "l":".-..",
    "m":"--",
    "n":"-.",
    "o":"---",
    "p":".--.",
    "q":"--.-",
    "r":".-.",
    "s":"...",
    "t":"-",
    "u":"..-",
    "v":"...-",
    "w":".--",
    "x":"-..-",
    "y":"-.--",
    "z":"--..",
    "1":".----",
    "2":"..---",
    "3":"...--",
    "4":"....-",
    "5":".....",
    "6":"-....",
    "7":"--...",
    "8":"---..",
    "9":"----.",
    "0":"-----",
}
mnemotechnique = {
    "a":"Allô ?",
    "b":"Bonaparte",
    "c":"Coca-Cola",
    "d":"Dorémi",
    "e":"Euh..",
    "f":"Farandole",
    "g":"Golgotha",
    "h":"Himalaya",
    "i":"Ici",
    "j":"Jablonovo",
    "k":"Koalo",
    "l":"Limonade",
    "m":"Moto",
    "n":"Noé",
    "o":"Oporto",
    "p":"Philosophe",
    "q":"Quocorico",
    "r":"Ricola",
    "s":"Sapristi",
    "t":"Thon",
    "u":"Union",
    "v":"Valparéso",
    "w":"Wagon Long",
    "x":"Xtrocadéro",
    "y":"Yomamoto",
    "z":"Zoro est là",
}
mnemoschematik = {
    ".-": "Allô ?",
    "-...": "Bonaparte",
    "-.-.": "Coca-Cola",
    "-..": "Do-ré-mi",
    ".": "Euh..",
    "..-.": "Farandole",
    "--.": "Golgotha",
    "....": "Himalaya",
    "..": "Ici",
    ".---": "Jablonovo",
    "-.-": "Koalo",
    ".-..": "Limonade",
    "--": "Moto",
    "-.": "Noël",
    "---": "Oporto",
    ".--.": "Philosophe",
    "--.-": "Quocorico",
    ".-.": "Ricola",
    "...": "Sapristi",
    "-": "Thon",
    "..-": "Union",
    "...-": "Valparéso",
    ".--": "Wagon Long",
    "-..-": "Xtrocadéro",
    "-.--": "Yomamoto",
    "--..": "Zoro est là"
}

crs = [j for j in morse.keys()]

def multi_quiz(length=10):
    score = 0
    while True:
        clear_text = "".join([random.choice(crs) for i in range(length)])
        encoded = "/".join([morse[i] for i in clear_text])
        if input(encoded+"\n> ").lower() != clear_text:
            print("Faux ! La bonne réponse {}".format(clear_text))
            print("Votre score est de {} points".format(score))
            break
        else :
            score += length
            print("Bonne réponse ! Votre score est de {} points".format(score))

def int_quiz():
    score = 0
    while True:
        clear_text = random.choice(crs)
        if input(clear_text.upper()+"\n> ") != morse[clear_text]:
            if clear_text in mnemotechnique.keys():
                print("Faux ! La bonne réponse est {} [{}]".format(morse[clear_text],mnemotechnique[clear_text]))
            else:
                print("Faux ! La bonne réponse est {}".format(morse[clear_text]))
            print("Votre score est de {} points".format(score))
            break
        else:
            score +=1
            print("Bonne réponse ! Votre score est de {} points".format(score))

def quiz():
    score = 0
    while True:
        clear_text = random.choice(crs)
        if input(str(morse[clear_text])+"\n> ").lower() != clear_text:
            if clear_text in mnemotechnique.keys():
                print("Faux ! La bonne réponse est {}[{}]".format(clear_text,mnemotechnique[clear_text]))
            else:
                print("Faux ! La bonne réponse est {}".format(clear_text))
            print("Votre score est de {} points".format(score))
            break
        else:
            score +=1
            print("Bonne réponse ! Votre score est de {} points".format(score))

def quiz_junior():
    score = 0
    crs = [j for j in mnemoschematik.keys()]
    while True:
        memo = random.choice(crs)
        if input(str(mnemoschematik[memo])+"\n> ").lower() != memo:
            print("Faux ! La bonne réponse est {}".format(memo))
            print("Votre score est de {} points".format(score))
            break
        else:
            score +=1
            print("Bonne réponse ! Votre score est de {} points".format(score))

gamemodes = {
    "Junior":quiz_junior,
    "Intermédiaire":int_quiz,
    "Normal":quiz,
    "Expert":multi_quiz,
}
gm = choose("Choisissez votre mode de jeu",[i for i in gamemodes.keys()])
while True:
    gamemodes[gm]()
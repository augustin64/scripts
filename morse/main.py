#!/usr/bin/python3
# max_score:392
import sys
import random
import platform
from optparse import OptionParser

if platform.system() == "Windows":
    import msvcrt
    import time
else:
    from select import select

try:
    import enquiries

    choose = enquiries.choose
except:  # On offre une autre option si le module enquiries n'est pas installé
    # ce module n'étant pas compatible égaleent sur toutes les plateformes
    def choose(query, options):
        print(query)
        print(
            "\n".join(["{}. {}".format(i + 1, options[i]) for i in range(len(options))])
        )
        response = int(input("> "))
        return options[response - 1]


morse = {
    "a": ".-",
    "b": "-...",
    "c": "-.-.",
    "d": "-..",
    "e": ".",
    "f": "..-.",
    "g": "--.",
    "h": "....",
    "i": "..",
    "j": ".---",
    "k": "-.-",
    "l": ".-..",
    "m": "--",
    "n": "-.",
    "o": "---",
    "p": ".--.",
    "q": "--.-",
    "r": ".-.",
    "s": "...",
    "t": "-",
    "u": "..-",
    "v": "...-",
    "w": ".--",
    "x": "-..-",
    "y": "-.--",
    "z": "--..",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    "0": "-----",
}
mnemotechnique = {
    "a": "Allô ?",
    "b": "Bonaparte",
    "c": "Coca-Cola",
    "d": "Dorémi",
    "e": "Euh..",
    "f": "Farandole",
    "g": "Golgotha",
    "h": "Himalaya",
    "i": "Ici",
    "j": "Jablonovo",
    "k": "Koalo",
    "l": "Limonade",
    "m": "Moto",
    "n": "Noé",
    "o": "Oporto",
    "p": "Philosophe",
    "q": "Quocorico",
    "r": "Ricola",
    "s": "Sapristi",
    "t": "Thon",
    "u": "Union",
    "v": "Valparéso",
    "w": "Wagon Long",
    "x": "Xtrocadéro",
    "y": "Yomamoto",
    "z": "Zoro est là",
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
    "--..": "Zoro est là",
}

crs = [j for j in morse.keys()]


def diff(a, b):
    """
    Renvoie la différence, formattée en couleurs entre les chaînes de charactères a et b
    """
    if platform.system() != "Windows":
        s = ""
        if len(a) > len(b):
            b = b + " " * (len(a) - len(b))
        if len(b) > len(a):
            a = a + " " * (len(b) - len(a))
        for i in range(len(a)):
            if a[i] != b[i]:
                s += "\x1b[7;30;41m" + b[i]
            else:
                s += "\x1b[0m\x1b[7;30;42m" + b[i]
        s += "\x1b[0m"
        return s
    else:
        return b


def multi_quiz(length=10, timed=True, timeout=5):
    """
    Pouvant comporter un timer ou non, ce quiz renvoie "length" charactères encodés en morse à décoder
    """
    score = 0
    while True:
        clear_text = "".join([random.choice(crs) for i in range(length)])
        encoded = "/".join([morse[i] for i in clear_text])
        if timed:
            s = timed_input(encoded, timeout=length * timeout)
        else:
            s = input(encoded + "\n").lower()

        if s == TimeoutError:
            print("\nTemps écoulé, sois plus rapide la prochaine fois !")
        elif s != clear_text:
            print(f"Faux ! La bonne réponse : {clear_text}")
            print(f"Votre réponse était :     {diff(clear_text,s)}")
            print("Votre score est de {} points".format(score))
            break
        else:
            score += length
            print("Bonne réponse ! Votre score est de {} points".format(score))


def int_quiz(timed=True, timeout=10):
    """
    Pouvant comporter un timer ou non, ce quiz renvoie une lettre ou chiffre à encoder en morse
    """
    score = 0
    while True:
        clear_text = random.choice(crs)
        if timed:
            s = timed_input(clear_text.upper(), timeout=timeout)
        else:
            s = input(clear_text.upper() + "\n> ")
        if s == TimeoutError:
            print("Temps écoulé, sois plus rapide la prochaine fois !")
        elif s != morse[clear_text]:
            if clear_text in mnemotechnique.keys():
                print(
                    "Faux ! La bonne réponse est {} [{}]".format(
                        morse[clear_text], mnemotechnique[clear_text]
                    )
                )
            else:
                print("Faux ! La bonne réponse est {}".format(morse[clear_text]))
            print("Votre score est de {} points".format(score))
            break
        else:
            score += 1
            print("Bonne réponse ! Votre score est de {} points".format(score))


def quiz(timed=True, timeout=10):
    """
    Pouvant comporter un timer ou non, ce quiz renvoie un charactère en morse à décoder
    """
    score = 0
    while True:
        clear_text = random.choice(crs)
        if timed:
            s = timed_input(str(morse[clear_text]), timeout=timeout)
        else:
            s = input(str(morse[clear_text]) + "\n> ")
        if s == TimeoutError:
            print("Temps écoulé, sois plus rapide la prochaine fois !")
        elif s != clear_text:
            if clear_text in mnemotechnique.keys():
                print(
                    "Faux ! La bonne réponse est {}[{}]".format(
                        clear_text, mnemotechnique[clear_text]
                    )
                )
            else:
                print("Faux ! La bonne réponse est {}".format(clear_text))
            print("Votre score est de {} points".format(score))
            break
        else:
            score += 1
            print("Bonne réponse ! Votre score est de {} points".format(score))


def quiz_junior(timed=True, timeout=10):
    """
    Pouvant comporter un timer ou non, ce quiz renvoie un moyen mnémotechnique dont il faut extraire le morse
    """
    score = 0
    crs = [j for j in mnemoschematik.keys()]
    while True:
        memo = random.choice(crs)
        if timed:
            s = timed_input(mnemoschematik[memo], timeout=timeout)
        else:
            s = input(mnemoschematik[memo] + "\n> ")
        if s == TimeoutError:
            print("tmps écoulé, sois plus rapide la prochaine fois !")
        elif s != memo:
            print("Faux ! La bonne réponse est {}".format(memo))
            print("Votre score est de {} points".format(score))
            break
        else:
            score += 1
            print("Bonne réponse ! Votre score est de {} points".format(score))


def timed_input(prompt, timeout=10):
    if platform.system() != "Windows":
        print(prompt)
        sys.stdin.flush()
        rlist, _, _ = select([sys.stdin], [], [], timeout)
        if rlist:
            s = sys.stdin.readline()
            return s[:-1].lower()
        else:
            return TimeoutError
    else:
        sys.stdout.write(prompt + "\n")
        sys.stdout.flush()
        endtime = time.monotonic() + timeout
        result = []
        while time.monotonic() < endtime:
            if msvcrt.kbhit():
                result.append(msvcrt.getwche())
                if result[-1] == "\r":
                    return "".join(result[:-1])
            time.sleep(0.04)
        return TimeoutError


parser = OptionParser()
parser.add_option(
    "-g",
    "--gamemode",
    dest="gamemode",
    help="choose GAMEMODE",
    type="string",
    metavar="(JUNIOR|INTERMEDIAIRE|NORMAL|EXPERT)",
)
parser.add_option(
    "-T",
    "--timeout",
    action="store",
    dest="timeout",
    type="int",
    help="set TIMEOUT",
    metavar="TIMEOUT",
    default=5,
)
parser.add_option(
    "-d",
    "--disable-timer",
    action="store_false",
    dest="timed",
    help="Disable timer",
    default=True,
)
parser.add_option(
    "-l",
    "--length",
    dest="length",
    help="Nombre d'éléments, disponible uniquement pour le mode de jeu EXPERT",
    action="store",
    type="int",
    metavar="NOMBRE D'ELEMENTS",
    default=10,
)
(options, args) = parser.parse_args()

gamemodes = {
    "Junior": quiz_junior,
    "Intermédiaire": int_quiz,
    "Normal": quiz,
    "Expert": multi_quiz,
}
if options.gamemode != None:
    gamemodes = {
        "JUNIOR": quiz_junior,
        "INTERMEDIAIRE": int_quiz,
        "NORMAL": quiz,
        "EXPERT": multi_quiz,
    }
    if options.gamemode not in gamemodes:
        print(f"Option not available gamemode {options.gamemode}")
        raise ValueError
    else:
        gm = gamemodes[options.gamemode]
else:
    gm = gamemodes[
        choose("Choisissez votre mode de jeu", [i for i in gamemodes.keys()])
    ]

while True:
    if gm == multi_quiz:
        gm(timed=options.timed, timeout=options.timeout, length=options.length)
    else:
        gm(timed=options.timed, timeout=options.timeout)

#!/usr/bin/python3
import subprocess
import webbrowser

import requests
from bs4 import BeautifulSoup
from optparse import OptionParser

global headers
global parsed_options

# TODO:
# ✔ Ajouter une option pour ouvrir la page dans le navigateur
# ✔ Ouvrir automatiquement le premier résultat si il est le seul correspondant à la requête
# ✔ Ajouter des options en tant que flags avec optparser
# ✔ Ajouter un flag pour ouvrir le premier résultat sans intervention de l'utilisateur
# ✔ Ajouter un flag pour activer/désactiver l'affichage des paroles lors de la lecture (activé par défaut)

# Le module enquiries n'est pas compatible avec Windows,
# On définit donc une alternative si le module n'est pas installé

try:
    import enquiries

    choose = enquiries.choose
except:  # On offre une autre option si le module enquiries n'est pas installé
    # ce module n'étant pas compatible de manière égale sur toutes les plateformes
    def choose(query, options):
        print(query)
        print("\n".join(["{}".format(i) for i in options]))
        response = int(input("> "))
        return options[response - 1]


class Search:
    def __init__(self, title, options=None):
        self.title = title

    def getResults(self):
        url = "https://www.choralepolefontainebleau.org/?s=" + self.title
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content, "html.parser")
        # On récupère tous les items renvoyés sur la page web
        chants = soup.find_all("article", {"class": "post"})
        liste_chants = []
        for el in chants:
            titre_el = el.find("h2").find("a").text
            a = 12
            while "\n" in titre_el:
                titre_el = titre_el.replace("\n" + " " * a, "")
                a -= 1  # petite manip qui supprime les espaces superflus... à revoir pour faire quelque chose de plus propre
            lien_el = el.find("h2").find("a")["href"]
            rubriques_el = [
                {"title": i.text, "url": i["href"]} for i in el.find("p").find_all("a")
            ]

            liste_chants.append(
                Chant(
                    {
                        "title": titre_el,
                        "url": lien_el,
                        "rubriques": rubriques_el,
                    }
                )
            )

        self.results = liste_chants

    def choisirChant(self):
        if len(self.results) == 0:
            print("Aucun résultat pour '" + self.title + "'")
            exit(0)
        elif parsed_options.force_first:
            self.chant = self.results[0]
            return
        elif len(self.results) == 1:
            print(
                f"Un seul résultat est disponible, choix effectué automatiquement ({self.results[0].title})"
            )
            self.chant = self.results[0]
            return

        options = [
            str(i + 1)
            + ". "
            + self.results[i].title
            + "\n "
            + (" | ").join([j.title for j in self.results[i].rubriques])
            for i in range(len(self.results))
        ]

        print("\033[H\033[J")  # clear le terminal
        # L'utilisateur choisit le chant qu'il souhaite consulter
        chant = choose("Voici les résultats de votre recherche", options)
        # On récupère l'objet correspondant
        self.chant = self.results[int(chant.split(".")[0]) - 1]
        return


class Chant:
    def __init__(self, data):
        self.title = data["title"]
        self.url = data["url"]
        self.rubriques = [Rubrique(i) for i in data["rubriques"]]

    def getDetails(self):
        r = requests.get(self.url, headers=headers)
        self.soup = BeautifulSoup(r.content, "html.parser")

        self.getEnregistrements()
        self.getParoles()
        self.getPartitionUrl()

    def getEnregistrements(self):
        main = self.soup.find("main")
        noscript = main.find_all("noscript")

        self.enregistrements = []

        for division in noscript:
            for element in division.find_all("a"):
                self.enregistrements.append(
                    Upload({"title": element.text, "url": element["href"]}, self)
                )

    def getParoles(self):
        main = self.soup.find("main")
        paroles = main.find("div", {"class": "paroles"})
        self.paroles = Paroles(None)
        if paroles != None:
            paroles = "\n\n".join([j.text for j in paroles.find_all("p")]) + "\n"
            self.paroles = Paroles(paroles)
        else:
            h3 = main.find_all("h3")
            for i in h3:
                if i.text == "Paroles :":
                    paroles = (
                        "\n\n".join([j.text for j in i.parent.find_all("p")]) + "\n"
                    )
                    self.paroles = Paroles(paroles)
                    break

    def getPartitionUrl(self):
        main = self.soup.find("main")
        based_pld = main.find("div", {"class": "based-pld"})
        if based_pld != None:
            self.partition = Partition(based_pld.find("a")["href"])
        else:
            self.partition = Partition(None)

    def choisirAction(self):
        options = [
            self.enregistrements[i].title for i in range(len(self.enregistrements))
        ]

        if str(self.paroles) != "None":
            options.append("Consulter les paroles")
        if str(self.partition) != "None":
            options.append("Consulter la partition")
        options.append("Ouvrir dans le navigateur")
        options.append("Quitter")

        print("\033[H\033[J")  # clear le terminal
        # L'utilisateur choisit l'enregistrement qu'il souhaite consulter
        options = [str(i + 1) + ". " + options[i] for i in range(len(options))]
        display_text = f"Voici les données disponibles pour : {self.title}"
        if len(options) == 1:
            display_text = "Aucune donnée n'a pu être récupérée pour ce chant"
        self.choix = choose(display_text, options)
        self.enregistrement = Upload({"title": None, "url": None}, self)
        # On récupère l'objet correspondant
        if "Quitter" in self.choix:
            self.action = "quit"
        elif "Ouvrir dans le navigateur" in self.choix:
            self.action = "open_url"
        elif "Consulter les paroles" in self.choix:
            self.action = "paroles"
        elif "Consulter la partition" in self.choix:
            self.action = "partition"
        else:
            self.action = "enregistrement"
            self.enregistrement = self.enregistrements[
                int(self.choix.split(".")[0]) - 1
            ]

    def __repr__(self):
        return "chant:" + self.title

    def open_in_browser(self):
        webbrowser.open(self.url)


class Partition:
    def __init__(self, url):
        self.url = url

    def __repr__(self):
        return str(self.url)

    def open(self):
        webbrowser.open(self.url)


class Paroles:
    def __init__(self, paroles):
        self.content = paroles

    def __repr__(self):
        if self.content is None:
            return ""
        return str(self.content)

    def show(self):
        print(self.content)
        input("[Press <Enter> to continue]")


class Rubrique:
    def __init__(self, data):
        self.title = data["title"]
        self.url = data["url"]

    def __repr__(self):
        return "rubrique:" + self.title


class Upload:
    def __init__(self, data, parent):
        self.title = data["title"]
        self.url = data["url"]
        self.parent = parent

    def play(self):
        if parsed_options.afficher_paroles:
            print(self.parent.paroles)
        else:
            print("À l'écoute:", self.title, "\n")
        subprocess.call(["mpv", self.url])
        # à améliorer de manière à être compatible avec des systèmes n'ayant pas installé mpv

    def __repr__(self):
        return "upload:" + self.title


def quit():
    exit(0)


headers = {"User-Agent": "Python Client for CPPMF"}

parser = OptionParser()
parser.add_option(
    "-a",
    "--afficher-paroles",
    dest="afficher_paroles",
    help="Afficher les paroles lors de la lecture d'un audio",
    action="store_true",
    default=False,
)
parser.add_option(
    "-f",
    "--force-first",
    dest="force_first",
    help="Choisir automatiquement le premier chant",
    action="store_true",
    default=False,
)

(parsed_options, args) = parser.parse_args()

if len(args) == 0:
    query = input("Quelle est votre recherche ?\n> ")
else:
    query = " ".join(args)

search = Search(query, options=parsed_options)
search.getResults()
search.choisirChant()

chant = search.chant
chant.getDetails()
while True:
    chant.choisirAction()
    actions = {
        "enregistrement": chant.enregistrement.play,
        "paroles": chant.paroles.show,
        "partition": chant.partition.open,
        "open_url": chant.open_in_browser,
        "quit": quit,
    }
    actions[chant.action]()

#!/usr/bin/python3
import subprocess
import sys

import requests
from bs4 import BeautifulSoup

# Les modules suivant ne sont pas nécessaire pour toutes les actions,
# et ne sont donc qu'importés quand nécessaire:
#
# webbrowser
#

# Le module enquiries n'est pas compatible avec Windows,
# On définit donc une alternative si le module n'est pas installé

try:
    import enquiries
    choose = enquiries.choose
except:         # On offre une autre option si le module enquiries n'est pas installé
                # ce module n'étant pas compatible de manière égale sur toutes les plateformes
    def choose(query,options):
        print(query)
        print("\n".join(["{}".format(i) for i in options]))
        response = int(input("> "))
        return options[response-1]


class Search():
    def __init__(self, title) :
        self.title = title

    def getResults(self):
        url = "https://www.choralepolefontainebleau.org/?s=" + self.title
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        # On récupère tous les items renvoyés sur la page web
        chants = soup.find_all('article', {"class": "post"})
        liste_chants = []
        for el in chants :
            titre_el = el.find('h2').find('a').text
            a = 12
            while '\n' in titre_el :
                titre_el = titre_el.replace('\n'+' '*a,'')
                a-=1    # petite manip qui supprime les espaces superflus... à revoir pour faire quelque chose de plus propre
            lien_el = el.find('h2').find('a')['href']
            rubriques_el = [ {'title':i.text,'url':i['href']} for i in el.find('p').find_all('a')]

            liste_chants.append(Chant({
                'title':titre_el,
                'url':lien_el,
                'rubriques':rubriques_el,
                }))

        self.results = liste_chants

    def choisirChant(self):
        options = [ str(i+1)+'. '+self.results[i].title+'\n '+(' | ').join([j.title for j in self.results[i].rubriques]) for i in range(len(self.results)) ]

        if len(options) == 0:
            print("Aucun résultat pour '"+self.title+"'")
            exit(0)

        print("\033[H\033[J") # clear le terminal
        # L'utilisateur choisit le chant qu'il souhaite consulter 
        chant = choose('Voici les résultats de votre recherche',options)
        # On récupère l'objet correspondant
        self.chant = self.results[int(chant.split('.')[0])-1]

class Chant():
    def __init__(self,data):
        self.title = data['title']
        self.url = data['url']
        self.rubriques = [Rubrique(i) for i in data['rubriques']]

    def getDetails(self):
        r = requests.get(self.url,headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        main = soup.find('main')
        self.paroles = main.find('div', {"class": "paroles"})
        if self.paroles != None:
            self.paroles = self.paroles.text
        playlist = main.find('noscript').find_all('a')
        self.enregistrements = [Upload({'title':i.text,'url':i['href']}) for i in playlist]

        # TODO : ajouter le support pour les parole pour toutes les versions du site
        # (Cela a été fait pour certaines version du site, mais le HTML n'est pas uniforme sur toutes les pages)

        based_pld = main.find('div', {"class":"based-pld"})
        if based_pld != None:
            self.partition_url = based_pld.find('a')['href']
        else :
            self.partition_url = None

    def choisirAction(self):
        options = [self.enregistrements[i].title for i in range(len(self.enregistrements)) ]

        if self.paroles != None:
            options.append('Consulter les paroles')
        if self.partition_url != None:
            options.append('Consulter la partition')    
        options.append('Quitter')

        print("\033[H\033[J") # clear le terminal 
        # L'utilisateur choisit l'enregistrement qu'il souhaite consulter
        options = [str(i+1)+'. '+options[i] for i in range(len(options))]
        self.choix = choose('Voici les enregistrements disponibles',options)
        # On récupère l'objet correspondant

        if 'Quitter' in self.choix :
            self.action = "quit"
        elif 'Consulter les paroles' in self.choix:
            self.action = "paroles"
        elif 'Consulter la partition' in self.choix:
            self.action = "partition"
        else :
            self.action = "enregistrement"
            self.enregistrement = self.enregistrements[int(self.choix.split('.')[0])-1]

    def __repr__(self):
        return ('chant:'+self.title)

class Rubrique():
    def __init__(self,data):
        self.title = data['title']
        self.url = data['url']
    def __repr__(self):
        return ('rubrique:'+self.title)

class Upload():
    def __init__(self,data):
        self.title = data['title']
        self.url = data['url']

    def play(self):
        print("À l'écoute:",self.title,"\n")
        subprocess.call(['mpv',self.url])
        # à améliorer de manière à être compatible avec des systèmes n'ayant pas installé mpv

    def __repr__(self):
        return ('upload:'+self.title)


global headers
headers = {'User-Agent':'Python Client for CPPMF'}

if len(sys.argv) < 2:
    query = input("Quelle est votre recherche ?\n> ")
else :
    query = ' '.join(sys.argv[1:])

search = Search(query)
search.getResults()
search.choisirChant()

chant = search.chant
chant.getDetails()
while True :
    chant.choisirAction()
    if chant.action == "enregistrement":
        chant.enregistrement.play()
    elif chant.action == "paroles":
        print(chant.paroles)
        input("[Press Enter to continue]")
    elif chant.action == "partition":
        import webbrowser
        webbrowser.open(chant.partition_url)
    elif chant.action == "quit":
        exit(0)

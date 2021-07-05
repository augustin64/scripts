#!/usr/bin/python3
import subprocess
import sys

import enquiries
import requests
from bs4 import BeautifulSoup

# Le module enquiries n'est pas compatible avec Windows,
# l'idéal serait donc d'en trouver une alternative pour les
# les systèmes autres que Linux et MacOS

class Search():
    def __init__(self, title) :
        self.title = title

    def getResults(self):
        url = "https://www.choralepolefontainebleau.org/?s=" + self.title
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        # On récupère tous les items rzenvoyés sur la page web
        chants = soup.find_all('article', {"class": "post"})
        liste_chants = []
        for el in chants :
            titre_el = el.find('h2').find('a').text
            a = 12
            while '\n' in titre_el :
                titre_el = titre_el.replace('\n'+' '*a,'')
                a-=1    # petite manip qui supprime les espaces superflus... à revoir pour faire quelque chsoe de plus propre
            
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
        chant = enquiries.choose('Voici les résultats de votre recherche',options)
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
        playlist = main.find('noscript').find_all('a')
        self.enregistrements = [Upload({'title':i.text,'url':i['href']}) for i in playlist]

        # TODO : ajouter les paroles en tant qu'option

    def choisirEnregistrement(self):
        options = [ str(i+1)+'. '+self.enregistrements[i].title for i in range(len(self.enregistrements)) ]
        options.append(str(len(self.enregistrements)+1)+'. Quitter')
        print("\033[H\033[J") # clear le terminal 
        # L'utilisateur choisit l'enregistrement qu'il souhaite consulter
        choix = enquiries.choose('Voici les enregistrements disponibles',options)
        # On récupère l'objet correspondant
        if '. Quitter' in choix :
            exit(0)
        else :
            self.enregistrement = self.enregistrements[int(choix.split('.')[0])-1]

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

if len(sys.argv) < 1:
    query = input("Quel chant souhaites tu écouter ?\n> ")
else :
    query = ' '.join(sys.argv[1:])

search = Search(query)
search.getResults()
search.choisirChant()

chant = search.chant
chant.getDetails()
while True :
    chant.choisirEnregistrement()
    chant.enregistrement.play()

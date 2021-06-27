#!/usr/bin/python3
"""
Ce script a pour objectif de compter le nombre total d'heures passées pendant l'année sur un évènement précis.
Les données de ce calendrier doivent être dans un fichier `calendar.ics`, dans le même dossier que ce script.
La sortie se fait dans un fichier `output.csv`, qui peut être lu par excel, libre office calc ou tout autre tableur qui supporte le format csv.
"""
from icalendar import Calendar
import time
import csv
"""
Si il n'est pas déjà installé, le module `icalendar` est nécessaire à l'exécution de ce script
Pour l'installer, il faut exécuter la commande suivante :
`py -m pip install icalendar`
à noter : `py` peut varier allant de `python` à `python3` également selon votre OS
"""
output = './output.csv'
input = './calendar.ics'

g = open(input,'rb')

gcal = Calendar.from_ical(g.read())
dico = {}

for component in gcal.walk():
    if component.name == "VEVENT":
        if str(component.get('summary')) in dico :
            dico[str(component.get('summary'))] = dico[str(component.get('summary'))] + (component.get('dtend').dt - component.get('dtstart').dt)
        else :
            dico[str(component.get('summary'))] = component.get('dtend').dt - component.get('dtstart').dt
g.close()

doc = open(output , "w", encoding="utf-8")
doc.write("")
doc.close()

doc = open(output , "a", encoding="utf-8")

for i in dico.keys():

    towrite = str(i).encode('ascii', 'ignore')

    doc.write(towrite.decode('ascii'))
    doc.write(';')
    doc.write(str(dico[i]))
    doc.write("\n")
doc.close()

print(len(dico.keys()),'évènements écrits dans',output)

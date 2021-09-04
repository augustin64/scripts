# Morse

Ce script python permet de s'entraîner au morse 
 
### 4 "modes de jeu" sont disponibles :  
+ Junior: Le script renvoie un moyen mnémotechnique et demande en échange le code morse correspondant
+ Intermédiaire: Le script renvoie un caractère et demande l'encodage en morse de ce caractère
+ Normal: Le script renvoie un caractère encodé en morse et demande le caractère décodé
+ Expert: Le script renvoie une série de caractères encodés et demande la série décodée

### Usage: main.py [options]
```
Options:
  -h, --help            show this help message and exit

  -g (JUNIOR|INTERMEDIAIRE|NORMAL|EXPERT), --gamemode=(JUNIOR|INTERMEDIAIRE|NORMAL|EXPERT)
                        choose GAMEMODE

  -T TIMEOUT, --timeout=TIMEOUT
                        set TIMEOUT

  -d, --disable-timer   Disable timer

  -l NOMBRE D'ELEMENTS, --length=NOMBRE D'ELEMENTS
                        Nombre d'éléments, disponible uniquement pour le mode
                        de jeu EXPERT
```
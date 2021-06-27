"""
L'objectif de ce script est de pouvoir redireiger des e-mails
depuis sa boite mail vers un client de chat comme discord ou google chat
sans avoir à copier le mail à la main, mais en le faisant suivre à une certaine adresse, à laquelle se connecte ce script.
Ce projet utilise donc des webhooks, qui doivent être mis en place par l'utilisateur.
Il est possible de spécifier le salon vers lequel on souhaite transférer l'email.
Le projet ne prend pas en compte les pièces jointes pour le moment et n'est pas maintenu activement.
"""
# importation des modules nécessaires

import imaplib, email, time, mimetypes, csv
from email import policy
from email.parser import BytesParser, Parser

# dépendances google-chat

from json import dumps
from httplib2 import Http

# dépendances discord

from discord_webhook import DiscordWebhook, DiscordEmbed

# initialisation des variables

print('Running Script...')

show_sender_email = True

identifiant, password = 'email@du.bot', 'MotDePasse'

reload_time = 5 # temps à attendre entre deux rechargements de la page

data_path = "Lien_Relatif_Ou_Absolu_Vers_Un_Fichier_Texte_Vide_à_Première_Utilisation"

cards = False #Fonctionnalité Google chat à acvtiver ou non

# définition des fonctions

# connexion à la boite mail

def log_in(id,pd) :

    mail = imaplib.IMAP4_SSL('imap.gmail.com') # Serveur imap, gmail dans notre cas
    mail.login(id,pd)

    return(mail)

# récupération du dernier email

def get_mail(mail,rank=-1):
    mail.list()
    mail.select("inbox") # Se connecte à la boite mail
    data = mail.search(None, "ALL")[1]


    ids = data[0]
    id_list = ids.split()
    latest_email_id = id_list[rank] # On récupère le dernier e-mail


    # fetch the email body (RFC822) for the given ID
    data = mail.fetch(latest_email_id, "(RFC822)")[1]

    return(data[0][1]) # here's the body, which is raw text of the whole email

# récupération des informations de l'email

def get_info(email):

    msg = BytesParser(policy=policy.default).parsebytes(email)

    to = msg['to']
    sender =  msg['from']
    topic =  msg['subject']

    simplest = msg.get_body(preferencelist=('related', 'plain'))
    try :
        content = (''.join(simplest.get_content().splitlines(keepends=True)))
    except:
        content = (''.join(str(simplest).splitlines(keepends=True)))
    return(to,sender,topic,content)

# envoi du message via discord

def send_discord_webhook(email_info,retry=True,cards=True):

    print('Sending Webhook...')

    urls = {}
    urls['main'] = 'https://discordapp.com/api/webhooks/lienVersLe/Webhook_principal'
    urls['other'] = 'https://discordapp.com/api/webhooks/lienVersLe/Webhook_avec_sujet_other'

    text = ''

    url = ''

    for i in email_info[3] :
        if i != '\n' :
            text = text + i
        else :
            break

    for j in urls.keys() :
        if j in text.lower() :
            url = urls[j]

    if url == '' : url = urls['main']

    if len(text) > 2048 : # On découpe l'email si il dépasse la limite imposée par discord

        length = len(email_info[3])
        texts = []
        cptparts = 0
        line = 0
        i = 0

        while i < length and line < len(email_info[3].splitlines(True)):

            texts.append([])
            cptparts += 1
            j = 0
            while j < 2048 and line + 1 < len(email_info[3].splitlines(True)):

                texts[cptparts-1].append(email_info[3].splitlines(True)[line])
                j += len(email_info[3].splitlines(True)[line])
                line += 1

            texts[cptparts-1].remove(texts[cptparts-1][-1])

            j -= len(email_info[3].splitlines(True)[line])
            line -= 1
            i += j

        for k in range(len(texts)) :

            desc = ""
            for l in texts[k] :
                desc += l

            if desc != '' :

                if len(texts) > 1 :
                    title = email_info[2] + ' (' + str(k+1) + ')'

                else:
                    title = email_info[2]

                webhook = DiscordWebhook(url=url, username="Mailing Bot")
                embed = DiscordEmbed(title=email_info[1] + '\n' + title, description=desc , color=242424)
                webhook.add_embed(embed)
                status = webhook.execute()

                if str(status) == '[<Response [400]>]' :
                    None

    else :
        title = email_info[2]

        webhook = DiscordWebhook(url=url, username="Mailing Bot")
        embed = DiscordEmbed(title=email_info[1] + '\n' + title, description=email_info[3] , color=242424)
        webhook.add_embed(embed)
        status = webhook.execute()

        if str(status) == '[<Response [400]>]' :
            None



    # actuellement avec discord webhooks

# envoi du message sur google chat

def send_googlechat_webhook(email_info,card=True) :
    print('Sending Webhook...')

    urls = {}
    urls['main'] = 'https://chat.googleapis.com/v1/spaces/Webhook_Main'
    urls['other'] = 'https://chat.googleapis.com/v1/spaces/Webhook_Other'

    text = ''

    url = ''

    for i in email_info[3] :
        if i != '\n' :
            text = text + i
        else :
            break

    for j in urls.keys() :
        if j in text.lower() :
            url = urls[j]

    if url == '' : url = urls['main']

    if len(text) > 3072 :

        length = len(email_info[3])

        texts = []

        cptparts = 0

        line = 0

        i = 0

        while i < length and line < len(email_info[3].splitlines(True)):

            texts.append([])
            cptparts += 1
            j = 0
            while j < 3072 and line + 1 < len(email_info[3].splitlines(True)):

                texts[cptparts-1].append(email_info[3].splitlines(True)[line])
                j += len(email_info[3].splitlines(True)[line])
                line += 1

            texts[cptparts-1].remove(texts[cptparts-1][-1])

            j -= len(email_info[3].splitlines(True)[line])
            line -= 1

            i += j

        for k in range(len(texts)) : 

            desc = ""

            for l in texts[k] :
                desc += l

            if desc != '' :

                if len(texts) > 1 :
                    title = email_info[2] + ' (' + str(k+1) + ')'

                else:
                    title = email_info[2]

                if card :
                    bot_message = {
                        "cards": [
                            {
                                "header": {
                                    "title": email_info[1],
                                    "subtitle": title
                                },
                                "sections": [
                                    {
                                    "widgets": [
                                        {
                                        "textParagraph": {
                                            "text": email_info[3]
                                        }
                                        }
                                    ]
                                    }
                                ]
                            }
                        ]
                    }
                else :
                    bot_message = {
                    'text' : text}



                message_headers = {'Content-Type': 'application/json; charset=UTF-8'}

                http_obj = Http()

                http_obj.request(
                    uri=url,
                    method='POST',
                    headers=message_headers,
                    body=dumps(bot_message),
                )

                print('Webhook envoyé')

    else :

        title = email_info[2]

        text = email_info[1] + '\n\n' + title + '\n\n' + email_info[3]
        if card : 
            bot_message = {
                "cards": [
                    {
                        "header": {
                            "title": email_info[1],
                            "subtitle": title
                        },
                        "sections": [
                            {
                            "widgets": [
                                {
                                "textParagraph": {
                                    "text": email_info[3]
                                }
                                }
                            ]
                            }
                        ]

                    }
                ]
            }
        else :
            bot_message = {
            'text' : text}



        message_headers = {'Content-Type': 'application/json; charset=UTF-8'}

        http_obj = Http()

        http_obj.request(
            uri=url,
            method='POST',
            headers=message_headers,
            body=dumps(bot_message),
        )

        print('Webhook envoyé')

# structure générale de la récupération du dernier mail

def get_email_info_from_mailbox(idn,psd,show_sender_email_=True,rank=-1) :

    mailbox = log_in(idn, psd)

    raw_email = get_mail(mailbox,rank=rank)
    info = (get_info(raw_email))

    raw_email = info

    if not(show_sender_email_) :
        sender = ''
        for i in info[1] :
            if i != '<' :
                sender = sender + i

            else :
                info = (info[0],sender,info[2],info[3])
                break

    mailbox.logout()

    return (info)

# fonction principale, se chargeant d'appeler les autres

def __main__(identifiant,password,show_sender_email=True,reload_time=5,datapath='scriptdata',cards=True) :

    

    try :
        with open(datapath) as f:
            id = f.read()
            latest_email_id = eval(id)

    except :


        mail = log_in(identifiant,password)

        mail.list()
        mail.select("inbox") # connect to inbox.
        data = mail.search(None, "ALL")[1]


        ids = data[0]
        mailbox_list = ids.split() # ids is a space separated string

        mail.logout()

        doc = open(datapath , "w", encoding="utf-8")
        doc.write(str(mailbox_list[-1]))
        doc.close()

        latest_email_id = str(mailbox_list[-1])
    

    while True : 

        mail = log_in(identifiant,password)

        mail.list()
        mail.select("inbox") # connect to inbox.
        data = mail.search(None, "ALL")[1]


        ids = data[0]
        mailbox_list = ids.split() # ids is a space separated string

        print(mailbox_list)

        mail.logout()

        if str(mailbox_list[-1]) != str(latest_email_id) :
            if str(latest_email_id) != str(mailbox_list[-2]) :
                for j in range(len(mailbox_list)) :
                    if str(latest_email_id) != str(mailbox_list[-j-1]) :

                        email = get_email_info_from_mailbox(identifiant,password,show_sender_email_=show_sender_email,rank=-j-1)
                        print(mailbox_list[-j-1])
                        send_discord_webhook(email,card=cards)

                    else :
                        break

            else :
                email = get_email_info_from_mailbox(identifiant,password,show_sender_email_=show_sender_email,rank=-1)
                print(mailbox_list[-1])
                send_discord_webhook(email,card=cards)

            latest_email_id = mailbox_list[-1]

            doc = open(datapath , "w", encoding="utf-8")
            doc.write(str(latest_email_id))
            doc.close() 

        else : print('Mailbox is empty')

        time.sleep(reload_time)
        1/0

# démarrage du programme

__main__(identifiant,password,show_sender_email=show_sender_email,reload_time=reload_time,datapath=data_path,cards=cards)

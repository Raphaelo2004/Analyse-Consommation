#---------------------------------------------------------------------------------------------------------Bibliothèques----------------------------------------------------------------------------------------------------------------------------------

import mysql.connector            #import de la bibliothèque "mysql.connector"
import matplotlib.pyplot as plt   #import de la bibliothèque "matplotlib.pylot" comme "plt"
import numpy as np                #import de la bibliothèque "numpy" comme "np"
import datetime                   #import de la bibliothèque "datetime"  

#-------------------------------------------------------------------------------------------------------Fonctions----------------------------------------------------------------------------------------------------


#ces 3 fonctions vont nous servir pour la création de l'histogramme qui doit s'afficher que sur certaines periodes car on n'a pas accès a la consommation sur les autres jours
#mais aussi pour nous expliquer si il est possible d'étudier ces jours ou non

def jour():                   #fonction pour obtenir le jour désiré
    req=f"SELECT DAY({d})"    #on selectionne le jour dans la date choisie
    cursor.execute(req)       #le .execute permet de passer une commande SQL à la base.
    retour=cursor.fetchall()  #le . fetchall permet de récupérer tous les éléments de la base correspondant à la requête.
    retour=retour[0][0]       #on utilise la commande précédente pour séléctionner ce qui nous intéresse
    return retour             #renvoie le jour


 
def mois():                   #fonction pour obtenir le mois désiré
    req=f"SELECT MONTH({d})"  #on selectionne le mois dans la date choisie
    cursor.execute(req)       #le .execute permet de passer une commande SQL à la base.
    retour=cursor.fetchall()  #le .fetchall permet de récupérer tous les éléments de la base correspondant à la requête.
    retour=retour[0][0]       #on utilise la commande précédente pour séléctionner ce qui nous intéresse
    return retour             #renvoie le mois

def annee():                 #fonction pour obtenir l'année désiré
    req=f"SELECT YEAR({d})"  #on selectionne l'année dans la date choisie
    cursor.execute(req)      #le .execute permet de passer une commande SQL à la base.
    retour=cursor.fetchall() #le .fetchall permet de récupérer tous les éléments de la base correspondant à la requête.
    retour=retour[0][0]      #on utilise la commande précédente pour séléctionner ce qui nous intéresse
    return retour            #renvoie l'année


#fonctions pour avoir la consommation sur un jour ou un mois ou encore une année avec son histogramme

def Conso_Jour():                #fonction pour obtenir la consommation d'un certain jour
    jour = date_choisie          #le jour est la date choisie
    
    requete1="SELECT * FROM `conso_david` WHERE `Date` <=" + "'" + jour + "'" + "limit 2"     #on selectionne tout dans le fichier "conso_david" où la date est notre jour
    cursor.execute(requete1)                                                                  #on exécute la méthode avec le .execute (une commande SQL)       
    r=cursor.fetchall()                                                                       #on récupère les éleméments correspondant à la requete dans la base
    
    conso_heures_creuses_jour = r[0][1] - r[1][1]                            #on selectionne dans excel nos valeurs
    conso_heures_pleines_jour = r[0][2] - r[1][2]
    conso_total = conso_heures_creuses_jour + conso_heures_pleines_jour      #le total est la somme des heures creuses et pleines 
    
    print(f"Lors du {jour}, votre consommation est de : {conso_heures_creuses_jour} kWh en heures creuses, de {conso_heures_pleines_jour} kWh en heures pleines, et ainsi de {conso_total} kWh en tout.")
    conn.close()       #on ferme

def Conso_Mois():
    req=f"SELECT `index Heures creuses (kWh)`,`index Heures pleines (kWh)` FROM `conso_david` WHERE {annee()} = YEAR(`Date`) AND {mois()} =MONTH(`Date`)"      #on accède a la table par un requête sql
    cursor.execute(req)            #le .execute permet de passer une commande SQL à la base.
    retour=cursor.fetchall()       #le .fetchall permet de récupérer tous les éléments de la base correspondant à la requête.
    if mois() == 12:                                                                                                                                           #si c'est le 12eme mois
        req2=f"SELECT `index Heures creuses (kWh)`,`index Heures pleines (kWh)` FROM `conso_david` WHERE {annee()}+1 = YEAR(`Date`) AND 1 =MONTH(`Date`)"      #on sélectionne les heures creuses et pleines ou l'année +1 est égale à notre année et c'est le premier mois
        cursor.execute(req2)              #le .execute permet de passer une commande SQL à la base.
        retour2=cursor.fetchall()         #le .fetchall permet de récupérer tous les éléments de la base correspondant à la requête. 
    else:    
        req2=f"SELECT `index Heures creuses (kWh)`,`index Heures pleines (kWh)` FROM `conso_david` WHERE {annee()} = YEAR(`Date`) AND {mois()}+1 =MONTH(`Date`)"  # sinon pareil sauf que l'année doit etre la meme que celle choisie et le mois doit etre celui apres le notre
        cursor.execute(req2)         #le .execute permet de passer une commande SQL à la base.
        retour2=cursor.fetchall()    #le .fetchall permet de récupérer tous les éléments de la base correspondant à la requête.
    conso_heures_creuses_mois=retour2[-1][0]-retour[-1][0]
    conso_heures_pleines_mois=retour2[-1][1]-retour[-1][1]
    conso_total=conso_heures_creuses_mois + conso_heures_pleines_mois
    print(f"Lors du mois numéro {mois()} de l'année {annee()}, vore consommation est de : {conso_heures_creuses_mois} kWh en heures creuses, de {conso_heures_pleines_mois} kWh en heures pleines, et ainsi de {conso_total} kWh en tout.")


def Conso_Annee():
    req=f"SELECT `index Heures creuses (kWh)`,`index Heures pleines (kWh)` FROM `conso_david` WHERE {annee()} = YEAR(`Date`) AND 1+{i} = MONTH(`Date`)"  # on selectionne les heures pleines et creuses où l'annee est la même que celle choisie et où le mois est celui d'apres celui choisit
    cursor.execute(req)             #le .execute permet de passer une commande SQL à la base.
    retour=cursor.fetchall()        #le .fetchall permet de récupérer tous les éléments de la base correspondant à la requête.
    req2=f"SELECT `index Heures creuses (kWh)`,`index Heures pleines (kWh)` FROM `conso_david` WHERE {annee()} = YEAR(`Date`) AND 2+{i} = MONTH(`Date`)" # on selectionne les heures pleines et creuses où l'annee est la même que celle choisie et est 2 mois apres celui qui est choisit
    cursor.execute(req2)             #le .execute permet de passer une commande SQL à la base.
    retour2=cursor.fetchall()        #le .fetchall permet de récupérer tous les éléments de la base correspondant à la requête.
    conso_heures_creuses_annee=retour2[-1][0]-retour[-1][0]       #on sélectionne les valeurs correspondantes
    conso_heures_pleines_annee=retour2[-1][1]-retour[-1][1]
    total=conso_heures_creuses_annee + conso_heures_pleines_annee
    return conso_heures_creuses_annee,conso_heures_pleines_annee,total  #on renvoie les heures creuses,pleines et le total

def histogramme(liste1,liste2,liste3):          #création de l'histogramme
    if annee() == 2021:                                                                            #si l'année est 2021
        x = np.arange(9)                                                                           #on a une range de 9
        plt.xticks(x, ['Jan', 'Fév', 'Mars', 'Avril', 'Mai','Juin','Juil' , 'Aout' , 'Sept'])      #en abscisse on met les mois de janvier à septembre dans matplotlib
    elif annee() == 2018:                                #si l'année est 2018
        x = np.arange(2)                                 #on a une range de 2
        plt.xticks(x, ['Novembre' , ' Décembre'])        #en abscisse on met novembre et décembre dans matplolib
    else :                                                                                                        
        x = np.arange(12)                                                                                                #sinon on a 12 valeurs sur l'axe des abscisses
        plt.xticks(x, ['Janv', 'Fév', 'Mars', 'Avril', 'Mai','Juin','Juil' , 'Aout' , 'Sept' , ' Oct' , 'Nov' , ' Déc']) #Fixer les valeurs de l'axe X(abscisse) dans Matplotlib
    width = 0.1          #marge de 0.1
    plt.bar(x-0.2, liste1, width, color='blue')  # plt.bar pour tracer un diagramme en barre
    plt.bar(x, liste2, width, color='orange') 
    plt.bar(x+0.2, liste3, width, color='green')     
    plt.xlabel("Mois")                     #plt.xlabel pour nommer l'axe des absisse "Mois" dans Matplotlib
    plt.ylabel("Consomation (kWh)")        #plt.ylabel pour nommer l'axe des ordonnée "kWh" sur Matplotlib
    plt.legend(["Heures creuses", "Heures pleines", "Total consomation"])  # Ajoute une légende à l'endroit optimal à PyPlot
    plt.show()                     #plt. show() pour faire un évenement en boucle qui va afficher notre courbe
    
    conn.close() #on ferme 


#-------------------------------------------------------------------------------------Exécution------------------------------------------------------------------------------------------------------------------------


conn=mysql.connector.connect(host="localhost",user="root",password="",database="panneaux solaires")           #information sur la base de donnée de wampserver
cursor=conn.cursor()                                                                                          #on créer ici un objet « cursor » permettant d’avoir accès à différentes méthodes
date_choisie = input("Choisissez une date a étudier (AAAA-MM-JJ):")        #on choisie une date à étudier
d = date_choisie                                                           #on la renomme sous "d"
d="'"+d+"'"
date_max = datetime.date(2021,10,25)                        #on définie la date maximum possible à étudier
date_min = datetime.date(2018,10,27)                        #et aussi une minimum
date_possible = datetime.date(annee(),mois(),jour())        #Create a datetime object
liste1=[]  #on créer 3 listes pour stocker nos valeurs
liste2=[]
liste3=[]
if date_max < date_possible:                                                                                                      #on étudie à l'aide de la bibliothèque datetime les dates choisies
    print("Choisissez une date plus ancienne car aucune information n'est encore disponible pour cette date et celles à venir.")  #si la date est trop ancienne ou trop loin on les rediriges 
    exit()
elif date_min > date_possible:
    print("Choisissez une date plus récente car aucune information n'est disponible pour cette date et celles précédentes.")
    exit()
else:                   #sinon on leur demande ce qu'ils veulent étudier
    question = input("Tapez un numéro pour obtenir vos informations :\n 1 - Votre consommation annuel \n 2 - Votre consommation pour un mois \n 3 - Votre consommation pour un jour \n Vous avez saisie le numéro : ")
    if question == "1":         #si c'est sa consommation annuel
        if annee() == 2021:     #si l'année est 2021
            for i in range (9):   #boucle de 9 mois car seulement 9 mois avec des informations
                x=Conso_Annee()        # x = consommmation de notre année
                liste1.append(x[0])    #on ajoute a la liste 1 la premiere valeur de x
                liste2.append(x[1])    #on ajoute a la liste 2 la seconde valeur de x
                liste3.append(x[2])    #on ajoute a la liste 3 la troisième valeur de x
            print("Les mois d'Octobre, Novembre et Décembre ne sont pas pris car votre consommation s'arrete le 2021-10-25.")
        else:                       #sinon
            if annee() == 2018:     #si l'année est 2018
                i = 10              #10 mois
                x=Conso_Annee()     # x = consommmation de notre année
                liste1.append(x[0]) #on ajoute a la liste 1 la premiere valeur de x
                liste2.append(x[1]) #on ajoute a la liste 2 la seconde valeur de x
                liste3.append(x[2]) #on ajoute a la liste 3 la troisième valeur de x
                print("Seulement les mois de Novembre et de Décembre sont pris en compte car votre consomation commence le 2018-10-27.")
            
            else:                         #sinon boucle de 11 car 11 mois
                for i in range (11):
                    x=Conso_Annee()      # x = consommmation de notre année
                    liste1.append(x[0])  #on ajoute a la liste 1 la premiere valeur de x
                    liste2.append(x[1])  #on ajoute a la liste 2 la seconde valeur de x
                    liste3.append(x[2])  #on ajoute a la liste 3 la troisième valeur de x
            req=f"SELECT `index Heures creuses (kWh)`,`index Heures pleines (kWh)` FROM `conso_david` WHERE {annee()} = YEAR(`Date`) AND 12 = MONTH(`Date`)"
            cursor.execute(req)           #le .execute permet de passer une commande SQL à la base.
            retour=cursor.fetchall()      #le .fetchall permet de récupérer tous les éléments de la base correspondant à la requête.
            req2=f"SELECT `index Heures creuses (kWh)`,`index Heures pleines (kWh)` FROM `conso_david` WHERE {annee()}+1 = YEAR(`Date`) AND 1 = MONTH(`Date`)"
            cursor.execute(req2)       #le .execute permet de passer une commande SQL à la base.
            retour2=cursor.fetchall()  #le .fetchall permet de récupérer tous les éléments de la base correspondant à la requête.
            conso_creuses_annee=retour2[-1][0]-retour[-1][0]
            conso_pleines_annee=retour2[-1][1]-retour[-1][1]
            total_annee=conso_creuses_annee + conso_pleines_annee
            liste1.append(conso_creuses_annee)     #on ajoute les valeurs des heures creuses de l'année selectionnées dans les lignes précédentes dans la liste 1
            liste2.append(conso_pleines_annee)     #on ajoute les valeurs des heures pleines de l'année selectionnées dans les lignes précédentes dans la liste 2
            liste3.append(total_annee)             #on ajoute le total des deux dans la liste 3
        histogramme(liste1,liste2,liste3)       #on éxécute la fonction histogramme avec ces listes
    
    
    if question == "2":                           #si il veut sa consommation pour un mois
        if mois() <= 10 and annee() <= 2018:      
            print("On ne peut donc pas établire votre consomation sur tous le mois car les informations sur votre consomation commencent le 2018-10-27.")
            exit()
        elif mois() >= 10 and annee() >= 2021:
            print("On ne peut donc pas établire votre consomation sur tous le mois car les informations sur votre consomation s'arretent le 2021-10-25.")
            exit()
        else:
            Conso_Mois()   #on éxécute la fonction Conso_Mois
            
        
    if question == "3": #si il veut sa consommation pour un jour 
        Conso_Jour()    #on éxécute la fonction Conso_Jour
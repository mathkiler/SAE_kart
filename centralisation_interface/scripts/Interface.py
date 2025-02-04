
from scripts.setup_draw import setup_draw
from module_import import *
from components import *
from config import *
from utils.utils import *
from callbacks import *

class Interface :
    def __init__(self):
        self.mqtt_thread_handler = None
        #initialisation pygame (interface graphique) 
        pygame.init()
        pygame.display.set_caption("Tableau de bord Kart") #changement du titre de la fenêtre
        if tactile : #si on est en mode ecran tactile on enlève la souris de l'écran
            pygame.mouse.set_visible(False)

        #Ouverture de la fenêtre Pygame
        self.window = pygame.display.set_mode((800,480)) #création d'une fenêtre en 800x480 qui est la taille de l'écran utilisé par la rapsberry
        self.clock = pygame.time.Clock() #clock utile pour bloquer la boucle et limiter la vitesse (même principe que sleep du module time)

        self.index = 0 #clock d'indice pour effectuer des tâches periodiquement
        #dictionnaire des listes qui va contenir tout les object qui sont cliquable
        self.clickable_object = {
            "affichage" : [],
            "navigation" : [],
            "systeme" : []
        }
        #dictionnaire des listes qui va contenir tout les object à afficher
        self.container_storage = {
            "affichage" : {},
            "navigation" : {},
            "systeme" : {}
        }
        self.current_page = "affichage" #page à afficher
        #information utile pour gérer les clignotants
        self.clignotant = {"index_clignotant" : 1, #compteur pour changer l'etat du clignotant periodiquement
                           "cligno" : 1, #nombre d'acoup restant avant d'eteindre le clignotant
                           "etat" : False, #affiche l'etat du clignotant actuel
                           "allume" : None, #allume deviens "droite" ou "gauche" quand un clignotant est allumé. Sinon il reste en None
                           "start" : None #indique le temps avec time() au moment où le clignotant c'est déclanché
                           } 

        #paramètrage
        self.format_heure = "24h"
        self.temperature_unite = "°C"

        #variable importé des autre partie du projet SAE
        #une valeur par defaut est mise en attendant d'avoir des vrai informations
        self.vitesse = 17
        self.vitesse_consigne = 17
        self.temperature_batterie = 20
        self.temperature_moteur = 20
        setup_draw(self)

    #méthode pour déssiner les objets
    #tout les object sont dans des containers. chaque container à une méthode draw pour dessiner les object à l'interrieur. 
    #il est donc possible de mettre des container dans d'autre container
    def draw(self) :
        for container in self.container_storage[self.current_page].values() :
            container.draw(self.window)

    #boucle principale de l"interface
    def start(self) :
        while main_loop :
            self.index+=1
            #captation des evenement de la fenêtre : si un clic est effectué, ou une touche appuyé
            self.event_window()
            #Limitation de vitesse de la boucle
            self.clock.tick(fps) 
            #dessin de chaque objet
            self.draw()
            #test periodique de certain élément
            self.periodic_test()
            #Rafraîchissement de l'écran
            pygame.display.flip()

    #test periodique de certain élément
    def periodic_test(self) :
        #changepent d'etat des clignotant toute les 0.5 secondes (fps//2)
        if self.clignotant["index_clignotant"]%(fps//2) == 0 :
            self.clignotant["index_clignotant"] = 1
            update_clignotant(self)
        else :
            self.clignotant["index_clignotant"]+=1
        #toute les secondes on update l'heure
        if self.index % fps == 0:
            update_heure(self)
        #toute les 10 secondes on test si on est bine connecté au hotstop wifi
        if self.index % (fps*10) == 0 :
            test_connection(self)
            self.index = 0

    def event_window(self) :
        global main_loop
        #event du clavier/de la fenêtre
        keys = pygame.key.get_pressed() #on récupère tout les touches du clavier (keys[] = True si la touche est préssé)
        for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE] :   #Si on ferme la fenêtre, on sort de la boucle principal
                main_loop = False
            if event.type == MOUSEBUTTONDOWN : #appui
                if tactile:
                    # Convertir les coordonnées tactiles en pixels
                    X = int(event.x * pygame.display.get_surface().get_width())
                    Y = int(event.y * pygame.display.get_surface().get_height())
                else:
                    X, Y = event.pos  # Utiliser les coordonnées de la souris
                #pour chaque objet cliquable, on va dans la methode on_click
                for objt in self.clickable_object[self.current_page] :
                    objt.on_click((X, Y))
            elif event.type == MOUSEBUTTONUP : #relâchement
                if tactile:
                    # Convertir les coordonnées tactiles en pixels
                    X = int(event.x * pygame.display.get_surface().get_width())
                    Y = int(event.y * pygame.display.get_surface().get_height())
                else:
                    X, Y = event.pos  # Utiliser les coordonnées de la souris
                #pour chaque objet cliquable, on va dans la methode on_release
                for objt in self.clickable_object[self.current_page] :
                    objt.on_release((X, Y))
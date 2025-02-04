###############################################################################################
#
#
#
#               ░░▒▒       ▓▒▓▓▓▓▓▓▓▓░████▒░░░░▒▒▒▒░
#             ▒▓▓▓▓▓▓▒     █▓▓▓▓▓▓▓▓▓████▓░░░░░░▒▒▒▒░░░
#            ▓▓▓▓▓▓▒▓▒▒▒▒░▒▒▒▒▒▒▒▒▒▓█▓▒▓██▒░░░░░░▒░▒░░▒▒
#            ▒▓▒▓▓▒▓▓▓▓▒▒▒░░▒▒▒▒▒▒▓█▓▒▓▓██▓▒░░░░░░░▒░░░░░
#       ▒▓███▓███▓▓▓█▓▓▓▓▓▒▒▒▒▒▓▒▒▒▓▓██▓▓▓▓▓▓▒░░░░░░▒▒▒▒░▒█
#        ▓█▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▓▓▓▒▓▓███▓▒░░░░░░░░░▒█
#   ██████████▓▓▓███▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓██▓▓▓█▓▓▒░░░░░░░░░    ██▓▓▓▓▓
#█████▓▓▓▓███████▓███████▓▓▓▓▓▓▓▓▒▒▒▓▓▓▓▓█▓██▓▓▓▓▓▓▓▓▒░░░░░░░░███████▓▓██
#█▓██▓▓▒░░▒▓████████████████████▓▒░▒▒▒▒▓█▓▓█▓▒▒▒▓▓▓▓▓▒▒▒▒░░░░░▒▓█████████  ░░█
#█▓▓██▓▒▒▒░░▒▒▓███████████▓▓▓▓▓▓▒▒▒▒▒▒▒▓▓▒▓█▓▓▓▓▓█▓▓▓▓▓▒▒▒▒░░░▒░░▒▓█████▓▒▒░░░░
#  ▒██▓▒▒▒▒▒▒▒░▒▒▓▓█▓▓▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓████▓██▓▓▒▓▓▓▓▒▓▓▓▓▒▒░░░░░░░▒▒▒▒▒▒▒▒░░░░░
#  ▓███▒▒▒▒▒▓▒▒▒▒░░▓▓▓▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓████▓▓▓▓▒▒▓████▓▓▒▒░░░░░░░░░░░░░░░░░░░░▒
#    ██▓▒▒▒▒▒▒▒▒▒▒░▒█████▓▓▓▓▓▓███▓▓▓▓▓▓█▓▓▓▓▓▒▓▒▓▒▓▓▓▓▓▒▒▒▒░░░░░░░░░░░░░░▒▒▒░░░▒
#        ▒▒▒▒▒▒▒▒▒▒▓█████▓▓▓▓▓▓████▓▓█████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒░░░░░░░░░░░▒▒▒▒▒▒▒▒▒▒░▒
#           ▓▒▒▒▒▒▒██▓▒▒████████████▓▒▒▓▓███▓▓▓▓▓▒▓▓▓▒▒░░░░░░░░░░░░░░░░░░░░▒▒▒▒▒▒
#                ▒▒██▓▓▒▓██████████▓░░░░░░▒▒▒▒▒▓▒▒▒░░░░░░░░░░░▒▒░░░░░░▒▒▒▓▓▓▓▒▒▒█
#                  ██▓▒▒▒██████████▓▒▒░░░░░░░▒▒▒▒▒▒░░░░░░░░░░░░░░░░▒▒▓▓▓▓▓▓▓▓▒▒▒
#                   ███▓▓████████▓▒▒░▒▒▒▒░░░░░░░░░░░░░░░░░░░░░░▒▒▒▒▒▓▓▓▓▓▓▓█
#                     █████████▓  ▒▒▒▒░░░▒▒▒▒░░░░░░░░░░░░░░░▒▒▒▒▒▒▒▒▒▒█
#                                   ▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░▒▒▒███▓▒▒▓
#
#                             Interface par Mathieu
#
##############################################################################################








from module_import import *
from scripts import Interface, MQTTMessageHandler
from config import topics



# Point d'entrée principal du programme
if __name__ == "__main__" :
    # Initialisation de l'interface utilisateur
    interface = Interface()
    # Création et initialisation du gestionnaire de messages MQTT
    mqtt_thread_handler = MQTTMessageHandler(topics, interface)
    interface.mqtt_thread_handler = mqtt_thread_handler # Lier le gestionnaire MQTT à l'interface
    # Démarrage de l'interface utilisateur
    interface.start()
    #Sortie du programme
    os._exit(1)
    

    
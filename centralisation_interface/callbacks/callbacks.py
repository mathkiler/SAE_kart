from module_import import subprocess
from config import dark_light_mode, VITESSE_MAX

def callback_affichage_button(self_Interface) :
    self_Interface.current_page = "affichage"
    self_Interface.container_storage["affichage"]["Bouton Choix Page"].get_object("Affichage").state = "pressed"
    self_Interface.container_storage["affichage"]["Bouton Choix Page"].get_object("Navigation").state = "normal"
    self_Interface.container_storage["affichage"]["Bouton Choix Page"].get_object("Système").state = "normal"

def callback_navigation_button(self_Interface) :
    self_Interface.current_page = "navigation"
    self_Interface.container_storage["navigation"]["Bouton Choix Page"].get_object("Affichage").state = "normal"
    self_Interface.container_storage["navigation"]["Bouton Choix Page"].get_object("Navigation").state = "pressed"
    self_Interface.container_storage["navigation"]["Bouton Choix Page"].get_object("Système").state = "normal"

def callback_systeme_button(self_Interface) :
    self_Interface.current_page = "systeme"
    self_Interface.container_storage["systeme"]["Bouton Choix Page"].get_object("Affichage").state = "normal"
    self_Interface.container_storage["systeme"]["Bouton Choix Page"].get_object("Navigation").state = "normal"
    self_Interface.container_storage["systeme"]["Bouton Choix Page"].get_object("Système").state = "pressed"

def callback_eco_button(self_Interface) :
    if self_Interface.container_storage["affichage"]["Mode Conduite"].get_object("Eco").state != "pressed" :
        self_Interface.mqtt_thread_handler.publish_message("moteur/mode", "eco")
        self_Interface.container_storage["affichage"]["Mode Conduite"].get_object("Eco").state = "pressed"
        self_Interface.container_storage["affichage"]["Mode Conduite"].get_object("Normal").state = "normal"
        self_Interface.container_storage["affichage"]["Mode Conduite"].get_object("Sport").state = "normal"

def callback_normal_button(self_Interface) :
    if self_Interface.container_storage["affichage"]["Mode Conduite"].get_object("Normal").state != "pressed" :
        self_Interface.mqtt_thread_handler.publish_message("moteur/mode", "normal")
    self_Interface.container_storage["affichage"]["Mode Conduite"].get_object("Eco").state = "normal"
    self_Interface.container_storage["affichage"]["Mode Conduite"].get_object("Normal").state = "pressed"
    self_Interface.container_storage["affichage"]["Mode Conduite"].get_object("Sport").state = "normal"

def callback_sport_button(self_Interface) :
    if self_Interface.container_storage["affichage"]["Mode Conduite"].get_object("Sport").state != "pressed" :
        self_Interface.mqtt_thread_handler.publish_message("moteur/mode", "sport")
    self_Interface.container_storage["affichage"]["Mode Conduite"].get_object("Eco").state = "normal"
    self_Interface.container_storage["affichage"]["Mode Conduite"].get_object("Normal").state = "normal"
    self_Interface.container_storage["affichage"]["Mode Conduite"].get_object("Sport").state = "pressed"

#le bouton activation charge n'est finalement plus actif depuis le tableau de bord
def callback_charge_button(self_Interface) :
    if self_Interface.container_storage["affichage"]["Activation Charge"].get_object("Charge").state == "normal" :
        self_Interface.container_storage["affichage"]["Activation Charge"].get_object("Charge").state = "pressed"
        self_Interface.container_storage["affichage"]["Activation Charge"].get_object("Charge").text.text = "CHARGE ON"
        self_Interface.mqtt_thread_handler.publish_message("charge/control", "ON")
    else :
        self_Interface.container_storage["affichage"]["Activation Charge"].get_object("Charge").state = "normal"
        self_Interface.container_storage["affichage"]["Activation Charge"].get_object("Charge").text.text = "CHARGE OFF"
        self_Interface.mqtt_thread_handler.publish_message("charge/control", "OFF")

    
    
def callback_cameras_recule() :
    script_path = '/home/kartuser/SAE_kart/camera_recule/script.sh'
    try:
        print(f"Exécution du script en arrière-plan : {script_path}")
        # Lancer le script en arrière-plan (ne bloque pas le script principal)
        process = subprocess.Popen(["bash", script_path])
        return process
    except FileNotFoundError:
        print(f"Fichier non trouvé : {script_path}")
        return None
    except Exception as e:
        print(f"Erreur lors de l'exécution du script : {str(e)}")
        return None


def callback_detection_ligne_switch(etat, self_Interface) :
    if etat :
        self_Interface.mqtt_thread_handler.publish_message("aide/ligne_blanche/status", "ON")
    else :
        self_Interface.mqtt_thread_handler.publish_message("aide/ligne_blanche/status", "OFF")

def callback_detection_obstacle_switch(etat, self_Interface) :
    if etat :
        self_Interface.mqtt_thread_handler.publish_message("aide/obstacle/status", "ON")
    else :
        self_Interface.mqtt_thread_handler.publish_message("aide/obstacle/status", "OFF")

def callback_endormissement_switch(etat, self_Interface) :
    if etat :
        self_Interface.mqtt_thread_handler.publish_message("aide/endormissement/status", "ON")
    else :
        self_Interface.mqtt_thread_handler.publish_message("aide/endormissement/status", "OFF")



def callback_1224h_switch(state_switch, self_Interface) :
    if state_switch :
        self_Interface.format_heure = "24h"
    else :
        self_Interface.format_heure = "12h"

def callback_temperature_unite_switch(state_switch, self_Interface) :
    if state_switch :
        self_Interface.temperature_unite = "°C"
    else :
        self_Interface.temperature_unite = "°F"
    temperature_batterie = self_Interface.temperature_batterie
    temperature_moteur = self_Interface.temperature_moteur
    self_Interface.mqtt_thread_handler.publish_message("moteur/temperature", f"{temperature_moteur}")
    self_Interface.mqtt_thread_handler.publish_message("bms/temperature", f"{temperature_batterie}")

def callback_dark_liht_switch(state_switch, self_Interface) :
    if state_switch :
        dark_light_mode["etat"] = "dark"
    else :
        dark_light_mode["etat"] = "light"
    self_Interface.container_storage["affichage"]["Background"].get_object("Background Rectangle").change_color(dark_light_mode["background"][dark_light_mode["etat"]])
    self_Interface.container_storage["navigation"]["Background"].get_object("Background Rectangle").change_color(dark_light_mode["background"][dark_light_mode["etat"]])
    self_Interface.container_storage["systeme"]["Background"].get_object("Background Rectangle").change_color(dark_light_mode["background"][dark_light_mode["etat"]])
    for container in self_Interface.container_storage["affichage"].values() :
            container.update_color()
    for container in self_Interface.container_storage["navigation"].values() :
            container.update_color()
    for container in self_Interface.container_storage["systeme"].values() :
            container.update_color()

def callback_reg_lim_moins(self_Interface, etat) :
    image_object = self_Interface.container_storage["systeme"]["Regulateur"].get_object("Bouton Moins")
    if etat == "release" :
        image_object.change_image("systeme/normal_moins")
        if self_Interface.vitesse_consigne > 1 :
            self_Interface.vitesse_consigne-=1
            self_Interface.container_storage["systeme"]["Regulateur"].get_object("Vitesse Consigne").text = self_Interface.vitesse_consigne
            self_Interface.mqtt_thread_handler.publish_message("aide/vitesse_consigne", f"{self_Interface.vitesse_consigne}")
    elif etat == "click" :
        image_object.change_image("systeme/pressed_moins")
    elif etat == "release_outside" :
        image_object.change_image("systeme/normal_moins")

def callback_reg_lim_plus(self_Interface, etat) :
    image_object = self_Interface.container_storage["systeme"]["Regulateur"].get_object("Bouton Plus")
    if etat == "release" :
        image_object.change_image("systeme/normal_plus")
        if self_Interface.vitesse_consigne < VITESSE_MAX :
            self_Interface.vitesse_consigne+=1
            self_Interface.container_storage["systeme"]["Regulateur"].get_object("Vitesse Consigne").text = self_Interface.vitesse_consigne
            self_Interface.mqtt_thread_handler.publish_message("aide/vitesse_consigne", f"{self_Interface.vitesse_consigne}")
    elif etat == "click" :
        image_object.change_image("systeme/pressed_plus")
    elif etat == "release_outside" :
        image_object.change_image("systeme/normal_plus")


def callback_reg_switch(self_Interface, etat) :
    if etat == "click" :
        image_object = self_Interface.container_storage["systeme"]["Regulateur"].get_object("Switch Limitateur Regulateur Container").get_object("Switch Reg")
        if image_object.image_path == "systeme/switch_regulateur" :
            return
        image_object.change_image("systeme/switch_regulateur")
        self_Interface.container_storage["systeme"]["Regulateur"].get_object("Switch Limitateur Regulateur Container").get_object("Switch Reg").size = (72, 68)
        #activation des options de vitesse de consigne
        self_Interface.container_storage["systeme"]["Regulateur"].get_object("Bouton Moins").show = True
        self_Interface.container_storage["systeme"]["Regulateur"].get_object("Vitesse Consigne").show = True
        self_Interface.container_storage["systeme"]["Regulateur"].get_object("Bouton Plus").show = True
        self_Interface.mqtt_thread_handler.publish_message("aide/reg_lim", "activation regulateur")

def callback_neutre_witch(self_Interface, etat) :
    if etat == "click" :
        image_object = self_Interface.container_storage["systeme"]["Regulateur"].get_object("Switch Limitateur Regulateur Container").get_object("Switch Reg")
        if image_object.image_path == "systeme/switch_neutre" :
            return
        image_object.change_image("systeme/switch_neutre")
        self_Interface.container_storage["systeme"]["Regulateur"].get_object("Switch Limitateur Regulateur Container").get_object("Switch Reg").size = (72, 68)
        #activation des options de vitesse de consigne
        self_Interface.container_storage["systeme"]["Regulateur"].get_object("Bouton Moins").show = False
        self_Interface.container_storage["systeme"]["Regulateur"].get_object("Vitesse Consigne").show = False
        self_Interface.container_storage["systeme"]["Regulateur"].get_object("Bouton Plus").show = False
        self_Interface.mqtt_thread_handler.publish_message("aide/reg_lim", "desactivation")
    
def callback_lim_switch(self_Interface, etat) :
    if etat == "click" :
        image_object = self_Interface.container_storage["systeme"]["Regulateur"].get_object("Switch Limitateur Regulateur Container").get_object("Switch Reg")
        if image_object.image_path == "systeme/switch_limitateur" :
            return
        image_object.change_image("systeme/switch_limitateur")
        self_Interface.container_storage["systeme"]["Regulateur"].get_object("Switch Limitateur Regulateur Container").get_object("Switch Reg").size = (72, 68)
        #activation des options de vitesse de consigne
        self_Interface.container_storage["systeme"]["Regulateur"].get_object("Bouton Moins").show = True
        self_Interface.container_storage["systeme"]["Regulateur"].get_object("Vitesse Consigne").show = True
        self_Interface.container_storage["systeme"]["Regulateur"].get_object("Bouton Plus").show = True
        self_Interface.mqtt_thread_handler.publish_message("aide/reg_lim", "activation limitateur")
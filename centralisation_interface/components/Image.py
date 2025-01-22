from module_import import *
from config import *
from utils.utils import *


class Image :
    def __init__(
            self,
            label: str,  # Nom de l'objet pour le récupérer facilement
            image_path: str,  # Chemin de l'image de l'icône (facultatif)
            show: bool, 
            callback_action: callable,  # Fonction appelée lors d'un clic
            **kwargs  # Paramètres supplémentaires
    ):
        self.label = label
        self.show = show
        self.position = (0,0)
        self.kwargs = kwargs
        # Callback
        self.callback_action = callback_action
        # Surface de texte et rectangle associé
        self.image_path = image_path
        self.image = self.get_pygame_image(image_path)
        self.size = self.image.get_size()

    def draw(self, window) :
        if self.show :
            window.blit(self.image, self.position)

    def toggle_show(self) :
        self.show = not self.show

    def get_size(self) :
        return self.image.get_size()
    
    def set_position(self, new_position) :
        self.position = new_position
        
    def get_pygame_image(self, path) :
        try:
            return pygame.image.load(f"{CURRENT_PATH}/assets/images/{path}").convert_alpha()
        except FileNotFoundError:
            raise FileNotFoundError(f"L'image avec ce chemin '{path}' est introuvable dans le dossier '/assets/images/'.")

    def change_image(self, new_img_path) :
        self.image = self.get_pygame_image(new_img_path)
        self.image_path = new_img_path

    def on_release(self, mouse_position) :
        if (self.position[0] < mouse_position[0] < (self.position[0]+self.size[0])) and (self.position[1] < mouse_position[1] < (self.position[1]+self.size[1])) and self.show :
            if self.callback_action != None :
                self.callback_action(**self.kwargs, etat="release")
        else :
            self.callback_action(**self.kwargs, etat="release_outside")
        
    def on_click(self, mouse_position) :
        if (self.position[0] < mouse_position[0] < (self.position[0]+self.size[0])) and (self.position[1] < mouse_position[1] < (self.position[1]+self.size[1])) and self.show :
            if self.callback_action != None :
                self.callback_action(**self.kwargs, etat="click")

        
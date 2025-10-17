from Models.theme import Theme # pyright: ignore[reportMissingImports]

class Session :
    name : str
    player : str
    themes : list
    succed_themes : list
    current_theme : Theme = None
    def __init__(self,name : str , player_name : str, themes : list = [])
        self.name = name
        self.player = player_name
        self.themes = themes
        self.succed_themes = []

        
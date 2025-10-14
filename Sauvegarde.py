import json

def sauvegarder_partie(etat, fichier="sauvegarde.json"):
    with open(fichier, "w", encoding="utf-8") as f:
        json.dump(etat, f, indent=4) 

def charger_progression(fichier="progression.json"):
    try:
        with open(fichier, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Aucune sauvegarde trouvée. Nouvelle partie.")
        return None 
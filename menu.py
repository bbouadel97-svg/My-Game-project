
CHOIX = {
    "PLAY": 1,
    "SAVE": 2,
    "RESTART": 3,
    "Partie sauvegardée": 4
}


def afficher_choix(choix):
    for nom, valeur in choix.items():
        print(f"{nom} : {valeur}") 
def afficher_menu():
    print("Hello to your game!")
    print("Instructions : Choisissez une option du menu.")
    print("Menu :")
    afficher_choix(CHOIX)

def Sauvegarder_partie_en_cours():
    nom_fichier = input("Entrez le nom du fichier pour sauvegarder la partie en cours : ").strip()
    # Logique de sauvegarde de la partie en cours dans le fichier spécifié
    print(f"Partie sauvegardée dans le fichier : {nom_fichier}")

def Utilisateur():
    choix_utilisateur = input("Quel est ton choix ? ").strip().upper()
    nom_utilisateur = input("Quel est ton prénom ? ").strip()
    if choix_utilisateur in CHOIX:
        print(f"Tu as choisi l'option {choix_utilisateur}.")
    else:
        print("Option invalide. Veuillez choisir une option valide.")
        return
    return choix_utilisateur, nom_utilisateur
    
def Reponse():
    reponse = input("Es-tu prêt à commencer ? Oui ou Non ").strip().lower()
    if reponse == "oui":
        print("Super! Commençons le jeu.")
    elif reponse == "non":
        print("D'accord, à la prochaine!")
        exit()
    else:
        print("Réponse invalide. Veuillez répondre par 'Oui' ou 'Non'.")
        return Reponse()        
    return reponse
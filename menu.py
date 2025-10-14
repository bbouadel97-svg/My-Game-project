
CHOIX = {
    "PLAY": 1,
    "SAVE": 2,
    "RESTART": 3
}


def afficher_choix(choix):
    for nom, valeur in choix.items():
        print(f"{nom} : {valeur}") 
def afficher_menu():
    print("Hello to your game!")
    print("Instructions : Choisissez une option du menu.")
    print("Menu :")
    afficher_choix(CHOIX)

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
    reponse = input("Voulez-vous continuer ? (oui/non) ").strip().lower()
    if reponse != "oui":
        print("A vos marques !")
        return
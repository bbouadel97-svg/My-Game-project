
import sqlite3 
CHOIX = {
    "PLAY": 1,
    "SAVE": 2,
    "RESTART": 3
}

def afficher_choix(CHOIX):
    for nom, valeur in CHOIX.items():
        print(f"{nom} : {valeur}")

def main():
    print("Hello to your game!")
    print("Instructions : Choisissez une option du menu.")
    print("Menu :")
    afficher_choix(CHOIX)

    choix_utilisateur = input("Quel est ton choix ? ").strip().upper()
    nom_utilisateur = input("Quel est ton prénom ? ")

    if choix_utilisateur in CHOIX:
        print(f"Tu as choisi l'option {choix_utilisateur}.")
    else:
        print("Option invalide. Veuillez choisir une option valide.")
        return

    reponse = input("Voulez-vous continuer ? (oui/non) ").strip().lower()
    if reponse != "oui":
        print("Fin du jeu.")
        return

    print("Game start!")
    categorie = {
        "1": "Algorithme",
        "2": "Metiers de l'informatique",
        "3": "Logique",
        "4": "Culture Générale",
        "5": "Anglais",
    }
    print("Choix de catégories :")
    for numero, nom in categorie.items():
        print(f"{numero} : {nom}")
    categorie_choisie = input("Choisissez le numéro d'une catégorie : ").strip()
    if categorie_choisie in categorie:
        print(f"Vous avez choisi la catégorie : {categorie[categorie_choisie]}")
    else:
        print("Numéro de catégorie invalide.")
        return

    # Exemple de question
    print("Question : Python est-il un langage compilé ? (true/false)")
    reponse = input("Votre réponse : ").strip().lower()
    if reponse == "true":
        print("Bonne réponse ! Clavier d'or conquered")
    elif reponse == "false":
        print("Mauvaise réponse. 0 points. Game Over")
    else:
        print("Réponse non reconnue.")
    choix_utilisateur = input("Quel est ton choix ? ").strip().upper()
    if choix_utilisateur in CHOIX:
        print(f"Tu as choisi l'option {choix_utilisateur}.")
    else:
        print("Option invalide. Veuillez choisir une option valide.")
        return

    reponse = input("Voulez-vous continuer ? (oui/non) ").strip().lower()
    if reponse != "oui":
        print("Fin du jeu.")
        return

    print("Game start!")
    categorie = {
        "1": "Algorithme",
        "2": "Metiers de l'informatique",
        "3": "Logique",
        "4": "Culture Générale",
        "5": "Anglais",
    }

if __name__ == "__main__":
    main()
    

    
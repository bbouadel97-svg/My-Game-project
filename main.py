from menu import afficher_menu, Utilisateur, Reponse
from Catgory import Category
from Algo import lancer_quizalgo


def run():
    afficher_menu()
    Utilisateur()
    Reponse()
    score = 0
    continuer_jeu = True
    played = set()
    while continuer_jeu:
        categorie = Category(played=played)
        if categorie is None:
            # Plus de catégories disponibles
            break
        score = lancer_quizalgo(score, categorie)
        played.add(str(categorie))
        choix = input("Voulez vous continuer de jouer? Oui ou Non\n")
        continuer_jeu = choix.lower() == "oui"
    print("Merci d'avoir joué ! À bientôt.")


if __name__ == "__main__":
    run()

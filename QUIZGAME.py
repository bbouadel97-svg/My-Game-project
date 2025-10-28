from menu import afficher_menu, Utilisateur, Reponse
from Catgory import Category
from Algo import lancer_quizalgo
from Sauvegarde import (
    sauvegarder_score,
    sauvegarder_score_db,
    afficher_leaderboard,
    afficher_leaderboard_db,
    init_scores_db,
)



def demander_categorie() -> str:
    """Demande au joueur de choisir une catégorie et retourne la clé choisie."""
    return Category()


def jouer_categorie(score: int, categorie: str) -> int:
    """Lance le quiz pour la catégorie fournie et renvoie le score mis à jour."""
    return lancer_quizalgo(score, categorie)


def run():
    afficher_menu()

    # Récupère le nom du joueur depuis menu.Utilisateur()
    user_info = Utilisateur()
    if isinstance(user_info, tuple) and len(user_info) == 2:
        _, nom_utilisateur = user_info
    else:
        nom_utilisateur = "Anonyme"

    # Confirmation pour commencer
    Reponse()

    # Prépare la base de données pour les scores
    init_scores_db()

    # Optionnel: afficher les leaderboards avant de commencer
    voir_lb = input("Voulez-vous voir le leaderboard avant de jouer ? (oui/non) \n").strip().lower()
    if voir_lb == 'oui':
        print("Leaderboard (JSON):")
        afficher_leaderboard()
        print("\nLeaderboard (DB):")
        afficher_leaderboard_db()

    # Choix du backend pour la sauvegarde des scores
    backend = input("Où sauvegarder les scores ? (json/db) [db]\n").strip().lower() or 'db'

    score = 0
    continuer_jeu = True

    while continuer_jeu:
        categorie = demander_categorie()
        score = jouer_categorie(score, categorie)

        # Sauvegarder après chaque partie
        try:
            if backend == 'json':
                sauvegarder_score(nom_utilisateur, score, categorie)
            else:
                sauvegarder_score_db(nom_utilisateur, score, categorie)
        except Exception as e:
            print("Impossible de sauvegarder le score:", e)

        # Demander si on continue
        while True:
            choix = input("Voulez vous continuer de jouer? (oui/non) \n").strip().lower()
            if choix in ('oui', 'non'):
                break
            print("Réponse invalide — tape 'oui' ou 'non'.")
        continuer_jeu = (choix == "oui")
#fonction pour reprendre une partie sauvegardée

    # Afficher leaderboard final si demandé
    if input("Voulez-vous voir le leaderboard final ? (oui/non) \n").strip().lower() == 'oui':
        print("Leaderboard (DB):")
        afficher_leaderboard_db()
        print("\nLeaderboard (JSON):")
        afficher_leaderboard()
#montrer le score final et le nom du joueur
    print(f"Votre score final est de {score}, {nom_utilisateur}.")


if __name__ == "__main__":
    run()

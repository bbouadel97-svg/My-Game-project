# -*- coding: utf-8 -*-
import csv
from pathlib import Path
import os
from menu import afficher_menu, Utilisateur, Reponse
from questions_service import get_boss_question_for_category
from Player_session import PlayerSession
from Progression import sauvegarder_progression,charger_progression,sauvegarder_partie,sauvegarder_score,sauvegarder_score_db

def charger_questions_csv(fichier_csv):
    categories = {
        "1": "Anglais",
        "2": "Logique",
        "3": "Algorithme", 
        "4": "Culture Générale",
        "5": "Métiers de l''informatique"
    }
    
    questions_par_categorie = {cat_id: [] for cat_id in categories}
    
    try:
        with open(fichier_csv, "r", encoding="utf-8") as f:
            lecteur = csv.reader(f)
            for ligne in lecteur:
                if len(ligne) >= 3:
                    cat_id, question, reponse = ligne[0], ligne[1], ligne[2]
                    if cat_id in questions_par_categorie:
                        questions_par_categorie[cat_id].append((question, reponse))
        return questions_par_categorie, categories
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier CSV: {e}")
        return {}, {}

def lancer_boss(session: PlayerSession, session_id: int, categorie: str, score: int = 0) -> tuple[bool, int]:
    boss_q = get_boss_question_for_category(categorie)
    if not boss_q:
        print("Pas de question BOSS disponible pour cette catégorie.")
        return False, score
        
    question, reponse_correcte = boss_q
    print("\n=== QUESTION BOSS ===")
    print("Cette question vaut 50 points ! Une mauvaise réponse en fait perdre 20.")
    print("\nQuestion:", question)   
    reponse = input("Votre réponse : ").strip()
    correct = reponse.lower() == reponse_correcte.lower() 

    if correct:
        print("\nBRAVO ! Vous avez vaincu le BOSS ! +50 points")
        score += 50
    else:
        print(f"\nDommage ! La réponse était : {reponse_correcte}")
        print("Le BOSS vous a vaincu. -20 points")
        score -= 20   
    # Enregistre la réponse dans la base de données (catégorie fournie)
    try:
        session.add_question_to_session_with_category(session_id, None, correct, int(categorie))
    except AttributeError:
        # fallback si l'ancienne méthode existe
        session.add_question_to_session(session_id, int(categorie), correct)   
    return correct, score
def lancer_quiz(session: PlayerSession, session_id: int, questions, categorie: str, score=0, max_questions=None):
    """Lance un quiz pour une catégorie.

    Par défaut on utilise 20 questions par catégorie si disponibles. Si la
    catégorie contient moins de questions, on utilise sa taille.
    """
    if not questions:
        print("Pas de questions disponibles pour cette catégorie.")
        return score

    # Défaut : 20 questions ou la taille de la liste si elle est plus petite
    if max_questions is None:
        max_questions = min(20, len(questions))

    for i, (question, reponse_correcte) in enumerate(questions):
        if i >= max_questions:
            break
            
        print("\nQuestion:", question)
        try:
            reponse = input("Votre réponse : ").strip()
            correct = reponse.lower() == reponse_correcte.lower()
            
            if correct:
                print("Correct ! +10 points")
                score += 10
            else:
                print(f"Incorrect. La réponse était : {reponse_correcte}")
                score -= 5
                
            # Enregistre la réponse dans la base de données (avec catégorie)
            try:
                session.add_question_to_session_with_category(session_id, i + 1, correct, int(categorie))
            except AttributeError:
                session.add_question_to_session(session_id, i + 1, correct)
        except EOFError:
            print("Réponse non fournie, question passée.")
            score -= 5
        
        print(f"Score actuel : {score}")

    return score

charger_progression()

def afficher_statistiques(session: PlayerSession, nom_utilisateur: str):
    """Affiche les statistiques du joueur."""
    historique = session.get_player_history(nom_utilisateur)
    if not historique:
        print("Aucune partie jouée.")
        return
        
    print("\n=== Statistiques du joueur ===")
    print(f"Joueur : {nom_utilisateur}")
    print(f"Meilleur score : {max(s['score'] for s in historique)}")
    print(f"Nombre de parties : {len(historique)}")

    derniere_session = historique[0]
    print("\nDernière partie :")
    print(f"Date : {derniere_session['date']}")
    print(f"Score : {derniere_session['score']}")
    print(f"Questions répondues : {derniere_session['questions_answered']}")
    print(f"Bonnes réponses : {derniere_session['correct_answers']}")
    print(f"Précision : {derniere_session['accuracy']:.1f}%")

def run():
    script_dir = Path(os.path.dirname(os.path.realpath(__file__)))
    csv_path = script_dir / "QUESTIONS.CSV"
    
    # Initialise la gestion des sessions
    session_manager = PlayerSession()
    
    questions_par_cat, categories = charger_questions_csv(csv_path)
    if not questions_par_cat:
        print("Erreur: Impossible de charger les questions.")
        return
    
    afficher_menu()
    user_info = Utilisateur()
    if isinstance(user_info, tuple) and len(user_info) == 2:
        _, nom_utilisateur = user_info
    else:
        nom_utilisateur = "Anonyme"
    
    # Crée ou récupère le joueur
    result = session_manager.create_player(nom_utilisateur)
    print(result)
    
    if Reponse().lower() != "oui":
        print("À bientôt!")
        return
    
    # Crée une nouvelle session de jeu
    session_id = session_manager.create_game_session(nom_utilisateur)
    score = 0
    played = set()
    
    while True:
        print("\nCatégories disponibles:")
        for cat_id, nom in categories.items():
            if cat_id not in played:
                print(f"{cat_id} : {nom}")
        
        if not [cat for cat in categories if cat not in played]:
            print("\nFélicitations ! Vous avez terminé toutes les catégories.")
            break
        
        choix = input("\nChoisissez une catégorie (ou q pour quitter) : ").strip()
        if choix.lower() == "q":
            break
            
        if choix not in categories or choix in played:
            print("Choix invalide ou catégorie déjà jouée.")
            continue
            
        print(f"\nCatégorie : {categories[choix]}")
        # Enregistre que la catégorie a été jouée pour cette session
        try:
            session_manager.add_category_to_session(session_id, int(choix))
        except AttributeError:
            pass

        score = lancer_quiz(session_manager, session_id, questions_par_cat[choix], choix, score)
        played.add(choix)
        
        print(f"\nScore après quiz : {score}")
        
        print("\nVous avez terminé les questions de cette catégorie!")
        if input("Voulez-vous affronter le BOSS de cette catégorie ? (oui/non) : ").strip().lower() == "oui":
            victoire, score = lancer_boss(session_manager, session_id, choix, score)
            if victoire:
                print("\nFélicitations ! Vous avez conquis cette catégorie !")
            else:
                print("\nVous pouvez réessayer le BOSS plus tard !")
        
        print(f"\nScore total : {score}")
        
        # Met à jour le score de la session et le meilleur score du joueur
        try:
            session_manager.update_game_session_score(session_id, score)
        except AttributeError:
            pass
        session_manager.update_player_score(nom_utilisateur, score)
        
        continuer = input("\nVoulez-vous continuer vers une autre catégorie ? (oui/non) : ").strip().lower()
        if continuer != "oui":
            break
    # Affiche les statistiques de fin de partie
    print(f"\nPartie terminée ! Score final : {score}")
    afficher_statistiques(session_manager, nom_utilisateur)
    print(f"Au revoir {nom_utilisateur}, à bientôt !")

if __name__ == "__main__":
    run()

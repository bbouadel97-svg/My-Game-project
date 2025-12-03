# -*- coding: utf-8 -*-
import csv
from pathlib import Path
import os
from menu import afficher_menu, Utilisateur, Reponse
from questions_service import get_boss_question_for_category
from Player_session import PlayerSession
from Progression import (
    sauvegarder_progression,
    charger_progression,
    reset_progression,
)

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
        print("\nBRAVO ! Vous avez vaincu le BOSS ! +30 points")
        score += 30
    else:
        print(f"\nDommage ! La réponse était : {reponse_correcte}")
        print("Le BOSS vous a vaincu. 0 points gagnés.")
        score += 0
    try:
        session.add_question_to_session_with_category(session_id, None, correct, int(categorie))
    except AttributeError:
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
                score += 0
            try:
                session.add_question_to_session_with_category(session_id, i + 1, correct, int(categorie))
            except AttributeError:
                session.add_question_to_session(session_id, i + 1, correct)
        except EOFError:
            print("Réponse non fournie, question passée.")
            score += 0
        
        print(f"Score actuel : {score}")

    return score
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
    session_manager = PlayerSession()   
    questions_par_cat, categories = charger_questions_csv(csv_path)
    if not questions_par_cat:
        print("Erreur: Impossible de charger les questions.")
        return    
    afficher_menu()
    user_info = Utilisateur()
    if isinstance(user_info, tuple) and len(user_info) == 2:
        choix_menu, nom_utilisateur = user_info
    else:
        choix_menu, nom_utilisateur = 1, "Anonyme"
    if choix_menu == 3:
        print("\nVous avez choisi RESTART de la partie sauvegardée.")
        confirm = input("Confirmer la réinitialisation complète ? (oui/non) : ").strip().lower()
        if confirm == "oui":
            try:
                reset_progression("progression.json")
            except Exception:
                pass
            try:
                session_manager = PlayerSession()
                if session_manager.reset_player_sessions(nom_utilisateur):
                    print("Sessions du joueur réinitialisées dans la base.")
            except Exception as e:
                print("Impossible de réinitialiser les sessions DB:", e)
            print("Réinitialisation terminée. Nouvelle partie !\n")
        else:
            print("Réinitialisation annulée. Poursuite de la partie normale.\n")
    result = session_manager.create_player(nom_utilisateur)
    print(result)
    played = set()
    score = 0
    if choix_menu == 4:
        etat = charger_progression("progression.json")
        if etat:
            nom_utilisateur = etat.get("nom", nom_utilisateur)
            score = int(etat.get("score", 0))
            played = set(str(c) for c in etat.get("categories_jouees", []))
            print(f"Progression chargée: joueur={nom_utilisateur}, score={score}, cat jouées={sorted(played)}")
        else:
            print("Aucune progression à reprendre. Nouvelle partie.")
    if Reponse().lower() != "oui":
        print("À bientôt!")
        return
    session_id = session_manager.create_game_session(nom_utilisateur)  
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
        try:
            sauvegarder_progression(nom_utilisateur, score, list(played))
        except Exception as e:
            print("Impossible de sauvegarder la progression:", e)
        try:
            session_manager.update_game_session_score(session_id, score)
        except AttributeError:
            pass
        session_manager.update_player_score(nom_utilisateur, score)
        
        continuer = input("\nVoulez-vous continuer vers une autre catégorie ? (oui/non) : ").strip().lower()
        if continuer != "oui":
            break
    try:
        sauvegarder_progression(nom_utilisateur, score, list(played))
    except Exception:
        pass
    print(f"\nPartie terminée ! Score final : {score}")
    afficher_statistiques(session_manager, nom_utilisateur)
    print(f"Au revoir {nom_utilisateur}, à bientôt !")

if __name__ == "__main__":
    run()

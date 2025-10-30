from menu import afficher_menu, Utilisateur, Reponse
from Catgory import Category
from Algo import lancer_quizalgo
from Sauvegarde import sauvegarder_progression, charger_progression
from boss import Boss
from questions_service import load_questions_from_sql
from pathlib import Path


# Mapping category keys to SQL table names (matching Script-1.sql)
CAT_TABLE = {
    "1": "quiz_algo",
    "2": "quiz_metiers",
    "3": "quiz_logique",
    "4": "quiz_culture",
    "5": "quiz_anglais",
}


def build_boss_for_category(cat_key: str, sql_path: Path | str = "Project 0/Script-1.sql") -> Boss:
    tables = load_questions_from_sql(Path(sql_path))
    table_name = CAT_TABLE.get(str(cat_key))
    qlist = tables.get(table_name, []) if table_name else []
    # Boss: 7 questions, need 5 correct to win
    return Boss(cat_key, table_name or f"Cat {cat_key}", qlist, n_questions=7, win_required=5)


def run():
    afficher_menu()

    # Ask to resume a saved campaign
    if input("Voulez-vous reprendre une campagne sauvegardée ? (oui/non) \n").strip().lower() == 'oui':
        etat = charger_progression()
    else:
        etat = None

    if etat:
        nom_utilisateur = etat["nom"]
        score = int(etat.get("score", 0))
        played = set(etat.get("categories_jouees", []))
        bosses_defeated = dict(etat.get("bosses_defeated", {}))
        final_unlocked = bool(etat.get("final_unlocked", False))
        print(f"Bienvenue de retour, {nom_utilisateur}. Score: {score}")
    else:
        user_info = Utilisateur()
        if isinstance(user_info, tuple) and len(user_info) == 2:
            _, nom_utilisateur = user_info
        else:
            nom_utilisateur = "Anonyme"
        Reponse()
        score = 0
        played = set()
        bosses_defeated = {k: False for k in CAT_TABLE.keys()}
        final_unlocked = False

    # Preload questions DB once
    sql_path = Path('Project 0/Script-1.sql')

    while True:
        # If final unlocked, offer final boss
        if final_unlocked:
            print("Le Clavier d'Or est disponible !")
            choix_final = input("Voulez-vous affronter le Clavier d'Or maintenant ? (oui/non) \n").strip().lower()
            if choix_final == 'oui':
                # build a mixed boss from all tables
                tables = load_questions_from_sql(sql_path)
                all_q = []
                for t in tables.values():
                    all_q.extend(t)
                final_boss = Boss('final', 'Clavier d\'Or', all_q, n_questions=10, win_required=7, scoring=(15, -10))
                won, score = final_boss.fight(starting_score=score)
                if won:
                    print("Félicitations ! Vous avez conquis le Clavier d'Or !")
                else:
                    print("Vous avez échoué contre le Clavier d'Or. Recommencez quand vous serez prêt.")
                # Save and exit
                sauvegarder_progression(nom_utilisateur, score, played, bosses_defeated, final_unlocked)
                break

        categorie = Category(played=played)
        if categorie is None:
            print("Plus de catégories disponibles.")
            # If all bosses defeated, unlock final
            if all(bosses_defeated.get(k, False) for k in CAT_TABLE.keys()):
                final_unlocked = True
                print("Tous les bosses vaincus — le Clavier d'Or est débloqué !")
                sauvegarder_progression(nom_utilisateur, score, played, bosses_defeated, final_unlocked)
                continue
            else:
                sauvegarder_progression(nom_utilisateur, score, played, bosses_defeated, final_unlocked)
                break

        # Play regular trial (lancer_quizalgo is expected to use category key)
        score = lancer_quizalgo(score, categorie)
        played.add(str(categorie))

        # After finishing trials in that category, face the boss (if not yet defeated)
        if not bosses_defeated.get(str(categorie), False):
            boss = build_boss_for_category(categorie, sql_path)
            won, score = boss.fight(starting_score=score)
            if won:
                bosses_defeated[str(categorie)] = True
                print(f"Boss {categorie} vaincu !")
            else:
                print(f"Boss {categorie} non vaincu. Tu peux retenter plus tard.")

        # If all bosses defeated, unlock final
        if all(bosses_defeated.get(k, False) for k in CAT_TABLE.keys()):
            final_unlocked = True
            print("Tous les bosses vaincus — le Clavier d'Or est débloqué !")

        # Save progression after each category/boss
        sauvegarder_progression(nom_utilisateur, score, played, bosses_defeated, final_unlocked)

        # Continue?
        choix = input("Voulez-vous continuer la campagne ? (oui/non) \n").strip().lower()
        if choix != 'oui':
            print("Progression sauvegardée. À bientôt !")
            break


if __name__ == "__main__":
    run()

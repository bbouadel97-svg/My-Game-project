<<<<<<< HEAD

=======
>>>>>>> 202519cb70301fd2b1da6150c2a7841ab7124c92
def Category(played=None):
    """Affiche les catégories disponibles et demande un choix.

    played: iterable of keys (e.g. ['1','3']) representing already-played categories.
    Retourne la clé choisie (string) ou None si plus de catégories disponibles.
    """
    if played is None:
        played = set()
    else:
        played = set(str(p) for p in played)

    categorie = {
        "1": "Algorithme",
        "2": "Metiers de l'informatique",
        "3": "Logique",
        "4": "Culture Générale",
        "5": "Anglais",
    }

    # Filtrer les catégories déjà jouées
    remaining = {k: v for k, v in categorie.items() if k not in played}

    if not remaining:
        print("Aucune catégorie restante. Merci d'avoir joué !")
        return None

<<<<<<< HEAD
    print("""
          
     ┏━╸╻ ╻┏━┓╻╻ ╻   ╺┳┓┏━╸┏━┓   ┏━╸┏━┓╺┳╸┏━╸┏━╸┏━┓┏━┓╻┏━╸┏━┓    
     ┃  ┣━┫┃ ┃┃┏╋┛    ┃┃┣╸ ┗━┓   ┃  ┣━┫ ┃ ┣╸ ┃╺┓┃ ┃┣┳┛┃┣╸ ┗━┓   ╹
     ┗━╸╹ ╹┗━┛╹╹ ╹   ╺┻┛┗━╸┗━┛   ┗━╸╹ ╹ ╹ ┗━╸┗━┛┗━┛╹┗╸╹┗━╸┗━┛   ╹                                                           
                                                                                                                                                               
                                                            """)
=======
    print("Choix de catégories :")
>>>>>>> 202519cb70301fd2b1da6150c2a7841ab7124c92
    for numero, nom in remaining.items():
        print(f"{numero} : {nom}")

    while True:
        choix = input("Choisis une catégorie : ").strip()
        if choix in remaining:
            print(f"Tu as choisi la catégorie : {choix} - {remaining[choix]}")
            return choix
        else:
            print("Catégorie invalide ou déjà jouée. Réessaie.")
<<<<<<< HEAD
Category()
=======
>>>>>>> 202519cb70301fd2b1da6150c2a7841ab7124c92

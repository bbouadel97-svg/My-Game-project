def boss_themes(played):
    try :   
        with open("boss_themes.txt", "r", encoding="utf-8") as f:
            boss_list = f.read().splitlines()
    except FileNotFoundError:
        boss_list = []
    for boss in boss_list:
        if boss not in played:
            print(f"Vous avez débloqué le boss du thème {boss} ! Préparez-vous pour un défi supplémentaire.")
            score = lancer_quizalgo(score, boss)
            played.add(boss)
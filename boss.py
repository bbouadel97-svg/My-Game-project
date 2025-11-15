import random
from typing import List, Tuple


class Boss:
    """Simple Boss class for a quiz boss fight.

    questions: list of (question, answer)
    n_questions: how many questions to ask
    win_required: min number of correct answers required to win
    scoring: tuple (points_correct, points_wrong)
    """
    def __init__(self, key: str, name: str, questions: List[Tuple[str, str]], n_questions: int = 7, win_required: int = 5, scoring=(10, -5)):
        self.key = str(key)
        self.name = name
        self.questions = list(questions)
        random.shuffle(self.questions)
        self.n_questions = min(n_questions, len(self.questions))
        self.win_required = win_required
        self.scoring = scoring

    def fight(self, starting_score: int = 0) -> tuple[bool, int, list]:
        """Run the boss fight.

        Returns (won: bool, new_score: int, last_questions: list of (q,a) asked).
        After a loss, the player is offered an immediate rematch (yes/no).
        """
        last_asked = None
        score = starting_score

        while True:
            correct = 0
            asked = []
            print(f"--- Combat contre le boss : {self.name} ---")
            for i in range(self.n_questions):
                # protect index just in case
                if i >= len(self.questions):
                    break
                q, a = self.questions[i]
                asked.append((q, a))
                print(f"Question {i+1}/{self.n_questions} :")
                user = input(q + "\nRéponse: ").strip().lower()
                if user == a.strip().lower():
                    correct += 1
                    score += self.scoring[0]
                    print(f"Correct (+{self.scoring[0]})")
                else:
                    score += self.scoring[1]
                    print(f"Faux (attendu: {a}) ({self.scoring[1]})")
                print(f"Score actuel : {score}\n")

            won = correct >= self.win_required
            last_asked = asked
            if won:
                print(f"Bravo ! Boss {self.name} vaincu ({correct}/{self.n_questions}).")
                return True, score, last_asked

            # lost
            print(f"Échec contre {self.name} ({correct}/{self.n_questions}).")
            rematch = input("Voulez-vous retenter le boss maintenant ? (oui/non) \n").strip().lower()
            if rematch == 'oui':
                # reshuffle questions for rematch
                random.shuffle(self.questions)
                continue
            return False, score, last_asked

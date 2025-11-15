# -*- coding: utf-8 -*-
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List

class PlayerSession:
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.db_path = self.script_dir / "game.db"
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS player
                          (id_player INTEGER PRIMARY KEY AUTOINCREMENT,
                           player_name TEXT UNIQUE,
                           player_score INTEGER DEFAULT 0)""")

            conn.execute("""CREATE TABLE IF NOT EXISTS game_session
                          (id_session INTEGER PRIMARY KEY AUTOINCREMENT,
                           id_player INTEGER,
                           score INTEGER DEFAULT 0,
                           date_played TEXT,
                           FOREIGN KEY(id_player) REFERENCES player(id_player))""")

            # Enregistre les questions répondues (avec catégorie optionnelle)
            conn.execute("""CREATE TABLE IF NOT EXISTS session_questions
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           id_session INTEGER,
                           id_question INTEGER,
                           category_id INTEGER,
                           answered_correctly INTEGER,
                           FOREIGN KEY(id_session) REFERENCES game_session(id_session))""")

            # Enregistre les catégories jouées dans une session
            conn.execute("""CREATE TABLE IF NOT EXISTS session_categories
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           id_session INTEGER,
                           category_id INTEGER,
                           FOREIGN KEY(id_session) REFERENCES game_session(id_session))""")
            # Migration: ajouter la colonne category_id si la table existait déjà
            cur = conn.cursor()
            cur.execute("PRAGMA table_info(session_questions)")
            cols = [r[1] for r in cur.fetchall()]
            if 'category_id' not in cols:
                try:
                    conn.execute('ALTER TABLE session_questions ADD COLUMN category_id INTEGER')
                except sqlite3.OperationalError:
                    # si la colonne existe déjà ou si l'alter échoue, ignorer
                    pass

    def create_player(self, nom: str) -> str:
        with sqlite3.connect(self.db_path) as conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT player_name FROM player WHERE player_name = ?", (nom,))
                if cursor.fetchone():
                    return f"Bon retour {nom} !"
                
                cursor.execute("INSERT INTO player (player_name, player_score) VALUES (?, 0)", (nom,))
                conn.commit()
                return f"Nouveau joueur {nom} créé !"
            except sqlite3.Error as e:
                return f"Erreur lors de la création du joueur : {e}"

    def update_player_score(self, nom: str, nouveau_score: int) -> None:
        # Met à jour le meilleur score du joueur si le nouveau score est supérieur
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT player_score FROM player WHERE player_name = ?", (nom,))
            row = cur.fetchone()
            if row is None:
                return
            best = row[0] or 0
            if nouveau_score > best:
                cur.execute("UPDATE player SET player_score = ? WHERE player_name = ?", (nouveau_score, nom))
                conn.commit()

    def create_game_session(self, nom: str) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_player FROM player WHERE player_name = ?", (nom,))
            player_id = cursor.fetchone()
            if not player_id:
                return 0
            
            cursor.execute("""
                INSERT INTO game_session (id_player, score, date_played)
                VALUES (?, 0, ?)
            """, (player_id[0], datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            conn.commit()
            return cursor.lastrowid

    def add_question_to_session(self, session_id: int, question_id: int, correct: bool) -> None:
        # Backwards-compatible: question_id can be None; category can be provided
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO session_questions (id_session, id_question, category_id, answered_correctly)
                VALUES (?, ?, NULL, ?)
            """, (session_id, question_id, 1 if correct else 0))
            conn.commit()

    def add_question_to_session_with_category(self, session_id: int, question_id: int, correct: bool, category_id: int = None) -> None:
        """Enregistre une question répondue et la catégorie associée (optionnel)."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO session_questions (id_session, id_question, category_id, answered_correctly)
                VALUES (?, ?, ?, ?)
            """, (session_id, question_id, category_id, 1 if correct else 0))
            conn.commit()

    def add_category_to_session(self, session_id: int, category_id: int) -> None:
        """Enregistre qu'une catégorie a été jouée dans la session."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO session_categories (id_session, category_id)
                VALUES (?, ?)
            """, (session_id, category_id))
            conn.commit()

    def update_game_session_score(self, session_id: int, score: int) -> None:
        """Met à jour le score final d'une session de jeu."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("UPDATE game_session SET score = ? WHERE id_session = ?", (score, session_id))
            conn.commit()

    def get_player_history(self, nom: str) -> List[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT gs.id_session, gs.score, gs.date_played,
                       COUNT(sq.id_question) as questions_answered,
                       SUM(sq.answered_correctly) as correct_answers
                FROM game_session gs
                JOIN player p ON gs.id_player = p.id_player
                LEFT JOIN session_questions sq ON gs.id_session = sq.id_session
                WHERE p.player_name = ?
                GROUP BY gs.id_session
                ORDER BY gs.date_played DESC
            """, (nom,))
            
            sessions = []
            for row in cursor.fetchall():
                session_id, score, date_played, total_q, correct_q = row
                correct_q = correct_q or 0
                total_q = total_q or 0
                sessions.append({
                    "session_id": session_id,
                    "score": score,
                    "date": date_played,
                    "questions_answered": total_q,
                    "correct_answers": correct_q,
                    "accuracy": (correct_q / total_q * 100) if total_q > 0 else 0
                })
            return sessions

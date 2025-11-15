# -*- coding: utf-8 -*-
import csv
import sqlite3
import os
from pathlib import Path

def init_database():
    script_dir = Path(os.path.dirname(os.path.realpath(__file__)))
    db_path = script_dir / "game.db"
    
    if db_path.exists():
        os.remove(db_path)
    
    con = sqlite3.connect(db_path)
    
    try:
        with open(script_dir / "Player.sql", "r", encoding="utf-8") as schema:
            sql_script = schema.read()
            con.executescript(sql_script)
            print("Schéma de base de données créé avec succès.")
        
        with open(script_dir / "QUESTIONS.CSV", "r", encoding="utf-8") as file:
            data = csv.reader(file)
            next(data)
            
            for row in data:
                try:
                    category_id = row[0]
                    question = row[1].replace("''", "''''")
                    answer = row[2].replace("''", "''''")
                    
                    query = f"INSERT INTO questions (question, reponse, id_category, is_boss) VALUES (?, ?, ?, 0)"
                    con.execute(query, (question, answer, category_id))
                except Exception as e:
                    print(f"Erreur lors de l''insertion de la question: {e}")
                    continue
        
        try:
            with open(script_dir / "boss_questions.csv", "r", encoding="utf-8") as file:
                data = csv.reader(file)
                next(data)
                
                for row in data:
                    try:
                        category_id = row[0]
                        question = row[1].replace("''", "''''")
                        answer = row[2].replace("''", "''''")
                        
                        query = f"INSERT INTO questions (question, reponse, id_category, is_boss) VALUES (?, ?, ?, 1)"
                        con.execute(query, (question, answer, category_id))
                    except Exception as e:
                        print(f"Erreur lors de l''insertion de la question boss: {e}")
                        continue
        except FileNotFoundError:
            print("Fichier boss_questions.csv non trouvé.")
        
        con.commit()
        print("Base de données initialisée avec succès!")
        
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM questions WHERE is_boss = 0")
        count_normal = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM questions WHERE is_boss = 1")
        count_boss = cur.fetchone()[0]
        
        print(f"Questions normales importées: {count_normal}")
        print(f"Questions boss importées: {count_boss}")
        
    except Exception as e:
        print(f"Erreur lors de l''initialisation de la base de données: {e}")
        con.rollback()
    finally:
        con.close()

if __name__ == "__main__":
    init_database()

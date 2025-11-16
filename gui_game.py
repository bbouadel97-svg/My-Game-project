# -*- coding: utf-8 -*-
import pygame
import sys
from pathlib import Path
from typing import Optional, List, Tuple
from Player_session import PlayerSession
from questions_service import get_boss_question_for_category
from Progression import sauvegarder_progression, charger_progression, reset_progression
import csv

# Initialisation Pygame
pygame.init()

# Constantes
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
BLUE = (70, 130, 180)
LIGHT_BLUE = (135, 206, 250)
GREEN = (34, 139, 34)
RED = (220, 20, 60)
YELLOW = (255, 215, 0)
PURPLE = (138, 43, 226)

# Polices
FONT_LARGE = None
FONT_MEDIUM = None
FONT_SMALL = None


def init_fonts():
    """Initialise les polices du jeu."""
    global FONT_LARGE, FONT_MEDIUM, FONT_SMALL
    FONT_LARGE = pygame.font.Font(None, 64)
    FONT_MEDIUM = pygame.font.Font(None, 36)
    FONT_SMALL = pygame.font.Font(None, 24)


class Button:
    """Bouton cliquable avec effet de survol."""
    
    def __init__(self, x, y, width, height, text, color, hover_color, text_color=WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        
    def draw(self, screen):
        """Dessine le bouton."""
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, self.rect, 3, border_radius=10)
        
        text_surf = FONT_MEDIUM.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
        
    def handle_event(self, event):
        """Gère les événements du bouton."""
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False


class QuizGame:
    """Classe principale du jeu avec interface graphique."""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Quiz Game - Le Clavier d'Or")
        self.clock = pygame.time.Clock()
        self.running = True
        
        init_fonts()
        
        # Données du jeu
        self.session_manager = PlayerSession()
        self.player_name = ""
        self.score = 0
        self.played_categories = set()
        self.current_category = None
        self.questions = []
        self.current_question_index = 0
        self.session_id = None
        self.user_input = ""
        self.input_active = False
        self.message = ""
        self.message_color = WHITE
        self.boss_answered = False
        self.show_feedback = False
        self.feedback_timer = 0
        self.feedback_duration = 90  # frames (1.5 secondes à 60 FPS)
        
        # États du jeu
        self.state = "MENU"  # MENU, NAME_INPUT, CATEGORY_SELECT, QUIZ, BOSS, STATS, RESTART
        
        # Charger les catégories
        self.categories = {
            "1": "Anglais",
            "2": "Logique",
            "3": "Algorithme",
            "4": "Culture Générale",
            "5": "Métiers de l'informatique"
        }
        
        self.load_questions()
        
    def load_questions(self):
        """Charge les questions depuis le fichier CSV."""
        csv_path = Path("QUESTIONS.CSV")
        self.questions_by_category = {cat_id: [] for cat_id in self.categories}
        
        try:
            with open(csv_path, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) >= 3:
                        cat_id, question, answer = row[0], row[1], row[2]
                        if cat_id in self.questions_by_category:
                            self.questions_by_category[cat_id].append((question, answer))
        except Exception as e:
            print(f"Erreur chargement questions: {e}")
    
    def draw_text(self, text, font, color, x, y, center=False):
        """Dessine du texte à l'écran."""
        text_surf = font.render(text, True, color)
        if center:
            text_rect = text_surf.get_rect(center=(x, y))
        else:
            text_rect = text_surf.get_rect(topleft=(x, y))
        self.screen.blit(text_surf, text_rect)
        return text_rect
    
    def draw_menu(self):
        """Dessine l'écran du menu principal."""
        self.screen.fill(BLUE)
        
        # Titre
        self.draw_text("LE CLAVIER D'OR", FONT_LARGE, YELLOW, SCREEN_WIDTH // 2, 100, center=True)
        self.draw_text("Quiz Game", FONT_MEDIUM, WHITE, SCREEN_WIDTH // 2, 160, center=True)
        
        # Créer les boutons seulement si nécessaire
        if not hasattr(self, 'menu_buttons'):
            self.menu_buttons = [
                Button(SCREEN_WIDTH // 2 - 150, 250, 300, 60, "JOUER", GREEN, LIGHT_BLUE),
                Button(SCREEN_WIDTH // 2 - 150, 330, 300, 60, "REPRENDRE", PURPLE, LIGHT_BLUE),
                Button(SCREEN_WIDTH // 2 - 150, 410, 300, 60, "RESTART", RED, LIGHT_BLUE),
                Button(SCREEN_WIDTH // 2 - 150, 490, 300, 60, "STATISTIQUES", BLUE, LIGHT_BLUE),
                Button(SCREEN_WIDTH // 2 - 150, 570, 300, 60, "QUITTER", DARK_GRAY, GRAY)
            ]
        buttons = self.menu_buttons
        
        for btn in buttons:
            btn.draw(self.screen)
            
        return buttons
    
    def draw_name_input(self):
        """Dessine l'écran de saisie du nom."""
        self.screen.fill(BLUE)
        
        self.draw_text("Entrez votre prénom:", FONT_MEDIUM, WHITE, SCREEN_WIDTH // 2, 250, center=True)
        
        # Zone de saisie
        input_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, 320, 400, 50)
        color = LIGHT_BLUE if self.input_active else GRAY
        pygame.draw.rect(self.screen, color, input_rect, border_radius=5)
        pygame.draw.rect(self.screen, WHITE, input_rect, 2, border_radius=5)
        
        # Texte saisi
        self.draw_text(self.user_input, FONT_MEDIUM, BLACK, input_rect.x + 10, input_rect.y + 10)
        
        # Bouton valider (cache)
        if not hasattr(self, 'name_input_button'):
            self.name_input_button = Button(SCREEN_WIDTH // 2 - 100, 420, 200, 50, "VALIDER", GREEN, LIGHT_BLUE)
        self.name_input_button.draw(self.screen)
        
        if self.message:
            self.draw_text(self.message, FONT_SMALL, self.message_color, SCREEN_WIDTH // 2, 500, center=True)
        
        return [input_rect, self.name_input_button]
    
    def draw_category_select(self):
        """Dessine l'écran de sélection de catégorie."""
        self.screen.fill(BLUE)
        
        self.draw_text(f"Joueur: {self.player_name} | Score: {self.score}", 
                      FONT_SMALL, WHITE, 20, 20)
        
        self.draw_text("Choisissez une catégorie:", FONT_LARGE, WHITE, 
                      SCREEN_WIDTH // 2, 80, center=True)
        
        # Afficher seulement les catégories non jouées
        available = [(k, v) for k, v in self.categories.items() if k not in self.played_categories]
        
        if not available:
            self.draw_text("Félicitations! Toutes les catégories terminées!", 
                          FONT_MEDIUM, YELLOW, SCREEN_WIDTH // 2, 300, center=True)
            if not hasattr(self, 'all_done_button'):
                self.all_done_button = Button(SCREEN_WIDTH // 2 - 150, 400, 300, 60, "VOIR STATS", GREEN, LIGHT_BLUE)
            self.all_done_button.draw(self.screen)
            return [self.all_done_button]
        
        # Cache des boutons de catégories
        cache_key = tuple(self.played_categories)
        if not hasattr(self, 'category_buttons_cache') or self.category_buttons_cache_key != cache_key:
            self.category_buttons_cache = []
            y_start = 180
            for i, (cat_id, cat_name) in enumerate(available):
                btn = Button(SCREEN_WIDTH // 2 - 250, y_start + i * 80, 500, 60, 
                            f"{cat_id}. {cat_name}", PURPLE, LIGHT_BLUE)
                btn.cat_id = cat_id
                self.category_buttons_cache.append(btn)
            # Bouton quitter
            btn_quit = Button(50, SCREEN_HEIGHT - 80, 150, 50, "QUITTER", RED, GRAY)
            self.category_buttons_cache.append(btn_quit)
            self.category_buttons_cache_key = cache_key
        
        buttons = self.category_buttons_cache
        for btn in buttons:
            btn.draw(self.screen)
        
        return buttons
    
    def draw_quiz(self):
        """Dessine l'écran de quiz."""
        self.screen.fill(BLUE)
        
        # Infos en haut
        self.draw_text(f"Joueur: {self.player_name} | Score: {self.score}", 
                      FONT_SMALL, WHITE, 20, 20)
        self.draw_text(f"Catégorie: {self.categories[self.current_category]}", 
                      FONT_SMALL, WHITE, 20, 50)
        
        if self.current_question_index >= len(self.questions):
            # Quiz terminé
            self.draw_text("Quiz terminé!", FONT_LARGE, YELLOW, SCREEN_WIDTH // 2, 200, center=True)
            self.draw_text(f"Score: {self.score}", FONT_MEDIUM, WHITE, SCREEN_WIDTH // 2, 280, center=True)
            
            if not hasattr(self, 'quiz_end_buttons'):
                self.quiz_end_buttons = [
                    Button(SCREEN_WIDTH // 2 - 150, 360, 300, 60, "AFFRONTER LE BOSS", RED, LIGHT_BLUE),
                    Button(SCREEN_WIDTH // 2 - 150, 440, 300, 60, "PASSER", GRAY, DARK_GRAY)
                ]
            for btn in self.quiz_end_buttons:
                btn.draw(self.screen)
            
            return self.quiz_end_buttons
        
        # Question actuelle
        question, answer = self.questions[self.current_question_index]
        
        self.draw_text(f"Question {self.current_question_index + 1}/{len(self.questions)}", 
                      FONT_MEDIUM, WHITE, SCREEN_WIDTH // 2, 120, center=True)
        
        # Afficher la question (multi-lignes si nécessaire)
        if not hasattr(self, 'current_question_lines') or self.current_question_lines_index != self.current_question_index:
            words = question.split()
            lines = []
            current_line = []
            max_width = SCREEN_WIDTH - 100
            for word in words:
                current_line.append(word)
                test_line = " ".join(current_line)
                if FONT_MEDIUM.size(test_line)[0] > max_width:
                    current_line.pop()
                    if current_line:
                        lines.append(" ".join(current_line))
                    current_line = [word]
            if current_line:
                lines.append(" ".join(current_line))
            self.current_question_lines = lines
            self.current_question_lines_index = self.current_question_index
        else:
            lines = self.current_question_lines
        
        y = 180
        for line in lines:
            self.draw_text(line, FONT_MEDIUM, WHITE, SCREEN_WIDTH // 2, y, center=True)
            y += 40
        
        # Zone de réponse
        input_rect = pygame.Rect(SCREEN_WIDTH // 2 - 300, y + 40, 600, 50)
        color = LIGHT_BLUE if self.input_active else GRAY
        pygame.draw.rect(self.screen, color, input_rect, border_radius=5)
        pygame.draw.rect(self.screen, WHITE, input_rect, 2, border_radius=5)
        
        self.draw_text(self.user_input, FONT_MEDIUM, BLACK, input_rect.x + 10, input_rect.y + 10)
        
        # Bouton valider (cache avec position dynamique)
        if not hasattr(self, 'quiz_validate_button') or self.quiz_validate_y != y + 120:
            self.quiz_validate_button = Button(SCREEN_WIDTH // 2 - 100, y + 120, 200, 50, "VALIDER", GREEN, LIGHT_BLUE)
            self.quiz_validate_y = y + 120
        self.quiz_validate_button.draw(self.screen)
        
        if self.message:
            self.draw_text(self.message, FONT_SMALL, self.message_color, 
                          SCREEN_WIDTH // 2, y + 200, center=True)
        
        return [input_rect, self.quiz_validate_button]
    
    def draw_boss(self):
        """Dessine l'écran du boss."""
        self.screen.fill(RED)
        
        self.draw_text("=== COMBAT DE BOSS ===", FONT_LARGE, YELLOW, 
                      SCREEN_WIDTH // 2, 80, center=True)
        
        # Si déjà répondu, afficher résultat et bouton continuer
        if self.boss_answered:
            self.draw_text(self.message, FONT_MEDIUM, self.message_color,
                          SCREEN_WIDTH // 2, 250, center=True)
            self.draw_text(f"Score: {self.score}", FONT_MEDIUM, WHITE,
                          SCREEN_WIDTH // 2, 320, center=True)
            if not hasattr(self, 'boss_continue_button'):
                self.boss_continue_button = Button(SCREEN_WIDTH // 2 - 100, 400, 200, 50, "CONTINUER", GREEN, LIGHT_BLUE)
            self.boss_continue_button.draw(self.screen)
            return [self.boss_continue_button]
        
        # Charger la question boss une seule fois (cache)
        if not hasattr(self, 'boss_question') or self.boss_question is None:
            boss_q = get_boss_question_for_category(self.current_category)
            
            if not boss_q:
                self.draw_text("Pas de question BOSS disponible", FONT_MEDIUM, WHITE, 
                              SCREEN_WIDTH // 2, 250, center=True)
                if not hasattr(self, 'boss_no_question_button'):
                    self.boss_no_question_button = Button(SCREEN_WIDTH // 2 - 100, 350, 200, 50, "CONTINUER", GREEN, LIGHT_BLUE)
                self.boss_no_question_button.draw(self.screen)
                return [self.boss_no_question_button]
            
            self.boss_question = boss_q
        
        question, answer = self.boss_question
        
        self.draw_text("Cette question vaut 50 points!", FONT_SMALL, YELLOW, 
                      SCREEN_WIDTH // 2, 150, center=True)
        self.draw_text("Une mauvaise réponse fait perdre 20 points", FONT_SMALL, YELLOW, 
                      SCREEN_WIDTH // 2, 180, center=True)
        
        # Question du boss (cache du découpage en lignes)
        if not hasattr(self, 'boss_question_lines') or self.boss_question_lines_text != question:
            words = question.split()
            lines = []
            current_line = []
            max_width = SCREEN_WIDTH - 100
            for word in words:
                current_line.append(word)
                test_line = " ".join(current_line)
                if FONT_MEDIUM.size(test_line)[0] > max_width:
                    current_line.pop()
                    if current_line:
                        lines.append(" ".join(current_line))
                    current_line = [word]
            if current_line:
                lines.append(" ".join(current_line))
            self.boss_question_lines = lines
            self.boss_question_lines_text = question
        else:
            lines = self.boss_question_lines
        
        y = 240
        for line in lines:
            self.draw_text(line, FONT_MEDIUM, WHITE, SCREEN_WIDTH // 2, y, center=True)
            y += 40
        
        # Zone de réponse
        input_rect = pygame.Rect(SCREEN_WIDTH // 2 - 300, y + 40, 600, 50)
        color = LIGHT_BLUE if self.input_active else GRAY
        pygame.draw.rect(self.screen, color, input_rect, border_radius=5)
        pygame.draw.rect(self.screen, WHITE, input_rect, 2, border_radius=5)
        
        self.draw_text(self.user_input, FONT_MEDIUM, BLACK, input_rect.x + 10, input_rect.y + 10)
        
        # Bouton valider (cache avec position dynamique)
        if not hasattr(self, 'boss_validate_button') or self.boss_validate_y != y + 120:
            self.boss_validate_button = Button(SCREEN_WIDTH // 2 - 100, y + 120, 200, 50, "VALIDER", GREEN, LIGHT_BLUE)
            self.boss_validate_y = y + 120
        self.boss_validate_button.draw(self.screen)
        
        if self.message:
            self.draw_text(self.message, FONT_SMALL, self.message_color, 
                          SCREEN_WIDTH // 2, y + 200, center=True)
        
        return [input_rect, self.boss_validate_button]
    
    def draw_stats(self):
        """Dessine l'écran des statistiques."""
        self.screen.fill(BLUE)
        
        self.draw_text("STATISTIQUES", FONT_LARGE, YELLOW, SCREEN_WIDTH // 2, 60, center=True)
        
        # Cache de l'historique
        if not hasattr(self, 'stats_history_cache') or self.stats_history_player != self.player_name:
            self.stats_history_cache = self.session_manager.get_player_history(self.player_name)
            self.stats_history_player = self.player_name
        history = self.stats_history_cache
        
        if not history:
            self.draw_text("Aucune partie jouée", FONT_MEDIUM, WHITE, 
                          SCREEN_WIDTH // 2, 250, center=True)
        else:
            y = 150
            self.draw_text(f"Joueur: {self.player_name}", FONT_MEDIUM, WHITE, 100, y)
            y += 50
            self.draw_text(f"Nombre de parties: {len(history)}", FONT_SMALL, WHITE, 100, y)
            y += 40
            self.draw_text(f"Meilleur score: {max(s['score'] for s in history)}", FONT_SMALL, WHITE, 100, y)
            y += 60
            
            # Dernière session
            last = history[0]
            self.draw_text("Dernière partie:", FONT_MEDIUM, YELLOW, 100, y)
            y += 50
            self.draw_text(f"Date: {last['date']}", FONT_SMALL, WHITE, 120, y)
            y += 35
            self.draw_text(f"Score: {last['score']}", FONT_SMALL, WHITE, 120, y)
            y += 35
            self.draw_text(f"Questions: {last['questions_answered']}", FONT_SMALL, WHITE, 120, y)
            y += 35
            self.draw_text(f"Bonnes réponses: {last['correct_answers']}", FONT_SMALL, WHITE, 120, y)
            y += 35
            self.draw_text(f"Précision: {last['accuracy']:.1f}%", FONT_SMALL, WHITE, 120, y)
        
        if not hasattr(self, 'stats_back_button'):
            self.stats_back_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 50, "RETOUR", GRAY, DARK_GRAY)
        self.stats_back_button.draw(self.screen)
        
        return [self.stats_back_button]
    
    def handle_menu_events(self, event, buttons):
        """Gère les événements du menu principal."""
        for i, btn in enumerate(buttons):
            if btn.handle_event(event):
                if i == 0:  # JOUER
                    self.state = "NAME_INPUT"
                    self.user_input = ""
                    self.message = ""
                elif i == 1:  # REPRENDRE
                    etat = charger_progression("progression.json")
                    if etat:
                        self.player_name = etat.get("nom", "")
                        self.score = int(etat.get("score", 0))
                        self.played_categories = set(str(c) for c in etat.get("categories_jouees", []))
                        self.session_manager.create_player(self.player_name)
                        self.session_id = self.session_manager.create_game_session(self.player_name)
                        self.state = "CATEGORY_SELECT"
                    else:
                        self.message = "Aucune progression trouvée"
                elif i == 2:  # RESTART
                    self.state = "NAME_INPUT"
                    self.user_input = ""
                    reset_progression("progression.json")
                elif i == 3:  # STATISTIQUES
                    self.state = "NAME_INPUT"
                    self.user_input = ""
                    self.message = "Entrez votre nom pour voir vos stats"
                    self.next_state_after_name = "STATS"
                elif i == 4:  # QUITTER
                    self.running = False
    
    def handle_name_input_events(self, event, elements):
        """Gère les événements de saisie du nom."""
        input_rect, btn_validate = elements
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_rect.collidepoint(event.pos):
                self.input_active = True
            else:
                self.input_active = False
        
        if event.type == pygame.KEYDOWN and self.input_active:
            if event.key == pygame.K_RETURN:
                self.validate_name()
            elif event.key == pygame.K_BACKSPACE:
                self.user_input = self.user_input[:-1]
            else:
                if len(self.user_input) < 20:
                    self.user_input += event.unicode
        
        if btn_validate.handle_event(event):
            self.validate_name()
    
    def validate_name(self):
        """Valide le nom du joueur."""
        if self.user_input.strip():
            self.player_name = self.user_input.strip()
            self.session_manager.create_player(self.player_name)
            
            if hasattr(self, 'next_state_after_name') and self.next_state_after_name == "STATS":
                self.state = "STATS"
                delattr(self, 'next_state_after_name')
            else:
                self.session_id = self.session_manager.create_game_session(self.player_name)
                self.state = "CATEGORY_SELECT"
        else:
            self.message = "Veuillez entrer un nom"
            self.message_color = RED
    
    def handle_category_events(self, event, buttons):
        """Gère les événements de sélection de catégorie."""
        for btn in buttons:
            if btn.handle_event(event):
                if btn.text == "QUITTER":
                    self.save_progression()
                    self.state = "MENU"
                elif btn.text == "VOIR STATS":
                    self.state = "STATS"
                elif hasattr(btn, 'cat_id'):
                    self.current_category = btn.cat_id
                    self.questions = self.questions_by_category[btn.cat_id][:20]
                    self.current_question_index = 0
                    self.user_input = ""
                    self.message = ""
                    self.state = "QUIZ"
    
    def handle_quiz_events(self, event, elements):
        """Gère les événements du quiz."""
        if len(elements) == 2 and isinstance(elements[0], Button):
            # Quiz terminé - choix boss
            btn_boss, btn_skip = elements
            if btn_boss.handle_event(event):
                self.state = "BOSS"
                self.user_input = ""
                self.message = ""
                self.boss_answered = False
                # Nettoyer les caches du boss pour un nouveau combat
                if hasattr(self, 'boss_question_lines'):
                    delattr(self, 'boss_question_lines')
                if hasattr(self, 'boss_question_lines_text'):
                    delattr(self, 'boss_question_lines_text')
                if hasattr(self, 'boss_question'):
                    delattr(self, 'boss_question')
            elif btn_skip.handle_event(event):
                self.played_categories.add(self.current_category)
                self.save_progression()
                self.state = "CATEGORY_SELECT"
        else:
            input_rect, btn_validate = elements
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    self.input_active = True
                else:
                    self.input_active = False
            
            if event.type == pygame.KEYDOWN and self.input_active:
                if event.key == pygame.K_RETURN:
                    self.validate_answer()
                elif event.key == pygame.K_BACKSPACE:
                    self.user_input = self.user_input[:-1]
                else:
                    self.user_input += event.unicode
            
            if btn_validate.handle_event(event):
                self.validate_answer()
    
    def validate_answer(self):
        """Valide la réponse du joueur."""
        if self.current_question_index < len(self.questions):
            question, answer = self.questions[self.current_question_index]
            correct = self.user_input.strip().lower() == answer.strip().lower()
            
            if correct:
                self.score += 10
                self.message = "Correct! +10 points"
                self.message_color = GREEN
            else:
                self.score -= 5
                self.message = f"Incorrect. Réponse: {answer} (-5 points)"
                self.message_color = RED
            
            try:
                self.session_manager.add_question_to_session_with_category(
                    self.session_id, self.current_question_index + 1, correct, int(self.current_category)
                )
            except:
                pass
            
            self.current_question_index += 1
            self.user_input = ""
            self.show_feedback = True
            self.feedback_timer = 0
    
    def handle_boss_events(self, event, elements):
        """Gère les événements du combat de boss."""
        if len(elements) == 1 and elements[0].text == "CONTINUER":
            if elements[0].handle_event(event):
                self.played_categories.add(self.current_category)
                self.save_progression()
                self.boss_answered = False
                # Nettoyer les caches du boss
                if hasattr(self, 'boss_question_lines'):
                    delattr(self, 'boss_question_lines')
                if hasattr(self, 'boss_question_lines_text'):
                    delattr(self, 'boss_question_lines_text')
                if hasattr(self, 'boss_question'):
                    delattr(self, 'boss_question')
                self.state = "CATEGORY_SELECT"
        else:
            input_rect, btn_validate = elements
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    self.input_active = True
                else:
                    self.input_active = False
            
            if event.type == pygame.KEYDOWN and self.input_active:
                if event.key == pygame.K_RETURN:
                    self.validate_boss_answer()
                elif event.key == pygame.K_BACKSPACE:
                    self.user_input = self.user_input[:-1]
                else:
                    self.user_input += event.unicode
            
            if btn_validate.handle_event(event):
                self.validate_boss_answer()
    
    def validate_boss_answer(self):
        """Valide la réponse au boss."""
        if hasattr(self, 'boss_question') and not self.boss_answered:
            question, answer = self.boss_question
            correct = self.user_input.strip().lower() == answer.strip().lower()
            
            if correct:
                self.score += 50
                self.message = "BRAVO! Boss vaincu! +50 points"
                self.message_color = YELLOW
            else:
                self.score -= 20
                self.message = f"Défaite! Réponse: {answer} (-20 points)"
                self.message_color = RED
            
            try:
                self.session_manager.add_question_to_session_with_category(
                    self.session_id, None, correct, int(self.current_category)
                )
            except:
                pass
            
            self.save_progression()
            self.user_input = ""
            self.boss_answered = True
    
    def handle_stats_events(self, event, buttons):
        """Gère les événements de l'écran des stats."""
        for btn in buttons:
            if btn.handle_event(event):
                self.state = "MENU"
    
    def save_progression(self):
        """Sauvegarde la progression."""
        try:
            sauvegarder_progression(self.player_name, self.score, list(self.played_categories))
            self.session_manager.update_game_session_score(self.session_id, self.score)
            self.session_manager.update_player_score(self.player_name, self.score)
        except Exception as e:
            print(f"Erreur sauvegarde: {e}")
    
    def run(self):
        """Boucle principale du jeu."""
        while self.running:
            self.clock.tick(FPS)
            
            # Gérer le timer de feedback
            if self.show_feedback:
                self.feedback_timer += 1
                if self.feedback_timer >= self.feedback_duration:
                    self.show_feedback = False
                    self.message = ""
                    self.feedback_timer = 0
            
            # Dessiner l'écran actuel d'abord
            if self.state == "MENU":
                buttons = self.draw_menu()
            elif self.state == "NAME_INPUT":
                elements = self.draw_name_input()
            elif self.state == "CATEGORY_SELECT":
                buttons = self.draw_category_select()
            elif self.state == "QUIZ":
                elements = self.draw_quiz()
            elif self.state == "BOSS":
                elements = self.draw_boss()
            elif self.state == "STATS":
                buttons = self.draw_stats()
            
            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                # Gérer les événements selon l'état
                if self.state == "MENU":
                    self.handle_menu_events(event, buttons)
                elif self.state == "NAME_INPUT":
                    self.handle_name_input_events(event, elements)
                elif self.state == "CATEGORY_SELECT":
                    self.handle_category_events(event, buttons)
                elif self.state == "QUIZ":
                    self.handle_quiz_events(event, elements)
                elif self.state == "BOSS":
                    self.handle_boss_events(event, elements)
                elif self.state == "STATS":
                    self.handle_stats_events(event, buttons)
            
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = QuizGame()
    game.run()

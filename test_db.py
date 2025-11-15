from Player_session import PlayerSession

s = PlayerSession()
print(s.create_player("DebugUser"))
sid = s.create_game_session("DebugUser")
print("session id:", sid)
if sid:
    s.add_category_to_session(sid, 2)
    s.add_question_to_session_with_category(sid, 1, True, 2)
    s.update_game_session_score(sid, 42)

print("History:", s.get_player_history("DebugUser"))

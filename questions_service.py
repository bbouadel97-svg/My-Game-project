import re
from pathlib import Path
from typing import Dict, List, Tuple


def load_questions_from_sql(sql_path: Path) -> Dict[str, List[Tuple[str, str]]]:
	"""Parse un fichier SQL et retourne un mapping table -> list[(question, answer)].

	Le parser est simple et cible les INSERT INTO statements présents dans
	`Project 0/Script-1.sql` où les valeurs sont des tuples (question, answer).
	"""
	if not sql_path.exists():
		raise FileNotFoundError(f"Fichier SQL introuvable: {sql_path}")

	text = sql_path.read_text(encoding='utf-8')

	# Rechercher tous les INSERT INTO table (...) VALUES ...; (multiligne possible)
	insert_re = re.compile(r"INSERT\s+INTO\s+(\w+)\s*\([^)]*\)\s*VALUES\s*(.+?);", re.IGNORECASE | re.DOTALL)

	# Rechercher des tuples de la forme ('question','answer') ou ["question","answer"]
	tuple_re = re.compile(r"\(?\s*(['\"])(.*?)\1\s*,\s*(['\"])(.*?)\3\s*\)?", re.DOTALL)

	result: Dict[str, List[Tuple[str, str]]] = {}

	for match in insert_re.finditer(text):
		table = match.group(1)
		values_blob = match.group(2)
		pairs: List[Tuple[str, str]] = []

		for tmatch in tuple_re.finditer(values_blob):
			q = tmatch.group(2).strip()
			a = tmatch.group(4).strip()
			pairs.append((q, a))

		if pairs:
			result[table] = pairs

	return result


if __name__ == "__main__":
	# Test rapide si on exécute le module directement
	sql = Path(__file__).parent / 'Project 0' / 'Script-1.sql'
	try:
		data = load_questions_from_sql(sql)
		for table, items in data.items():
			print(f"{table}: {len(items)} questions")
	except Exception as e:
		print("Erreur lors du chargement des questions:", e)

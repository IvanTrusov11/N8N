import json
import os
import re
import sys

# Если передан аргумент - используем его, иначе папка скрипта
if len(sys.argv) > 1:
    folder = sys.argv[1]
else:
    folder = os.path.dirname(os.path.abspath(__file__))

for filename in os.listdir(folder):
    if not filename.endswith('.json'):
        continue

    filepath = os.path.join(folder, filename)

    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    name = data.get('name', '').strip()
    if not name:
        continue

    safe = re.sub(r'[\\/:*?"<>|]', '_', name)
    new_filename = safe + '.json'
    new_filepath = os.path.join(folder, new_filename)

    if filename == new_filename:
        continue

    if os.path.exists(new_filepath):
        print(f"SKIP (уже есть): {new_filename}")
        continue

    os.rename(filepath, new_filepath)
    print(f"{filename} -> {new_filename}")

print("Готово")
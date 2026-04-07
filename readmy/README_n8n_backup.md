# N8N Workflows Backup

Бэкап воркфлоу из локального n8n (Docker) на GitHub.

---

## Экспорт и пуш (делать когда нужно обновить)

```bash
# 1. Экспортировать все воркфлоу внутри контейнера
docker exec n8n n8n export:workflow --all --backup --output=//home/node/.n8n/workflows-backup/

# 2. Запаковать в архив (MSYS_NO_PATHCONV нужен для Git Bash)
MSYS_NO_PATHCONV=1 docker exec n8n tar -czf /tmp/workflows.tar.gz -C /home/node/.n8n/workflows-backup .

# 3. Вытащить архив на хост
MSYS_NO_PATHCONV=1 docker exec n8n cat /tmp/workflows.tar.gz > /c/tmp/workflows.tar.gz

# 4. Распаковать в папку репозитория
tar -xzf /c/tmp/workflows.tar.gz -C ~/desktop/git_ivtru11/n8n/

# 5. Переименовать файлы по полю name внутри JSON
cd ~/desktop/git_ivtru11/n8n
python rename.py

# 6. Запушить на GitHub
git add .
git commit -m "update workflows"
git push
```

---

## Восстановление (импорт обратно в n8n)

```bash
# 1. Клонировать репо (если нужно)
git clone https://github.com/IvanTrusov11/N8N.git ~/desktop/git_ivtru11/n8n

# 2. Скопировать JSON файлы обратно в контейнер
MSYS_NO_PATHCONV=1 docker exec n8n mkdir -p /home/node/.n8n/workflows-restore
tar -czf /c/tmp/restore.tar.gz -C ~/desktop/git_ivtru11/n8n .
MSYS_NO_PATHCONV=1 docker exec n8n sh -c 'cat > /tmp/restore.tar.gz' < /c/tmp/restore.tar.gz
MSYS_NO_PATHCONV=1 docker exec n8n tar -xzf /tmp/restore.tar.gz -C /home/node/.n8n/workflows-restore/

# 3. Импортировать все воркфлоу в n8n
MSYS_NO_PATHCONV=1 docker exec n8n n8n import:workflow --separate --input=/home/node/.n8n/workflows-restore/
```

---

## Структура

```
N8N/
├── README.md
├── rename.py
└── *.json     # каждый воркфлоу отдельным файлом (имя = name из JSON)
```

---

## rename.py

Переименовывает файлы вида `2Uct4DZlKoA95E9L.json` в читаемые названия по полю `name` внутри JSON.

```python
import json
import os
import re

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
```

---

## Заметки

- Credentials не экспортируются и не хранятся здесь
- Контейнер называется `n8n`
- Воркфлоу хранятся в Docker volume `n8n_data`, прямой доступ с хоста невозможен
- Git Bash требует `MSYS_NO_PATHCONV=1` для путей внутри контейнера

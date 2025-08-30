from analyzer.workspace import make_workspace
from analyzer.downloader import download_repo
from analyzer.deps_audit import audit_dependencies
import json
from pathlib import Path

repo_url = input("Введите ссылку на репозиторий: ")
ws = make_workspace(repo_url)
print("Создана рабочая папка:", ws)
repo_path = Path(ws)/"repo"
print("Путь для клонирования репозитория:", repo_path)
print("Проверка, что папка создана:", repo_path.parent.exists())
print("Проверка, что папка пуста:", not any(repo_path.parent.iterdir()))
ok, out = download_repo(repo_url, str(repo_path))
print("Клонирование прошло успешно?", ok)
print("Вывод git clone:")
print(out)
if ok:
    ok_audit, out_json = audit_dependencies(str(repo_path))
    print("Аудит зависимостей успешен?", ok_audit)
    print("Сырый JSON (первые 300 символов):")
    print(out_json[:300] if out_json else "пусто")
    try:
        data = json.loads(out_json) if out_json else {}
        print("Загруженные данные (ключи верхнего уровня):", list(data.keys()))
    except Exception as ex:
        print("Ошибка при разборе JSON:", ex)
else:
    print("Аудит зависимостей пропущен из-за ошибки клонирования.")





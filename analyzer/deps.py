from pathlib import Path

def find_deps_file(repo_dir: str) -> tuple[bool, str | None]:
    """
    Ищет в корне repo_dir один из файлов зависимостей:
    - requirements.txt
    - pyproject.toml
    - Pipfile
    Возвращает (found, path) — found=True и абсолютный путь, если найден.
    """
    repo_path = Path(repo_dir).resolve()
    deps_files = ["requirements.txt", "pyproject.toml", "Pipfile"]

    for deps_file in deps_files:
        file_path = repo_path / deps_file
        if file_path.is_file():
            return True, str(file_path.resolve())

    return False, None

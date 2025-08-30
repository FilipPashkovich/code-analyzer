from analyzer.deps import find_deps_file
import subprocess as sp
import sys

def audit_dependencies(repo_dir: str) -> tuple[bool, str | None]:
    """
    Ищет в repo_dir файл зависимостей (requirements.txt / pyproject.toml / Pipfile)
    и запускает pip-audit c универсальным ключом --path.
    Возвращает (success, output_json_or_error).
    """
    found, deps_path = find_deps_file(repo_dir)
    print(f"Найден файл зависимостей: {deps_path}" if found else "Файл зависимостей не найден.")
    if not found:
        return False, "Файл зависимостей не найден (requirements.txt / pyproject.toml / Pipfile)."

    # используем текущий python для вызова модуля
    cmd = [
        sys.executable, "-m", "pip_audit",
        "--path", deps_path,
        "-f", "json",
    ]

    try:
        result = sp.run(
            cmd,
            check=True,
            capture_output=True,
            text=True,
            timeout=120,
        )
        # JSON только из stdout
        output = (result.stdout or "").strip()

        # stderr можно напечатать в логах, но НЕ смешивать с JSON
        if result.stderr.strip():
            print("pip-audit stderr:", result.stderr.strip())

        return True, output

    except sp.CalledProcessError as e:
        err = (e.stderr or e.stdout or "").strip()
        if "not found" in err.lower() and "pip-audit" in err:
            err = "pip-audit не найден. Установи его в venv: `pip install pip-audit`."
        return False, err or "Ошибка запуска pip-audit."

    except sp.TimeoutExpired:
        return False, "⏱️ Таймаут pip-audit (120с). Проверь сеть/доступ к реестрам."

    except FileNotFoundError:
        return False, "Команда не найдена. Убедись, что активирован venv и pip-audit установлен."

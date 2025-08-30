import subprocess as sp


def download_repo(repo_url: str, dest_dir: str) -> tuple[bool, str]:
    """
    Клонирует репозиторий по URL в папку dest_dir (только последний коммит).
    Возвращает:
      (success: bool, output: str)
        success = True, если клонирование прошло без ошибок;
        output  = объединённый/полезный текст stdout/stderr для логов.
    """
    # 1) Сформировать команду git clone с оптимизациями
    cmd = [
        "git", "clone",
        "--depth", "1",           # только последняя версия
        "--single-branch",        # не тащим все ветки
        "--no-tags",              # не тащим теги
        repo_url,
        dest_dir,
    ]

    try:
        # 2) Запустить процесс
        result = sp.run(
            cmd,
            check=True,               # ошибка → исключение
            capture_output=True,      # перехватываем вывод
            text=True,                # строки, не байты
            timeout=120,              # защита от зависания
        )

        # 3) Собрать полезный вывод (git часто пишет служебное в stderr)
        out_parts = []
        if result.stdout:
            out_parts.append(result.stdout.strip())
        if result.stderr:
            out_parts.append(result.stderr.strip())
        output = "\n".join(out_parts) if out_parts else "Clone completed."
        print(f"✅ Репозиторий успешно клонирован в {dest_dir}")
        return True, output

    except FileNotFoundError:
        msg = "git не найден. Установи: brew install git (и проверь PATH)."
        print(f"❌ {msg}")
        return False, msg

    except sp.TimeoutExpired:
        print("Таймаут клонирования (120с). Проверь сеть/URL.")
        return False, "Таймаут клонирования (120с). Проверь сеть/URL."

    except sp.CalledProcessError as e:
        err = (e.stderr or e.stdout or "").strip()
        if "already exists" in err:
            print(f"⚠️ Папка {dest_dir} уже существует.")
        else:
            print(f"❌ Ошибка клонирования: {err}")
        if not err:
            err = "Ошибка клонирования. Проверь URL и доступ к git."
        return False, err or "Ошибка клонирования."

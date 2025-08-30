from datetime import datetime
import os
import uuid
from pathlib import Path

def make_workspace(repo_url: str, base: str = "runs") -> str:
    """
    Возвращает путь к созданной папке вида:
    runs/<YYYYmmdd-HHMM>-<repo-slug>-<short-uuid>/
    """
    ts=datetime.now().strftime("%Y%m%d-%H%M")
    short_id=str(uuid.uuid4())[:8]
    slug=f"{repo_url.split('/')[-1].replace('.git','')}-{ts}-{short_id}"
    path=Path(base)/slug
    path.mkdir(parents=True, exist_ok=True)
    return str(path)

from analyzer.deps_audit import audit_dependencies

path = "runs/requirements-20250829-1549-ce903438/repo"
ok, out = audit_dependencies(path)
print("Аудит зависимостей успешен?", ok)
print("Сырый JSON (первые 300 символов):")
print(out[:300] if out else "пусто")

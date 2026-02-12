import os

def ensure_dir(path: str) -> None:
    if path and not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)

def safe_join(base: str, filename: str) -> str:
    # evita cosas raras tipo ../
    filename = os.path.basename(filename)
    return os.path.join(base, filename)

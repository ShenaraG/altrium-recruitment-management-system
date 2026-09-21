import os


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def _read(path):
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read()

import os


def find_project_root(
    markers=("pyproject.toml", ".git", os.path.join("config", "settings.yaml"))
) -> str:
    """
    Walks up from the current working directory until a marker file is found.
    Returns the absolute path to the project root directory.
    """
    current = os.path.abspath(os.getcwd())
    while True:
        for marker in markers:
            if os.path.exists(os.path.join(current, marker)):
                return current
        parent = os.path.dirname(current)
        if parent == current:
            break
        current = parent
    raise FileNotFoundError(f"Project root not found. Looked for any of: {', '.join(markers)}")

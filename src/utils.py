from .load_config import users_file_path


def get_db_size() -> str:
    """Returns user base size in string format or error"""
    try:
        with open(users_file_path, "r", encoding="utf-8") as file:
            return str(len(file.readlines()))
    except Exception as e:
        return e

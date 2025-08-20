MAX_NAME_LENGTH = 90

def truncate_string(text: str) -> str:
    max_length = MAX_NAME_LENGTH
    if len(text) > max_length:
        return text[:max_length - 3] + "..."
    return text
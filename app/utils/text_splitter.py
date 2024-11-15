def split_text_into_chunks(text: str, chunk_size: int = 1000) -> list:
    return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]

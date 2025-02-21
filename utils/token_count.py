# utils/token_count.py
import tiktoken

def get_token_count(text: str, model: str = "text-embedding-ada-002") -> int:
    """
    Returns the number of tokens in the given text using the tokenizer for the specified model.
    """
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(text)
    return len(tokens)
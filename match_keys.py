import difflib
import re

def replace_keys_with_fuzzy_match(data: dict, target_keys: list) -> dict:
    """
    Replace the keys in the input dictionary 'data' with the closest matching key from 'target_keys'.
    The target keys are assumed to be LaTeX formatted strings (e.g., '\\text{TradeAmount}').
    
    Args:
        data (dict): The original dictionary with keys to be replaced.
        target_keys (list): A list of target keys (as LaTeX formatted strings) to match against.
    
    Returns:
        dict: A new dictionary with keys replaced by matching target keys.
    """
    # Function to extract the inner text from a LaTeX formatted target key.
    def extract_inner_text(latex_str: str) -> str:
        match = re.search(r'\{(.+?)\}', latex_str)
        return match.group(1) if match else latex_str

    # Build a mapping from the inner text to the original formatted target key.
    inner_to_full = {extract_inner_text(tk): tk for tk in target_keys}
    
    # List of inner text keys to match against.
    target_inner_texts = list(inner_to_full.keys())
    
    # Function to find the best matching inner text.
    def find_best_match(key: str, target_list: list) -> str:
        match_list = difflib.get_close_matches(key, target_list, n=1, cutoff=0)
        return match_list[0] if match_list else key

    # Build the new dictionary with replaced keys.
    new_data = {}
    for key, value in data.items():
        best_inner_match = find_best_match(key, target_inner_texts)
        # Use the full LaTeX formatted key if found; otherwise, keep the original key.
        new_key = inner_to_full.get(best_inner_match, key)
        new_data[new_key] = value

    return new_data
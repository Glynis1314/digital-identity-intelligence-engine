from difflib import SequenceMatcher


# Compare text similarity
def similarity_score(text1, text2):

    if not text1 or not text2:
        return 0

    text1 = text1.lower()
    text2 = text2.lower()

    similarity = SequenceMatcher(
        None,
        text1,
        text2
    ).ratio()

    return similarity
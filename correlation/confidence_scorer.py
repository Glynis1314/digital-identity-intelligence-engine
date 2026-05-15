from utils.similarity import similarity_score


def calculate_confidence(
    email,
    username,
    found,
    profile_name=None,
    bio=None
):

    score = 0

    # Email local part
    local_part = email.split("@")[0].lower()

    username = username.lower()

    # Found profile
    if found:
        score += 20

    # Exact username match
    if username == local_part:
        score += 30

    # Cleaned username match
    cleaned_email = (
        local_part
        .replace(".", "")
        .replace("_", "")
    )

    if username == cleaned_email:
        score += 25

    # Partial username match
    if username in cleaned_email:
        score += 15

    # Profile name similarity
    if profile_name:

        name_similarity = similarity_score(
            local_part,
            profile_name
        )

        score += int(name_similarity * 30)

    # Bio similarity
    if bio:

        bio_similarity = similarity_score(
            local_part,
            bio
        )

        score += int(bio_similarity * 10)

    # Limit max score
    score = min(score, 100)

    return score
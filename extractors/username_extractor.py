import re


def extract_usernames(email):

    # Extract local part before @
    local_part = email.split("@")[0]

    # Store username variations
    usernames = set()

    # Original
    usernames.add(local_part)

    # Remove dots
    usernames.add(local_part.replace(".", ""))

    # Remove underscores
    usernames.add(local_part.replace("_", ""))

    # Remove special characters
    cleaned = re.sub(r'[^a-zA-Z0-9]', '', local_part)
    usernames.add(cleaned)

    # Split into words/numbers
    parts = re.split(r'[._]', local_part)

    for part in parts:
        if len(part) > 2:
            usernames.add(part)

    # Combine first two parts
    if len(parts) >= 2:
        combined = parts[0] + parts[1]
        usernames.add(combined)

    # Remove empty values
    usernames = [u for u in usernames if u]

    return list(usernames)
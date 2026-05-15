def classify_risk(confidence):

    if confidence >= 70:
        return "HIGH"

    elif confidence >= 40:
        return "MEDIUM"

    else:
        return "LOW"
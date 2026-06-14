keywords = [
    "otp",
    "verify",
    "urgent",
    "bank",
    "password",
    "kyc",
    "winner",
    "prize"
]

def detect_threat(text):

    text = str(text).lower()

    score = 0

    found_keywords = []

    for word in keywords:
        if word in text:
            score += 1
            found_keywords.append(word)

    if score >= 4:
        level = "High Risk"
    elif score >= 2:
        level = "Medium Risk"
    else:
        level = "Low Risk"

    return score, level, found_keywords

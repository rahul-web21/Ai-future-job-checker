def calculate_future_score(answer):
    score = 70
    text = answer.lower()

    if "automate" in text:
        score -= 10
    if "human" in text:
        score += 10
    if "critical" in text:
        score += 10

    return max(0, min(score, 100))
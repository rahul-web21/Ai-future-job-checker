def evaluate_answer(answer):
    score = 0
    if len(answer) > 150:
        score += 1
    if "AI" in answer:
        score += 1
    if "skill" in answer.lower():
        score += 1
    if "future" in answer.lower():
        score += 1

    return {
        "quality_score": score,
        "max_score": 4
    }
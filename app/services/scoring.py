import random

def score_result(result: dict):
    total = result.get("claims_checked", 0)
    verified = result.get("verified_count", 0)

    if total == 0:
        return random.randint(0, 30) 

    raw_percent = (verified / total) * 100

    if raw_percent <= 20: 
        score = random.randint(0, 30)
    elif raw_percent >= 90:  
        score = random.randint(80, 100)
    else:
        score = 30 + ((raw_percent - 20) / (90 - 20)) * (80 - 30)
        score = round(score)

    return score

def score_result(result: dict):
    total = result.get("claims_checked", 0)
    verified = result.get("verified_count", 0)

    if total == 0:
        return 0

    base_score = (verified / total) * 100
    return round(base_score)

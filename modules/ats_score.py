def calculate_ats_score(skill_match_result, jd_data):

    matched_count = len(
        skill_match_result["matched_skills"]
    )

    total_required = len(
        jd_data.get("required_skills", [])
    )

    if total_required == 0:
        return 0

    score = (
        matched_count / total_required
    ) * 100

    return round(score, 2)
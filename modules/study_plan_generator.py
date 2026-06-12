import ollama

def generate_study_plan(missing_skills, interview_report):

    prompt = f"""
    Create a personalized 7-day interview preparation study plan.

    Missing Skills:
    {missing_skills}

    Interview Report:
    {interview_report}

    Provide the following:

    Weak Areas:
    - List weak areas

    Day 1:
    - Topics

    Day 2:
    - Topics

    Day 3:
    - Topics

    Day 4:
    - Topics

    Day 5:
    - Topics

    Day 6:
    - Topics

    Day 7:
    - Topics

    Recommended Resources:
    - Resources for learning

    Final Preparation Tips:
    - Tips before interview
    """

    response = ollama.chat(
        model="qwen2.5:1.5b",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response["message"]["content"]
import ollama


def generate_interview_report(user_answers):

    prompt = f"""
    You are an expert technical interviewer.

    Analyze the following interview answers:

    {user_answers}

    Provide:

    1. Overall Score out of 100
    2. Strengths
    3. Weaknesses
    4. Recommendations

    Format nicely.
    """

    response = ollama.chat(
        model="qwen2.5:1.5b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]
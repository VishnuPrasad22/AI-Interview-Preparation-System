import ollama


def generate_questions(
    resume_data,
    jd_data,
    skill_match_result
):

    prompt = prompt = f"""
You are an expert technical interviewer.

Resume Data:
{resume_data}

Job Description Data:
{jd_data}

Skill Match Result:
{skill_match_result}

Generate exactly 15 interview questions.

Requirements:
- 5 Resume-Based Questions
- 5 JD-Based Questions
- 5 Missing Skill Questions

Return ONLY numbered questions.

Example:

1. What is Python?
2. Explain OOP concepts.
3. What is SQL normalization?

Do not add headings.
Do not add categories.
Do not add explanations.
Do not add markdown.
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
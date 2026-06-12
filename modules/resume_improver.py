import ollama


def generate_resume_suggestions(
    resume_data,
    jd_data,
    skill_match_result
):

    prompt = f"""
Resume:
{resume_data}

Job Description:
{jd_data}

Missing Skills:
{skill_match_result["missing_skills"]}

Give 5 resume improvement suggestions.
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
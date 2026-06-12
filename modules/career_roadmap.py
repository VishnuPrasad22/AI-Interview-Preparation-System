import ollama


def generate_career_roadmap(
    resume_data,
    jd_data,
    missing_skills
):

    prompt = f"""
You are an AI Career Coach.

Resume Data:
{resume_data}

Job Description:
{jd_data}

Missing Skills:
{missing_skills}

Create a detailed 6-week roadmap.

Format:

Week 1:
- Topics

Week 2:
- Topics

Week 3:
- Topics

Week 4:
- Topics

Week 5:
- Topics

Week 6:
- Topics

Final Goal:
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
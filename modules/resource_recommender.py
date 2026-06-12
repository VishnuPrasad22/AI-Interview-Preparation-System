RESOURCE_MAP = {

    "python": [
        "Python Official Tutorial",
        "https://docs.python.org/3/tutorial/",
        "https://realpython.com/",
        "https://youtu.be/QXeEoD0pB3E?si=h9h5-uAgpixJmSrE",
        "https://youtu.be/_uQrJ0TkZlc?si=uP3-IyMbKwJMicjx"
    ],

    "sql": [
        "W3Schools SQL",
        "https://www.w3schools.com/sql/",
        "https://www.geeksforgeeks.org/sql-tutorial/",
        "https://youtu.be/7S_tz1z_5bA?si=kYJtLrqXFEKRODp1"
    ],

    "java": [
        "Java Official Docs",
        "https://docs.oracle.com/javase/tutorial/",
        "https://www.geeksforgeeks.org/java/"
    ],

    "machine learning": [
        "Scikit-Learn",
        "https://scikit-learn.org/stable/user_guide.html",
        "https://www.kaggle.com/learn"
    ],

    "deep learning": [
        "TensorFlow Tutorials",
        "https://www.tensorflow.org/tutorials",
        "https://pytorch.org/tutorials/"
    ],

    "Generative-AI": [
        "RAG",
        "https://aws.amazon.com/what-is/retrieval-augmented-generation/"
    ]
}


def recommend_resources(missing_skills):

    recommendations = {}

    for skill in missing_skills:

        skill_lower = skill.lower().strip()

        for key in RESOURCE_MAP:

            if key in skill_lower or skill_lower in key:
                recommendations[skill] = RESOURCE_MAP[key]

    return recommendations
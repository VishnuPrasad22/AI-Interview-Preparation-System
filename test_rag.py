from modules.rag_engine import ask_interview_coach

question = "What is normalization in DBMS?"

answer = ask_interview_coach(question)

print("\nAnswer:\n")
print(answer)
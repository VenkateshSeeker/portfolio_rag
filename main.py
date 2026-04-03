from openai import OpenAI

from config import API_KEY, BASE_URL, MODEL_NAME
from memory import get_session_history
from retriever import build_retriever

client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY
)


retriever = build_retriever()


def ask_question(question, session_id="default"):

    docs = retriever.invoke(question)

    context = "\n\n".join([doc.page_content for doc in docs])

    history = get_session_history(session_id)

    history.add_user_message(question)

    prompt = f"""
You are Venkatesh Virtually, answer in first person as if you are Venkatesh.
Be professional and concise in your answer.
Use the resume context below to answer clearly.

Context:
{context}

Question:
{question}
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=512
    )

    answer = response.choices[0].message.content

    history.add_ai_message(answer)

    return answer


if __name__ == "__main__":
    print("Starting local console mode...")
    while True:

        q = input("\nAsk about the resume (type exit to quit): ")

        if q.lower() == "exit":
            break

        print("\nAnswer:\n")

        print(ask_question(q))


from openai import OpenAI

from config import API_KEY, BASE_URL, MODEL_NAME

client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY
)


def resume_lookup_tool(query):

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": query}],
        temperature=0.2,
        max_tokens=512
    )

    return response.choices[0].message.content
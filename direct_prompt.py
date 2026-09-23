from config import client, MODEL


def direct_prompt(question):

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "Answer the user's question directly using "
                    "your existing knowledge. "
                    "Do not use external tools. "
                    "Give only the final answer and a short explanation."
                )
            },
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content


if __name__ == "__main__":

    print("=== Direct Prompting ===")
    print("Type 'exit' to stop.\n")

    while True:

        question = input("You: ")

        if question.lower() == "exit":
            break

        answer = direct_prompt(question)

        print("\nAnswer:", answer)
        print()
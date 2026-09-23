from config import client, MODEL


def chain_of_thought(question):

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a careful reasoning assistant. "
                    "Solve the user's problem step by step internally. "
                    "Do not use external tools. "
                    "After reasoning, provide a concise explanation "
                    "of the key calculation or logic and then give "
                    "the final answer."
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

    print("=== Chain-of-Thought Prompting ===")
    print("Type 'exit' to stop.\n")

    while True:

        question = input("You: ")

        if question.lower() == "exit":
            break

        answer = chain_of_thought(question)

        print("\nAnswer:", answer)
        print()
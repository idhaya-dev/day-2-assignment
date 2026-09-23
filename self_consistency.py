from collections import Counter

from config import client, MODEL


QUESTION = """
CS101 costs ₹30,000.
AI202 costs ₹40,000.
DS303 costs ₹35,000.

Option A:
CS101 and AI202 with a 10% scholarship.

Option B:
All three courses with a 25% scholarship.

Which option is cheaper, and by how much?
Give the final answer clearly.
"""


def ask_cot(question, temperature):

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "Solve the problem carefully using step-by-step "
                    "reasoning internally. Do not use external tools. "
                    "Give a concise explanation and a final answer."
                )
            },
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=temperature
    )

    return response.choices[0].message.content


if __name__ == "__main__":

    print("=== Self-Consistency Experiment ===")
    print()

    # Run multiple times with non-zero temperature
    temperature = 0.7
    runs = 5

    answers = []

    print(f"Running {runs} times with temperature={temperature}\n")

    for i in range(runs):

        answer = ask_cot(QUESTION, temperature)

        answers.append(answer)

        print(f"--- Run {i + 1} ---")
        print(answer)
        print()


    # Show the expected correct result
    print("=== Expected Calculation ===")

    option_a = (30000 + 40000) * 0.90
    option_b = (30000 + 40000 + 35000) * 0.75

    difference = option_b - option_a

    print(f"Option A = ₹{option_a:,.2f}")
    print(f"Option B = ₹{option_b:,.2f}")
    print(f"Option A is cheaper by ₹{difference:,.2f}")
    print()


    # Run once at temperature 0
    print("=== Temperature 0 ===")

    deterministic_answer = ask_cot(
        QUESTION,
        temperature=0
    )

    print(deterministic_answer)
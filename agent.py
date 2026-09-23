import json

from config import client, MODEL

from tools import (
    get_course_fee,
    calculate_discounted_fee
)


# Tools available to the ReAct agent
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_course_fee",
            "description": (
                "Get the official fee of a course from the "
                "private course database."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "course_code": {
                        "type": "string",
                        "description": "Course code such as CS101, AI202, or DS303"
                    }
                },
                "required": ["course_code"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "calculate_discounted_fee",
            "description": (
                "Calculate the final course fee after applying "
                "a scholarship percentage."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "course_code": {
                        "type": "string",
                        "description": "Course code such as CS101, AI202, or DS303"
                    },
                    "scholarship_percent": {
                        "type": "number",
                        "description": "Scholarship percentage"
                    }
                },
                "required": [
                    "course_code",
                    "scholarship_percent"
                ]
            }
        }
    }
]


# Connect tool names to Python functions
available_functions = {
    "get_course_fee": get_course_fee,
    "calculate_discounted_fee": calculate_discounted_fee
}


def react_agent(question):

    messages = [
        {
            "role": "system",
            "content": """
You are a ReAct course-fee assistant.

You have access to private course-fee information through tools.

Available courses:
- CS101
- AI202
- DS303

When a question asks for an actual course fee, scholarship-adjusted fee,
or comparison involving course fees, use the appropriate tool.

Do not invent course fees.

You may call tools multiple times when the question requires information
about multiple courses.

After receiving the tool results, provide a concise final answer.
"""
        },
        {
            "role": "user",
            "content": question
        }
    ]


    # ReAct loop
    for step in range(8):

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools,
            tool_choice="auto",
            parallel_tool_calls=False,
            temperature=0
        )

        message = response.choices[0].message


        # Agent wants to use a tool
        if message.tool_calls:

            print(
                "\n[THOUGHT] "
                "The agent needs course information from a tool."
            )

            messages.append(message)

            for tool_call in message.tool_calls:

                function_name = tool_call.function.name

                arguments = json.loads(
                    tool_call.function.arguments
                )

                print(
                    f"[ACTION] {function_name}({arguments})"
                )

                function = available_functions[function_name]

                result = function(**arguments)

                print(
                    f"[OBSERVATION] {result}"
                )

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": function_name,
                        "content": json.dumps(result)
                    }
                )

        else:

            print("\n[FINAL ANSWER]")

            return message.content


    return "The agent could not complete the request."


if __name__ == "__main__":

    print("=== ReAct Course Fee Agent ===")
    print("Type 'exit' to stop.\n")

    while True:

        question = input("You: ")

        if question.lower() == "exit":
            break

        answer = react_agent(question)

        print(answer)
        print()
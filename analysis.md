# Reasoning and Acting: Comparing Direct Prompting, Chain-of-Thought, and ReAct

## 1. Scenario

The scenario selected for this project is a **Course Fee and Scholarship Advisor**.

The system contains course-fee information for three courses:

| Course |     Fee |
| ------ | ------: |
| CS101  | ₹30,000 |
| AI202  | ₹40,000 |
| DS303  | ₹35,000 |

The system can also calculate the final course fee after applying a scholarship percentage.

For example, a user may ask:

> What is the fee for CS101?

This question requires access to the course-fee information stored in the application's private data.

Another type of question requires multi-step reasoning and calculation:

> Which is cheaper: CS101 and AI202 with a 10% scholarship, or all three courses with a 25% scholarship? By how much?

The same scenario was implemented using three approaches:

1. Direct Prompting
2. Chain-of-Thought Prompting
3. ReAct Agent

The purpose of this project is to compare how these approaches handle reasoning, external information, tool usage, multi-step questions, reliability, transparency, speed, cost, and consistency across repeated runs.

---

# 2. Approach Overview

## 2.1 Direct Prompting

Direct prompting sends the user's question directly to the language model and asks it to provide an answer.

The flow is:

```text
User Question
      ↓
Language Model
      ↓
Final Answer
```

The direct-prompting implementation does not use the course-fee tools. It therefore relies only on the model's existing knowledge and the information included in the user's prompt.

For a general question, the model can provide an answer directly. However, when the user asks for a project-specific fact such as the exact fee of CS101, the model does not have access to the application's private course-fee data.

In the experiment, asking the direct chatbot for the CS101 fee demonstrated this limitation. The model could not reliably retrieve the private value stored in the project.

Direct prompting is simple because it requires no tool selection or external data retrieval. However, its lack of external information access limits its reliability for questions that depend on private or application-specific data.

---

## 2.2 Chain-of-Thought Prompting

Chain-of-Thought prompting is designed for questions that require multiple reasoning or calculation steps.

The flow is:

```text
User Question
      ↓
Language Model
      ↓
Internal reasoning
      ↓
Concise explanation
      ↓
Final Answer
```

The Chain-of-Thought implementation asks the model to solve the problem carefully and provide a concise explanation and final answer. It does not use external course-fee tools.

For example, when the course prices are provided directly in the question, the model can calculate the scholarship-adjusted prices and compare the two options.

For Option A:

```text
CS101 + AI202
= ₹30,000 + ₹40,000
= ₹70,000

After 10% scholarship:
₹70,000 × 0.90
= ₹63,000
```

For Option B:

```text
CS101 + AI202 + DS303
= ₹30,000 + ₹40,000 + ₹35,000
= ₹105,000

After 25% scholarship:
₹105,000 × 0.75
= ₹78,750
```

The difference is:

```text
₹78,750 - ₹63,000
= ₹15,750
```

Therefore, Option A is cheaper by ₹15,750.

However, Chain-of-Thought does not solve the external-information problem by itself. If the course fees are not provided in the prompt, the model cannot use the application's private course database because no tool is connected to it.

Thus, Chain-of-Thought improves multi-step reasoning when the required information is available, but it cannot independently retrieve facts from the project's private data.

---

## 2.3 ReAct Agent

The ReAct agent combines reasoning with actions and observations.

The implementation provides the agent with two tools:

* `get_course_fee()`
* `calculate_discounted_fee()`

The overall process is:

```text
User Question
      ↓
Agent decides what information is required
      ↓
Action → Tool
      ↓
Observation ← Tool Result
      ↓
Agent processes the result
      ↓
Another Action if required
      ↓
Observation
      ↓
Final Answer
```

For example, when the user asks:

> What is the fee for CS101?

the agent can identify that it needs the course fee and call:

```text
get_course_fee("CS101")
```

The tool retrieves the private course information:

```text
CS101 = ₹30,000
```

The agent then uses this observation to produce the final answer.

For a question involving multiple courses, the agent can make multiple tool calls. It can retrieve the required course information, observe the returned values, perform the required calculations, and then provide the final answer.

The ReAct approach therefore extends the language model with the ability to interact with external information through tools. The visible action and observation trace also makes the tool-use process easier to inspect.

---

# 3. Analysis

## 3.1 Explanation of Each Approach

Direct Prompting, Chain-of-Thought, and ReAct differ mainly in how they obtain information and solve the user's request.

Direct Prompting answers immediately from the language model. It does not use tools and has no access to the private course-fee database in this project. It can handle general questions and simple requests, but it cannot reliably answer questions that require private application-specific facts. The process is simple: the user provides a question, the language model generates a response, and the response is returned to the user.

Chain-of-Thought adds a stronger reasoning process for questions involving several calculation or logical steps. In this project, it can solve the scholarship comparison when the course prices are supplied in the question. However, it still does not use tools. Therefore, it cannot retrieve the private CS101, AI202, or DS303 fees when those values are not provided in the prompt. Its limitation is that improved reasoning does not automatically provide access to missing external information.

The ReAct agent combines reasoning with tool usage. It can determine that external course information is required, call an appropriate tool, observe the result, and continue processing the task. It can also make multiple tool calls when the question requires information about multiple courses. This makes the approach suitable for questions that combine reasoning with external information access.

---

## 3.2 Comparison Table

| Basis for comparison                    | Direct Prompting                                                              | Chain-of-Thought                                                              | ReAct Agent                                                                                  |
| --------------------------------------- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| **Reasoning depth**                     | Provides a direct answer with limited explicit reasoning                      | Better suited to multi-step reasoning and calculations                        | Combines reasoning with actions and observations                                             |
| **Tool usage**                          | No tool usage                                                                 | No tool usage                                                                 | Uses course-fee tools when required                                                          |
| **Reliability on multi-step questions** | Can handle simple questions but may be less reliable for complex calculations | Better for multi-step calculations when all required information is available | Can handle multi-step tasks involving both calculations and external information             |
| **Transparency**                        | The answer is returned directly with no visible reasoning process             | A concise explanation can be provided, but internal reasoning is not exposed  | Tool actions and observations can be displayed in an execution trace                         |
| **Speed / cost**                        | Generally simple and fast because it requires a direct model response         | May require more reasoning but does not require tool calls                    | Can require multiple model and tool interactions, increasing execution time and cost         |
| **Consistency across repeated runs**    | Can vary when temperature is non-zero                                         | Can vary when temperature is non-zero                                         | Model decisions can vary, although tool results themselves are deterministic in this project |

---

## 3.3 Self-Consistency Observation

A Chain-of-Thought reasoning question was selected for the self-consistency experiment:

> CS101 costs ₹30,000. AI202 costs ₹40,000. DS303 costs ₹35,000. Which is cheaper: CS101 and AI202 with a 10% scholarship, or all three courses with a 25% scholarship? By how much?

The mathematically correct calculation is:

```text
Option A:
CS101 + AI202
= ₹30,000 + ₹40,000
= ₹70,000

After 10% scholarship:
₹70,000 × 0.90
= ₹63,000


Option B:
CS101 + AI202 + DS303
= ₹30,000 + ₹40,000 + ₹35,000
= ₹105,000

After 25% scholarship:
₹105,000 × 0.75
= ₹78,750


Difference:
₹78,750 - ₹63,000
= ₹15,750
```

Therefore, the correct answer is that **Option A is cheaper by ₹15,750**.

The question was run five times using a non-zero temperature of **0.7**.

| Run | Temperature | Result                         | Correct? |
| --- | ----------: | ------------------------------ | -------- |
| 1   |         0.7 | Option A is cheaper by ₹15,750 | Yes      |
| 2   |         0.7 | Option A is cheaper by ₹15,750 | Yes      |
| 3   |         0.7 | Option A is cheaper by ₹15,750 | Yes      |
| 4   |         0.7 | Option A is cheaper by ₹15,750 | Yes      |
| 5   |         0.7 | Option A is cheaper by ₹15,750 | Yes      |

All five runs produced the same underlying answer. Some responses used slightly different wording and formatting, but every run correctly identified Option A as cheaper by ₹15,750.

Therefore, the **majority answer was Option A, cheaper by ₹15,750**, and the majority answer was correct. In this experiment, the majority answer was also the answer produced by all five runs.

The program's expected calculation also confirmed:

```text
Option A = ₹63,000.00
Option B = ₹78,750.00
Option A is cheaper by ₹15,750.00
```

The same question was then run once with **temperature = 0**.

The temperature-0 run also produced:

> Option A is cheaper by ₹15,750.

Therefore, in this particular experiment, both the five non-zero-temperature runs and the temperature-0 run produced the same correct mathematical result.

The experiment shows that even when the final answer remains consistent, the wording and presentation of generated responses can vary. In this particular test, the non-zero temperature did not change the final conclusion. Temperature 0 also produced the same correct result and is intended to provide more deterministic generation.

---

## 3.4 Suitability Analysis

For the Course Fee and Scholarship Advisor scenario, the ReAct approach is suitable because the scenario requires both reasoning and access to external course-fee information.

Direct Prompting is useful for simple questions where the required information is already available to the language model. It is fast and straightforward, but it cannot retrieve the private course fees used by this application.

Chain-of-Thought is appropriate when the main challenge is multi-step reasoning or calculation and all required information is already available in the prompt. In this scenario, it can correctly calculate scholarship-adjusted fees when the course prices are supplied. However, it cannot independently retrieve those prices from the application's private data.

The ReAct agent combines the capabilities required by this scenario. It can use the language model to understand the user's request, call the appropriate course-fee tool, observe the returned information, and continue processing the task. It can also perform multiple tool calls when several courses are involved.

The self-consistency experiment showed that all five non-zero-temperature runs produced the same correct answer for the selected calculation, and the temperature-0 run produced the same result. This indicates that the tested reasoning question was consistent under the particular model and temperature settings used in this experiment. However, consistency can depend on the model, prompt, temperature, and task.

Overall, the ReAct approach fits the scenario because it combines language understanding and reasoning with access to the course-fee tools.

---

## 3.5 Conclusion

Direct Prompting, Chain-of-Thought, and ReAct are useful for different types of problems.

Direct Prompting is appropriate when a user needs a straightforward response and the required information is already available to the language model. It is simple and fast and does not require external tools, making it useful for basic conversational tasks and general questions.

Chain-of-Thought is appropriate when the main challenge is multi-step reasoning or calculation. It can help solve problems that require several logical or mathematical steps when the necessary information is already available in the prompt. However, reasoning alone does not provide access to external databases or application-specific information.

A ReAct agent is appropriate when a problem requires both reasoning and interaction with external information or tools. The agent can determine what information it needs, perform an action using a tool, observe the result, and continue the process until it can provide a final answer. This makes ReAct useful for tasks involving private databases, APIs, calculations, searches, or multiple operations.

The Course Fee and Scholarship Advisor scenario demonstrates these differences clearly. Direct Prompting provides a direct model response, Chain-of-Thought improves multi-step reasoning when the required information is available, and ReAct extends the system by allowing the model to obtain external information through tools and use those results in its final response.
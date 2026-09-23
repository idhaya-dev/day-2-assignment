# Reasoning and Acting: Direct Prompting, Chain-of-Thought, and ReAct

## 1. Scenario

The scenario selected for this project is a **Course Fee and Scholarship Advisor**.

The system contains course-fee information for three courses:

| Course | Fee |
|---|---:|
| CS101 | ₹30,000 |
| AI202 | ₹40,000 |
| DS303 | ₹35,000 |

The system can also calculate the final fee after applying a scholarship percentage.

For example, a user may ask:

> What is the fee for CS101?

This question requires access to the course-fee information.

A second type of question requires reasoning and calculation:

> Which is cheaper: CS101 and AI202 with a 10% scholarship, or all three courses with a 25% scholarship? By how much?

The same scenario was implemented using three approaches:

1. Direct Prompting
2. Chain-of-Thought Prompting
3. ReAct Agent

The purpose is to compare how these approaches handle reasoning, external information, tools, multi-step questions, reliability, transparency, speed, cost, and consistency.

---

# 2. Explanation of Each Approach

## 2.1 Direct Prompting

Direct prompting sends the user's question directly to the language model and asks it to provide an answer.

The flow is:

```text
User Question
      ↓
Language Model
      ↓
Final Answer
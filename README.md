# Reasoning and Acting: Direct Prompting, Chain-of-Thought, and ReAct

## Project Overview

This project compares three approaches for solving a course fee and scholarship problem:

1. Direct Prompting
2. Chain-of-Thought Prompting
3. ReAct Agent

The same scenario is used to study how these approaches differ in reasoning depth, tool usage, reliability, transparency, speed, cost, and consistency.

---

## Scenario

The project uses a Course Fee and Scholarship Advisor scenario.

The course-fee data used by the project is:

| Course | Fee |
|---|---:|
| CS101 | ₹30,000 |
| AI202 | ₹40,000 |
| DS303 | ₹35,000 |

The system can also calculate scholarship-adjusted course fees.

Example question:

> What is the fee for CS101?

Example reasoning question:

> Which is cheaper: CS101 and AI202 with a 10% scholarship, or all three courses with a 25% scholarship? By how much?

---

## Approaches

### 1. Direct Prompting

The question is sent directly to the language model.

```text
User Question
      ↓
Language Model
      ↓
Final Answer
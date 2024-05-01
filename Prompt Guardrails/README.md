# Introduction
There are instances where we want to give an LLM guardrails for what it should
not talk about and to keep it on point. Some examples are: 

* Politics: Do not mention politics or respond to political questions.
* Purpose: Only respond to queries which are true to purpose.
* Toxic Language: Do not repeat toxic language

Purpose:
Often when you are building a RAG solution, you want to scope responses and achieve a certain tone for interactions. Vectara customers who are on the Scale Plan can do this by using the “promptText” in combination with the GPT4 based summarizer (vectara-summary-ext-v1.3.0).

Methodology:
We will now outline the general methodology to use this approach in a structured way:
Identify what topics are in scope for the summarization
Identify the style you want to achieve
Identify how you will evaluate the responses:
Scoring with a person (e.g. a Test Manager or Stakeholder)
An LLM, such as GPT4.
Create a list of test questions, ensuring to create expected and out of scope questions.
Run a prompt engineering dev-test loop:
Build Your Custom Prompt
Run your test harness
Evaluate
This methodology can also be re-used to ensure updated content is being referenced in responses.

Detailed Example
<<

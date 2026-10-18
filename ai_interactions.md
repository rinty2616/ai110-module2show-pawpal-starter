# AI Collaboration Notes

This project was prepared with ChatGPT assistance. **Before submission, replace sample prompts with your own actual prompts and observations.**

| Project stage | Example prompt to ask an AI assistant | What to review yourself |
|---|---|---|
| System design | "Create a simple UML diagram with Owner, Pet, Task, and Scheduler classes." | Do relationships show one owner with multiple pets? |
| Implementation | "How can Scheduler get all tasks from Owner instead of one Pet?" | Does `Owner.get_all_tasks()` really include every pet? |
| Algorithms | "How can Python detect overlapping timed tasks and generate daily repeats?" | Are durations and date increments correct? |
| Testing | "Create pytest cases for sorting, multi-pet tasks, recurrence, and conflicts." | Are the tests meaningful and passing? |
| Refactoring | "Can this scheduling method be clearer without adding complexity?" | Does the simplified code still meet requirements? |

## Example context engineering practice

Provide an AI coding assistant with the relevant source file, expected behavior, and a failing test or CLI output. Ask for the smallest change that fixes the issue. Verify the suggestion locally instead of assuming that generated code is correct.

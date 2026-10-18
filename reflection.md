# 🐾 PawPal+ Project Reflection

## 1. System Design

### a. Initial Design

The three main actions I wanted users to perform in PawPal+ were:

1. Add and manage pets.
2. Schedule care activities such as feeding, walking, and medication.
3. View and organize daily tasks.

The application uses four main Python classes: `Owner`, `Pet`, `Task`, and `Scheduler`.

The `Owner` class manages multiple pets and their information. The `Pet` class stores pet details and their scheduled activities. The `Task` class stores information about each activity, including its date, time, duration, priority, frequency, and completion status.

The `Scheduler` class organizes tasks, detects scheduling conflicts, manages recurring activities, and creates daily plans. It retrieves tasks from all pets through the `Owner.get_all_tasks()` method.

Separating these classes makes the application easier to understand, maintain, and improve.

### b. Design Changes

The initial design focused on managing pets, adding tasks, and displaying schedules.

As the project developed, the application included additional features such as task duration, priority levels, daily and weekly recurrence, scheduling conflicts, and owner time preferences.

These improvements make the application more useful because pet owners need to manage multiple activities within their available time.

I also learned how the Streamlit interface communicates with the Python backend and how `st.session_state` keeps information available during the browser session.

## 2. Scheduling Logic and Tradeoffs

### a. Constraints and Priorities

The PawPal+ scheduler organizes tasks using several important factors:

- **Task time:** Each activity has a scheduled date and start time.
- **Task duration:** Each activity requires a specific number of minutes.
- **Priority:** Tasks are classified as high, medium, or low priority.
- **Daily time budget:** The scheduler considers how much time the owner has available.
- **Owner preferences:** The scheduler considers the owner's preferred time of day.

High-priority activities are considered before medium- and low-priority activities.

When tasks have the same priority, the scheduler considers the owner's preferred time of day and scheduled start times.

If two activities overlap or a task exceeds the available time budget, the scheduler can skip a task and explain why.

This helps the owner understand which activities can fit into the daily plan.

### b. Tradeoffs

One important design tradeoff is using a simple, priority-first scheduling algorithm instead of a complicated optimization system.

The scheduler uses a greedy approach. This means it considers tasks according to priority and accepts tasks that fit the available time without conflicting with already selected activities.

This approach is easier to understand, test, and maintain.

However, the scheduler does not automatically move activities to different times. Sometimes it may skip a task even when rearranging the schedule could allow more tasks to be completed.

Another limitation is that conflict detection works within a scheduled date and does not fully handle activities that cross midnight.

I believe this approach is appropriate for an introductory Python project because it demonstrates useful algorithms while keeping the code understandable.

## 3. AI Collaboration

### a. How I Used AI

I used ChatGPT as my AI coding assistant throughout the PawPal+ project.

ChatGPT helped me understand the assignment instructions, prepare the Python backend, work with the Streamlit interface, understand UML diagrams, and review the testing process.

At the beginning, I needed guidance setting up the project on my MacBook.

ChatGPT explained how to open the project in VS Code, create a Python virtual environment, activate it, and install the required packages.

I also used ChatGPT to understand the four main Python classes and how they work together.

Two examples of questions I asked ChatGPT were:

1. "Give me step by step from the beginning."
2. "I opened uml_final.mmd but do not understand the code. Explain it simply."

These explanations helped me understand the project structure and visualize the relationships between `Owner`, `Pet`, `Task`, and `Scheduler`.

I used the same ChatGPT conversation for help with the different phases. This made it easier to follow my progress and return to earlier instructions. I also learned that separate conversations could be useful for organizing larger projects into design, implementation, and testing tasks.

The most helpful AI features were step-by-step explanations, troubleshooting assistance, code examples, and explanations of unfamiliar programming concepts.

### b. Judgment and Verification

I learned that AI-generated code and instructions should always be reviewed and tested rather than accepted without checking.

For example, while using my application, ChatGPT initially referred to a field as "Task title." However, the actual application used the label "Task description." I checked the interface and followed the corrected instruction.

This showed me that AI suggestions sometimes need to be adjusted to match the actual application.

I also encountered Streamlit warnings about the older `use_container_width` setting. ChatGPT explained that the newer `width="stretch"` setting should be used instead.

I tested the application manually by adding Bella as a pet and creating care activities.

I scheduled two activities for Bella at 08:00: Breakfast and Morning Feeding. The application detected that these tasks overlapped.

When I generated the smart daily plan, the scheduler selected Breakfast and skipped Morning Feeding because the activities conflicted.

I also tested recurring tasks. After completing Bella's daily Morning walk on October 18, 2026, the application generated the next occurrence for October 19, 2026.

Finally, I ran the automated testing suite using:

`python -m pytest`

All 14 tests passed successfully.

These experiences taught me that AI is helpful for understanding and creating software, but human review and verification are essential.

## 4. Testing and Verification

### a. What I Tested

I tested PawPal+ through the command-line interface, Streamlit web application, and automated Python tests.

**Command-Line Testing**

I ran `python main.py` in the VS Code terminal.

The program successfully displayed scheduled activities for Bella and Luna, detected a time conflict, generated a daily plan, and demonstrated recurring task functionality.

**Streamlit Application Testing**

I opened the application in Chrome using `streamlit run app.py`.

I tested adding pets, creating activities, marking tasks as completed, and generating daily schedules.

I also tested scheduling conflicts by creating two activities at the same time.

**Automated Testing**

I ran `python -m pytest` on my MacBook.

The results were:

```text
collected 14 items

tests/test_pawpal.py .............. [100%]

14 passed in 0.02s
```

The automated tests cover task creation and completion, adding tasks, managing multiple pets, sorting, filtering, recurring activities, conflict detection, priority handling, daily time budgets, and invalid inputs.

These tests are important because they help verify that the application's core logic behaves as expected.

### b. Confidence Level

**Confidence Level: ★★★★☆ (4/5)**

I rate the PawPal+ backend four out of five stars because all 14 automated tests passed, and the main application features worked during manual testing.

I successfully verified pet management, task scheduling, conflict detection, recurring tasks, and daily planning.

However, there is still room for improvement.

The application stores data in the current browser session rather than a permanent database. This means information can be lost when the session ends.

Additional testing would also help verify more complex scheduling situations, including overnight tasks and interactions between different features.

Overall, I am confident that the application demonstrates the required Python object-oriented programming and scheduling concepts.

## 5. Reflection

### a. What Went Well

One of the most successful parts of this project was learning how the different Python classes work together.

Separating the `Owner`, `Pet`, `Task`, and `Scheduler` classes made the project easier to understand.

The CLI-first workflow was also helpful because I could run `main.py` and verify the scheduling logic before testing the web application.

Another important success was learning how to use the VS Code terminal.

I learned how to create and activate a virtual environment, install Python packages, run Python programs, and execute automated tests.

Using the Mermaid Live Editor helped me understand the UML diagram and visualize the structure of the application.

Seeing the Streamlit application work in Chrome helped connect the Python code to a real user interface.

### b. What I Would Improve

If I had more time, I would improve PawPal+ in several ways.

First, I would add a database so pet owners could save their information permanently.

Second, I would improve the scheduling algorithm so it could suggest alternative times when two activities conflict.

Third, I would add more flexible recurring task options, such as activities that repeat every few days or on selected weekdays.

I would also improve the application's visual design and add more automated tests for user interactions.

These improvements would make PawPal+ more practical for real pet owners.

### c. Key Takeaway

The most important lesson I learned is that building a software application requires more than writing code.

It involves understanding requirements, designing a system, choosing algorithms, testing functionality, and improving the results.

I also learned that AI can be a valuable coding assistant, especially when learning unfamiliar programming concepts.

However, AI-generated suggestions still need to be reviewed, understood, and verified.

As the person responsible for the project, I need to understand how the system works and make decisions about its design and functionality.

Completing PawPal+ helped me gain practical experience with Python, object-oriented programming, UML diagrams, Streamlit, scheduling algorithms, and automated testing.

This project also helped me become more comfortable using VS Code and working through technical problems step by step.
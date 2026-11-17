# Student Allowance Allocation

This project explores how students can allocate a fixed allowance in Nigerian naira (NGN) across essentials, emergency reserves, savings, and discretionary spending. The first release will pair a Python command-line program with a documented allocation model and an academic paper draft.

## Current status

`allocation.py` is the original prototype. It sketches an airtime flow with a ₦300 cap and a ₦30,000 income threshold. It has no entry point, refers to a deadline before assigning it, and tries to compare an empty string with a number. Its balance update uses equality comparison, so the balance would stay the same. The success message represents a simulated purchase. The allocation rules are still to be defined.

## Version 1 scope

| Deliverable | Completion criteria |
| --- | --- |
| Python program | Accept a budget and budget period, produce an NGN allocation, and handle invalid inputs and shortfalls. Simulate any spending recorded through the program. |
| Allocation model | Document inputs, category priorities, rounding, and shortfall rules. Account for the full budget and explain each recommendation. |
| Evaluation | Compare the proposed rules with a simple fixed-percentage baseline using documented synthetic scenarios. Measure essential expenses covered, reserve targets met, and budget violations. Record assumptions and limitations. |
| Academic paper draft | Describe the research question, related work, model, evaluation, results, and limitations. Include instructions to reproduce results from a tagged version. |

Starter research question: How does a priority-based allocation rule compare with a fixed-percentage split on essential-expense coverage and emergency-reserve funding across different student budgets?

## Progress log

| Date | Progress | Next step |
| --- | --- | --- |
| 2026-11-17 | Copied the original prototype into the project and documented its current behavior and proposed scope. | Define the budget period, category priorities, and what the model should do when the allowance cannot cover essentials. |

## GitHub workflow

Commit the original prototype and README together as the project baseline. Track the program, model, evaluation, and paper as GitHub issues. Commit each completed change with a message that describes the outcome. Update this log at milestones with what changed, how it was checked, and any assumptions that affect later work. Tag releases so the paper can reference the exact version used for its results.

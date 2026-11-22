# Student Allowance Allocation

This project explores how students can make a limited allowance last until their next payment. Development starts with a Python budgeting model in Nigerian naira (NGN), supported by an academic paper draft. The intended Student Mode feature will account for essential expenses, reserves, and changes during an allowance period.

## Current status

`allowance_allocation_jupyter_notebook.ipynb` is the active prototype. It accepts an allowance, a positive whole-number period in days, and amounts to protect for internet, transport, and emergencies. It subtracts those commitments and divides the remaining balance across the period.

Money calculations use Python's `Decimal`. The input loop rejects negative or nonfinite money values, invalid numeric text, and zero, negative, or fractional days. When commitments exceed the allowance, it reports the shortfall and prompts for another attempt. A fully committed allowance produces a daily budget of zero.

`allocation.py` preserves the original airtime-flow prototype and has unresolved execution and balance-update issues. The Word document contains the developing academic paper. The notebook currently collects inputs inside its functions, and its printed daily budget is rounded to two decimal places. A rule for distributing rounding remainders across days is pending.

## Run the prototype

Open `allowance_allocation_jupyter_notebook.ipynb` in Jupyter or VS Code with the Python and Jupyter extensions. Select a Python kernel, run the active function-definition cell, and answer the input prompts. Earlier worked examples are currently commented out. The active code uses Python's standard library.

For an allowance of ₦80,000 over 31 days, with ₦5,000 for internet, ₦10,000 for transport, and a ₦5,000 emergency reserve, the prototype protects ₦20,000 and calculates a daily budget of ₦1,935.48 from the remaining ₦60,000.

## Verification

On 22 November 2026, eight scripted checks executed the saved notebook code in fresh namespaces with simulated input. They covered a funded budget, a fully committed allowance, invalid money text, zero days, fractional days, a shortfall followed by a valid attempt, a nonfinite allowance, and a negative commitment. All eight passed. These checks verified the input and calculation flow. Evaluation of student outcomes remains pending.

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
| 2026-11-20 | Added the initial daily-budget notebook and academic paper draft to GitHub. | Develop the commitment allocation logic. |
| 2026-11-22 | Verified and pushed commitment calculations and input retry handling in commit `401a414`. All eight scripted checks passed. | Pass explicit inputs into the calculation functions and separate interactive prompts from calculations. |

## Planned development

Next, the calculation functions will accept explicit inputs so experiments and a future GUI can reuse them. Later stages will address spending updates, debt repayment deadlines, delayed allowances, savings goals, and evaluation against a baseline. A database, authentication, and a web interface are planned for a usable prototype. AI-assisted prediction is a later research direction.

## GitHub workflow

Track the program, model, evaluation, and paper as GitHub issues. Commit each completed change with a message that describes the outcome. Update this log at milestones with what changed, how it was checked, and any assumptions that affect later work. Tag releases so the paper can reference the exact version used for its results.

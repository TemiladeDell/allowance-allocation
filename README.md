# Student Allowance Allocation

This project explores how students can make a limited allowance last until their next payment. Development starts with a Python budgeting model in Nigerian naira (NGN), supported by an academic paper draft. The intended Student Mode feature will account for essential expenses, reserves, and changes during an allowance period.

## Current status

`allowance_allocation_jupyter_notebook.ipynb` is the active prototype. It accepts an allowance, a positive whole-number period in days, and amounts to protect for internet, transport, and emergencies. It subtracts those commitments and divides the remaining balance across the period.

Money calculations use Python's `Decimal`. The input loop rejects negative or nonfinite money values, invalid numeric text, and zero, negative, or fractional days. When commitments exceed the allowance, it reports the shortfall and prompts for another attempt. A fully committed allowance produces a daily budget of zero.

The notebook separates input collection, commitment calculations, and daily-budget calculations into three functions.

| Function | Responsibility |
| --- | --- |
| `users_decision()` | Collect the allowance, period, and commitment amounts from the user. |
| `commitment_function(total_allowance, internet, transportation, emergency)` | Validate money values and return the available balance followed by the protected total. |
| `allocation_function(balance, days)` | Check for a negative balance or nonpositive days, then return the balance divided by days. |

The final calling cell connects these functions inside a retry loop. An invalid attempt displays an error and repeats the prompts. The two calculation functions can also be called directly with supplied values.

`allocation.py` preserves the original airtime-flow prototype and has unresolved execution and balance-update issues. The Word document contains the developing academic paper. Printed daily budgets are rounded to two decimal places. A rule for distributing rounding remainders across days is pending. Whole-number days and finite money values are validated through the interactive flow; the standalone daily-budget function currently checks only negative balances and nonpositive days.

## Run the prototype

Open `allowance_allocation_jupyter_notebook.ipynb` in Jupyter or VS Code with the Python and Jupyter extensions. Select a Python kernel, run the active cells containing imports and function definitions in order, then run the final retry-loop cell and answer its prompts. Restarting the kernel clears earlier definitions, so rerun the definition cells before using the functions again. Earlier worked examples are currently commented out. The active code uses Python's standard library.

For an allowance of ₦80,000 over 31 days, with ₦5,000 for internet, ₦10,000 for transport, and a ₦5,000 emergency reserve, the prototype protects ₦20,000 and calculates a daily budget of ₦1,935.48 from the remaining ₦60,000.

## Verification

On 23 November 2026, eight scripted checks executed the refactored notebook code in fresh namespaces with simulated input. They covered a funded budget, a fully committed allowance, invalid money text, zero days, fractional days, a shortfall followed by a valid attempt, a nonfinite allowance, and a negative commitment. All eight passed. The checks were run during development and are not yet stored as a test suite in the repository. They verified the input and calculation flow. Evaluation of student outcomes remains pending.

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
| 2026-11-23 | Separated input collection from both calculation functions and restored the outer retry loop in commit `fbc5cf5`. All eight scripted checks passed after the refactor. | Build a spending-update function and recalculate the daily budget after a day of spending. |

## Planned development

Next, a spending-update function will accept an available balance, a day's spending, and the remaining period. It will calculate the updated balance and days for a revised daily budget. Validation will need to cover overspending and the final day of the period. Later stages will address debt repayment deadlines, delayed allowances, savings goals, and evaluation against a baseline. A database, authentication, and a web interface are planned for a usable prototype. AI-assisted prediction is a later research direction.

## GitHub workflow

Track the program, model, evaluation, and paper as GitHub issues. Commit each completed change with a message that describes the outcome. Update this log at milestones with what changed, how it was checked, and any assumptions that affect later work. Tag releases so the paper can reference the exact version used for its results.

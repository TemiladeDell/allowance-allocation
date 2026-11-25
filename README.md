# Student Allowance Allocation

This project explores how students can make a limited allowance last until their next payment. Development starts with a Python budgeting model in Nigerian naira (NGN), supported by an academic paper draft. The intended Student Mode feature will account for essential expenses, reserves, and changes during an allowance period.

## Current status

`allocation.py` is the runnable Python prototype. On 24 November 2026, the active budgeting and spending logic developed in `allowance_allocation_jupyter_notebook.ipynb` was moved into this file. The notebook remains the testing ground for experiments and model development. The original airtime-flow code is preserved in Git history.

The notebook and Python script both include savings modes and day advancement. Non-reluctant savings now deducts automatically when a day's feeding allowance is released, including the first day. The student selects a rate during setup; the saved rate applies to later releases.

The program accepts an allowance, a positive whole-number period in days, and amounts to protect for internet, transport, and emergencies. It subtracts those commitments and treats the remaining balance as feeding funds. It includes category purchases, repeated-purchase limits, savings, day advancement, and JSON saving and loading.

Money calculations use Python's `Decimal`. The input loop rejects negative or nonfinite money values, invalid numeric text, and zero, negative, or fractional days. When commitments exceed the allowance, it reports the shortfall and prompts for another attempt. A fully committed allowance produces a daily budget of zero.

The Python file contains the core calculations and interactive entry point, together with the menu and persistence functions listed below.

| Function | Responsibility |
| --- | --- |
| `users_decision()` | Collect the allowance, period, and commitment amounts from the user. |
| `commitment_function(total_allowance, internet, transportation, emergency)` | Validate money values and return the available balance followed by the protected total. |
| `allocation_function(balance, days)` | Check for a negative balance or nonpositive days, then return the balance divided by days. |
| `allowance_allocation()` | Start the saved-budget menu when running the script. |

An invalid budget setup repeats the setup prompts. An invalid spending request returns to the session menu. The calculation functions accept supplied values for reuse in experiments. The script starts through an `if __name__ == "__main__"` guard, so importing it defines the functions without prompting for input.

The Word document contains the developing academic paper. A rule for distributing rounding remainders across days is pending. Whole-number days and finite money values are validated through the interactive flow; the standalone daily-budget function currently checks only negative balances and nonpositive days.

## Category purchases and persistence

The category purchase menu and local JSON saving developed in the notebook are now also available in `allocation.py`. The notebook remains the testing ground for further model development.

| Function | Responsibility |
| --- | --- |
| `spending_function(category_balances, daily_limits, budget_state=None)` | Validate a simulated purchase and update the selected category and its remaining daily availability. |
| `user_menu(category_balances=None, daily_limits=None, budget_state=None)` | Set up or resume a budget, process daily savings, and offer balance, purchase, and plan-change actions. |
| `save_balances(category_balances, daily_limits, file_path, budget_state=None)` | Save balances, daily availability, rates, and budget state as JSON. |
| `load_balances(file_path, budget_state=None)` | Validate and restore balances and optional budget state, including saved rates. |
| `saved_budget_menu(file_path)` | Start or resume a budget, then save the results when the session menu exits. |

Each purchase reduces only its selected category and today's availability for that category. Emergency funds remain reserved. Invalid requests and cancelled purchases preserve balances. Reopening today's save preserves the remaining daily limits, preventing a restart from granting another full daily allowance.

Daily availability for feeding, internet, and transport is calculated from each category's allocation and the budget period, rounded down to the nearest kobo. Purchase amounts must be positive, finite, within the remaining limit, and have at most two decimal places. Purchases are recorded as local simulations.

Saving currently happens when the budget menu exits. A new budget replaces the existing single-user save after that session. Both versions use Nigeria calendar dates and process elapsed budget days. Automatic saving after each purchase, transaction history, and multi-user support remain pending. Daily releases are processed when the program runs or resumes; the local prototype has no background service.

## Savings and day advancement

Each account has one active savings mode and one accumulated savings balance.

| Mode | Rule |
| --- | --- |
| Reluctant Saver | Move unused feeding availability into savings when the day closes. The next day receives its usual allowance, subject to available funds and final-day rounding. |
| Non-reluctant Saver | Automatically deduct the selected rate at each daily feeding release before spending. Small saves 10%, Medium saves 20%, and Hardcore saves 30% of the original daily feeding allowance. Unused feeding availability carries forward. |

For an original daily feeding allowance of ₦4,000, automatic savings is ₦400, ₦800, or ₦1,200, leaving ₦3,600, ₦3,200, or ₦2,800 from the new daily allowance available for feeding. Carryover does not change the percentage base. Deductions are rounded down to kobo. Each transfer reduces feeding funds and daily availability, then increases savings by the same amount. A processed-date record prevents another deduction on the same day, including after reopening. A zero daily feeding allowance produces a zero deduction.

Mode and rate changes take effect the following day. The old day closes under its existing mode, then the next day's mode and rate are activated before its automatic savings deduction. Internet availability carries forward; transport currently follows the same carryover rule. Daily releases increase availability within existing category balances. Day advancement handles elapsed days, prevents repeated closing, and ends releases when the allowance period finishes. The final day makes category rounding remainders available; the savings percentage base remains the original daily allowance.

| Function | Responsibility |
| --- | --- |
| `budget_today()` | Return today's Nigeria calendar date using UTC+1. |
| `choose_savings_mode()` | Select the active savings method during setup. |
| `choose_savings_rate()` | Select Small 10%, Medium 20%, or Hardcore 30% for automatic daily deductions. |
| `schedule_savings_mode(budget_state, new_mode, today=None, new_rate=None)` | Record a mode or rate change for the following day. |
| `savings_allocation(category_balances, daily_limits, budget_state, today=None)` | Apply the day's automatic non-reluctant deduction once, using the saved rate without prompting for a contribution. |
| `advance_budget_day(category_balances, daily_limits, budget_state, today=None)` | Process day closing, carryover, mode changes, and remaining days. |

The menu passes `budget_state` explicitly alongside balances and limits. JSON saves include `finances.savings`, original daily allowances, `savings_rate`, `pending_savings_rate`, active and pending modes, remaining days, and `last_savings_date`/`last_closed_date`. Rates are saved as decimal strings.

Earlier manual-savings saves with budget metadata are migrated without an extra deduction for their already-open day. On resume, the student selects a rate for future daily releases, including any scheduled switch into non-reluctant mode. Earlier files with no budget metadata still have readable balances, but lack the original daily amounts needed for savings; keep a backup before replacing such a save.

## Run the prototype

From the project folder, run the program with Python 3.

```sh
python allocation.py
```

The script requires Python 3.10 or later for `match` cases and uses only the standard library. Choose a new budget or resume today's save, then use the menu to view balances or record category purchases. Exit the session menu to save to `saved_balance.json` in the current working directory.

For notebook experiments, use the following workflow.

Open `allowance_allocation_jupyter_notebook.ipynb` in Jupyter or VS Code with the Python and Jupyter extensions. Select a Python kernel and run the import and function-definition cells in order. The standalone `print(user_menu())` cell is an interactive experiment without JSON saving. For a saved session, run the following command in a new cell.

```python
saved_budget_menu()
```

Choose a new budget or resume a saved budget. During setup, select a savings mode and, for non-reluctant mode, an automatic rate. The session menu displays balances and daily availability, records simulated purchases, schedules mode or rate changes, and exits to save. Automatic savings is processed before purchases are allowed. Resuming processes elapsed days. The default save is `saved_balance.json` in the kernel's working directory. An alternative path can be supplied as `saved_budget_menu("my_budget.json")`.

Restarting the kernel clears definitions, so rerun the definition cells before starting another session. Earlier worked examples are currently commented out. The active code uses Python's standard library.

For an allowance of ₦80,000 over 31 days, with ₦5,000 for internet, ₦10,000 for transport, and a ₦5,000 emergency reserve, the prototype protects ₦20,000 and calculates a daily budget of ₦1,935.48 from the remaining ₦60,000.

## Verification

On 25 November 2026, all 56 checks passed for the automatic-savings correction across both notebook and script. The 34 savings and integration checks covered function parity, import safety, all three first-day rates, duplicate prevention, daily deductions excluding carryover, reluctant leftovers, switches in both directions, next-day rate changes, missed days, period end, zero feeding allowances, invalid rates, insufficient funds, complete menus, save/resume, next-day resume, and migration of earlier manual-savings saves. Another 22 checks covered purchase validation, cancellation, category-specific debits, missing/corrupt saves, full notebook execution, and the script entry point.

On 25 November 2026, all 23 checks passed against the saved notebook executed in a fresh namespace. They covered all three voluntary rates, duplicate contributions, cancellation and invalid choices, insufficient funds, the original daily percentage base, reluctant day closing, carryover, scheduled mode changes, missed days, final-day handling, backward dates, invalid purchases, complete menu sessions, save/resume, next-day resumption, missing and corrupt files, and legacy balances. Simulated inputs, explicit dates, and temporary files were used. The personal balance-guide Markdown cell was removed before testing and publishing.

The earlier Python migration was checked against its matching notebook milestone using simulated new-budget and resumed-budget sessions. The checks compared prompts, outputs, and saved balances, including a rejected repeat purchase. Additional checks covered import behavior and invalid save files.

On 24 November 2026, eleven purchase and menu checks passed for the new notebook flow. They covered category-specific deductions, repeated overspending, invalid choices and amounts, cancellation, zero availability, and a complete menu session. Seven additional persistence checks passed, covering exact decimal round trips, resumed purchases, retained daily limits, new saves, missing files, corrupt files, and rejection of previous-day saves. Temporary files were used for these checks.

Earlier on 24 November 2026, five scenarios compared the script's prompts and outputs with the notebook logic at the migration milestone. They covered a valid purchase, spending retries, setup retries, a shortfall retry, and a fully committed allowance with zero spending. All five matched, allowing for a spelling correction in the shortfall message. A separate check confirmed that importing the script does not prompt for input.

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
| 2026-11-24 | Added validated feeding expenses, separate spending retries, and remaining-balance calculations in the notebook. Moved the active logic into an organized, runnable `allocation.py` with an import-safe entry point. Five comparison scenarios and an import check passed. | Represent category balances together, then add a menu and persistence. |
| 2026-11-24 | Added notebook category purchases, repeated-purchase limits, balance menus, and same-day JSON saving and loading in commit `70e3d6b`. Eleven purchase/menu checks and seven persistence checks passed. | Define day advancement and carryover, then migrate the verified notebook additions into the Python program. |
| 2026-11-24 | Migrated the notebook's category purchase and persistence functions into `allocation.py`, retaining the simple loops and match cases. | Define day advancement and carryover. |
| 2026-11-25 | Added notebook savings modes, once-per-day voluntary contributions, carryover, scheduled mode changes, day advancement, and persistent savings state. Removed the personal Markdown guide and pushed commit `66fe44d` after all 23 checks passed. | Migrate and verify the savings milestone in the Python program. |
| 2026-11-25 | Corrected non-reluctant savings to deduct automatically at each daily release, including setup. Stored rates and processing dates, removed the manual contribution action, and synchronized the notebook and Python program. | Continue testing complete allowance periods before the demonstration interface. |

## Planned development

Next, continue testing complete allowance periods and clarify the remaining product rules. Later stages will address transaction history, debt repayment deadlines, delayed allowances, and evaluation against a baseline. A database and a simulated web interface are planned to demonstrate Student Mode as a potential feature for an established financial platform. AI-assisted prediction is a later research direction. Functions remain together while these responsibilities develop.

## GitHub workflow

Track the program, model, evaluation, and paper as GitHub issues. Commit each completed change with a message that describes the outcome. Update this log at milestones with what changed, how it was checked, and any assumptions that affect later work. Tag releases so the paper can reference the exact version used for its results.

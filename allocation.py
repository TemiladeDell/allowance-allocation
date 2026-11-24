"""Student allowance budgeting with category purchases and local JSON storage.

Run python allocation.py to start a new budget or resume today's saved budget.
"""

import json
from datetime import date
from decimal import Decimal, InvalidOperation, ROUND_DOWN
from pathlib import Path


def users_decision():
    total_allowance_allocated = Decimal(input("Enter your total amount allowance: "))

    days = int(input("Enter period of usage for this amount: "))

    if days <= 0:
        raise ValueError("Enter a positive number")

    internet_allowance = Decimal(input("Enter amount for Airtime/Data: "))
    transportation_allowance = Decimal(input("Enter amount for Transportation: "))
    emergency_reserve_allowance = Decimal(input("Enter amount for Emergency reserve: "))

    return total_allowance_allocated, internet_allowance, transportation_allowance, emergency_reserve_allowance, days


def commitment_function(total_allowance, internet, transportation, emergency):
    total_allowance_received = Decimal(total_allowance)
    if not total_allowance_received.is_finite():
        raise ValueError("Enter a finite number")
    if total_allowance_received < 0:
        raise ValueError("Enter a non-negative number")

    internet_allocation = Decimal(internet)
    transportation_allocation = Decimal(transportation)
    emergency_reserve_allocation = Decimal(emergency)

    if not internet_allocation.is_finite() or not transportation_allocation.is_finite() or not emergency_reserve_allocation.is_finite():
        raise ValueError("Enter a finite number")

    if internet_allocation < 0 or transportation_allocation < 0 or emergency_reserve_allocation < 0:
        raise ValueError("Enter non-negative numbers")


    protected_allowance_commitment = internet_allocation + transportation_allocation + emergency_reserve_allocation
    if protected_allowance_commitment > total_allowance_received:
        raise ValueError(f"Commitemnts greater than available balance. You are {protected_allowance_commitment - total_allowance_received} short")
    non_protected_allowance = total_allowance_received - protected_allowance_commitment

    return non_protected_allowance , protected_allowance_commitment


def allocation_function(balance, days):
    if balance < 0:
        raise ValueError("Balance cannot be negative")
    if days <= 0:
        raise ValueError("Days must be greater than zero")
    feeding_balance = balance / days
    return feeding_balance


def spending_function(category_balances, daily_limits):
    choice = input(
        "What kind of purchase do you want to make?\n"
        "1. Airtime/Data\n2. Transportation\n3. Feeding\n4. Cancel\n"
    ).strip()

    match choice:
        case "1":
            category = "internet"
        case "2":
            category = "transport"
        case "3":
            category = "feeding"
        case "4":
            return None
        case _:
            raise ValueError("Choose 1, 2, 3, or 4.")

    category_balance = category_balances[category]
    daily_remaining = daily_limits[category]
    if not category_balance.is_finite() or category_balance < 0:
        raise ValueError("Category balance must be finite and non-negative.")
    if not daily_remaining.is_finite() or daily_remaining < 0:
        raise ValueError("Daily limit must be finite and non-negative.")

    maximum_purchase = min(category_balance, daily_remaining)
    if maximum_purchase == 0:
        raise ValueError("No funds are available for this category today.")

    print(f"Available for {category} today: NGN {maximum_purchase:,.2f}")
    amount = Decimal(input("Enter the purchase amount in NGN: "))
    if not amount.is_finite():
        raise ValueError("Enter a finite purchase amount.")
    if amount <= 0:
        raise ValueError("Purchase amount must be greater than zero.")
    if amount > maximum_purchase:
        raise ValueError("Purchase exceeds this category's available daily amount.")
    if amount != amount.quantize(Decimal("0.01")):
        raise ValueError("Enter an amount with at most two decimal places.")

    # Calculate both results before updating either balance.
    remaining_category_balance = category_balance - amount
    remaining_daily_limit = daily_remaining - amount
    category_balances[category] = remaining_category_balance
    daily_limits[category] = remaining_daily_limit

    return {
        "category": category,
        "amount": amount,
        "remaining_category_balance": remaining_category_balance,
        "remaining_daily_limit": remaining_daily_limit,
    }


def user_menu(category_balances=None, daily_limits=None):
    if (category_balances is None) != (daily_limits is None):
        raise ValueError("Supply both category balances and daily limits.")

    while category_balances is None:
        try:
            allowance, internet, transport, emergency, days = users_decision()
            balance, expenditure_balance = commitment_function(
                allowance, internet, transport, emergency
            )
            category_balances = {
                "feeding": balance,
                "internet": internet,
                "transport": transport,
                "emergency": emergency,
            }
            daily_limits = {}
            for category in ("feeding", "internet", "transport"):
                daily_limits[category] = allocation_function(
                    category_balances[category], days
                ).quantize(Decimal("0.01"), rounding=ROUND_DOWN)
            break
        except (ValueError, InvalidOperation) as error:
            print(error)

    while True:
        choice = input(
            "\nWhat would you like to do?\n"
            "1. View remaining balances\n2. View daily availability\n"
            "3. Make a simulated purchase\n4. Exit\n"
        ).strip()
        match choice:
            case "1":
                for category, amount in category_balances.items():
                    print(f"{category.capitalize()} balance: NGN {amount:,.2f}")
                print(f"Total remaining: NGN {sum(category_balances.values()):,.2f}")
            case "2":
                for category, amount in daily_limits.items():
                    print(f"{category.capitalize()} available today: NGN {amount:,.2f}")
            case "3":
                try:
                    transaction = spending_function(category_balances, daily_limits)
                    if transaction is None:
                        print("Purchase cancelled.")
                        continue
                    print(
                        f"Recorded simulated {transaction['category']} purchase "
                        f"of NGN {transaction['amount']:,.2f}."
                    )
                    print(
                        f"Remaining in category: "
                        f"NGN {transaction['remaining_category_balance']:,.2f}"
                    )
                    print(
                        f"Available today: "
                        f"NGN {transaction['remaining_daily_limit']:,.2f}"
                    )
                except (ValueError, InvalidOperation) as error:
                    print(error)
            case "4":
                return category_balances, daily_limits
            case _:
                print("Choose 1, 2, 3, or 4.")


def save_balances(category_balances, daily_limits, file_path="saved_balance.json"):
    user = {
        "ID": "1",
        "date": date.today().isoformat(),
        "finances": {},
        "daily_limits": {},
    }
    # Decimal values are stored as strings to preserve money exactly.
    for category, amount in category_balances.items():
        user["finances"][category] = str(amount)
    for category, amount in daily_limits.items():
        user["daily_limits"][category] = str(amount)

    destination = Path(file_path)
    temporary_file = destination.with_name(destination.name + ".tmp")
    with temporary_file.open("w", encoding="utf-8") as file:
        json.dump(user, file, indent=4)
    # Replace the old save only after writing the complete new file.
    temporary_file.replace(destination)


def load_balances(file_path="saved_balance.json"):
    with open(file_path, "r", encoding="utf-8") as file:
        user = json.load(file)
    if not isinstance(user, dict):
        raise ValueError("Saved balances must contain a user record.")
    if user.get("date") != date.today().isoformat():
        raise ValueError(
            "This save is from another day. Moving a budget to a new day "
            "has not been implemented yet."
        )
    if not isinstance(user.get("finances"), dict):
        raise ValueError("Saved category balances are missing.")
    if not isinstance(user.get("daily_limits"), dict):
        raise ValueError("Saved daily limits are missing.")

    category_balances = {}
    daily_limits = {}
    for category in ("feeding", "internet", "transport", "emergency"):
        amount = Decimal(user["finances"][category])
        if not amount.is_finite() or amount < 0:
            raise ValueError("Saved balances must be finite and non-negative.")
        category_balances[category] = amount
    for category in ("feeding", "internet", "transport"):
        amount = Decimal(user["daily_limits"][category])
        if not amount.is_finite() or amount < 0:
            raise ValueError("Saved daily limits must be finite and non-negative.")
        if amount > category_balances[category]:
            raise ValueError("A daily limit exceeds its category balance.")
        daily_limits[category] = amount
    return category_balances, daily_limits


def saved_budget_menu(file_path="saved_balance.json"):
    while True:
        choice = input(
            "\nWelcome. What would you like to do?\n"
            "1. Start a new budget (replaces the save after the session)\n"
            "2. Continue today's saved budget\n3. Exit\n"
        ).strip()
        try:
            match choice:
                case "1":
                    category_balances, daily_limits = user_menu()
                case "2":
                    category_balances, daily_limits = load_balances(file_path)
                    category_balances, daily_limits = user_menu(
                        category_balances, daily_limits
                    )
                case "3":
                    return
                case _:
                    print("Choose 1, 2, or 3.")
                    continue
        except (OSError, ValueError, InvalidOperation, KeyError, TypeError) as error:
            print(f"Could not open the budget: {error}")
            continue

        # Retry saving the same results without collecting the budget again.
        while True:
            try:
                save_balances(category_balances, daily_limits, file_path)
                print("Balances saved.")
                break
            except OSError as error:
                print(f"Could not save balances: {error}")
                choice = input("Enter 1 to retry saving or 2 to finish without saving: ").strip()
                match choice:
                    case "2":
                        return category_balances, daily_limits
                    case _:
                        continue
        return category_balances, daily_limits


def allowance_allocation():
    """Start the interactive budget menu."""
    return saved_budget_menu()


if __name__ == "__main__":
    allowance_allocation()

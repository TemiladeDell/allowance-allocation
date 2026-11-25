"""Student allowance prototype. Logic copied from the development notebook."""

from datetime import datetime, date, timedelta, timezone
from decimal import Decimal, InvalidOperation, ROUND_DOWN


def budget_today():
    return datetime.now(timezone(timedelta(hours=1))).date()


def choose_savings_mode():
    choice = input("1. Reluctant Saver\n2. Non-reluctant Saver\n").strip()
    match choice:
        case "1":
            return "reluctant"
        case "2":
            return "non_reluctant"
        case _:
            raise ValueError("Choose 1 or 2.")


# Choose the automatic percentage once during setup or a scheduled plan change.
def choose_savings_rate():
    choice = input("Choose your automatic daily savings rate:\n1. Small 10%\n2. Medium 20%\n3. Hardcore 30%\n").strip()
    match choice:
        case "1":
            return Decimal("0.10")
        case "2":
            return Decimal("0.20")
        case "3":
            return Decimal("0.30")
        case _:
            raise ValueError("Choose 1, 2, or 3.")


def schedule_savings_mode(budget_state, new_mode, today=None, new_rate=None):
    if today is None:
        today = budget_today()
    if today.isoformat() != budget_state["active_date"]:
        raise ValueError("Advance the budget to today first.")
    if new_mode not in ("reluctant", "non_reluctant"):
        raise ValueError("Unknown savings mode.")
    if new_mode == "non_reluctant":
        if new_rate not in (Decimal("0.10"), Decimal("0.20"), Decimal("0.30")):
            raise ValueError("Choose a savings rate of 10%, 20%, or 30%.")
    else:
        new_rate = None
    if new_mode == budget_state["savings_mode"] and new_rate == budget_state["savings_rate"]:
        budget_state["pending_savings_mode"] = None
        budget_state["pending_mode_date"] = None
        budget_state["pending_savings_rate"] = None
        return
    budget_state["pending_savings_mode"] = new_mode
    budget_state["pending_savings_rate"] = new_rate
    budget_state["pending_mode_date"] = (today + timedelta(days=1)).isoformat()


# Automatic deduction: no contribution prompt. Use the original daily allowance,
# excluding carryover. A saved date prevents another debit on the same day.
def savings_allocation(category_balances, daily_limits, budget_state, today=None):
    if today is None:
        today = budget_today()
    if today.isoformat() != budget_state["active_date"]:
        raise ValueError("Advance the budget to today first.")
    if budget_state["remaining_days"] <= 0 or budget_state["savings_mode"] == "reluctant":
        return Decimal("0")
    if budget_state["last_savings_date"] == today.isoformat():
        return Decimal("0")
    rate = budget_state["savings_rate"]
    if rate not in (Decimal("0.10"), Decimal("0.20"), Decimal("0.30")):
        raise ValueError("An automatic savings rate must be selected.")
    original_allowance = budget_state["original_daily_limits"]["feeding"]
    amount = (original_allowance * rate).quantize(Decimal("0.01"), rounding=ROUND_DOWN)
    if amount > daily_limits["feeding"] or amount > category_balances["feeding"]:
        raise ValueError("Not enough feeding money remains for automatic savings.")
    category_balances["feeding"] -= amount
    daily_limits["feeding"] -= amount
    category_balances["savings"] += amount
    budget_state["last_savings_date"] = today.isoformat()
    return amount


# Open each day by applying automatic savings before spending can begin.
# Reluctant mode still saves leftovers only when the previous day closes.
def advance_budget_day(category_balances, daily_limits, budget_state, today=None):
    if today is None:
        today = budget_today()
    active = date.fromisoformat(budget_state["active_date"])
    if today < active:
        raise ValueError("Today's date is earlier than the budget date.")
    saved = savings_allocation(category_balances, daily_limits, budget_state, active)
    while active < today and budget_state["remaining_days"] > 0:
        if budget_state["last_closed_date"] != active.isoformat():
            if budget_state["savings_mode"] == "reluctant":
                amount = daily_limits["feeding"]
                category_balances["feeding"] -= amount
                category_balances["savings"] += amount
                daily_limits["feeding"] = Decimal("0")
                saved += amount
            budget_state["last_closed_date"] = active.isoformat()
            budget_state["remaining_days"] -= 1
        active += timedelta(days=1)
        budget_state["active_date"] = active.isoformat()
        if budget_state["pending_mode_date"] is not None:
            if budget_state["pending_mode_date"] <= active.isoformat():
                budget_state["savings_mode"] = budget_state["pending_savings_mode"]
                budget_state["savings_rate"] = budget_state["pending_savings_rate"]
                budget_state["pending_savings_mode"] = None
                budget_state["pending_savings_rate"] = None
                budget_state["pending_mode_date"] = None
        for category in ("feeding", "internet", "transport"):
            if budget_state["remaining_days"] == 0:
                daily_limits[category] = Decimal("0")
            elif budget_state["remaining_days"] == 1:
                daily_limits[category] = category_balances[category]
            else:
                release = budget_state["original_daily_limits"][category]
                daily_limits[category] = min(
                    category_balances[category], daily_limits[category] + release
                )
        # The newly released allowance is reduced before the next menu action.
        saved += savings_allocation(category_balances, daily_limits, budget_state, active)
    return saved


from decimal import Decimal

# Values gotten from user input
def users_decision():
    total_allowance_allocated = Decimal(input("Enter your total amount allowance: "))

    days = int(input("Enter period of usage for this amount: "))

    if days <= 0:
        raise ValueError("Enter a positive number")

    internet_allowance = Decimal(input("Enter amount for Airtime/Data: "))
    transportation_allowance = Decimal(input("Enter amount for Transportation: "))
    emergency_reserve_allowance = Decimal(input("Enter amount for Emergency reserve: "))

    return total_allowance_allocated, internet_allowance, transportation_allowance, emergency_reserve_allowance, days





# Updated independent commitment function
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


# Allocation function to calculate daily budget based on balance and days
def allocation_function(balance, days):
    if balance < 0:
        raise ValueError("Balance cannot be negative")
    if days <= 0:
        raise ValueError("Days must be greater than zero")
    feeding_balance = balance / days
    # FIX: Calculate only; savings is called by the menu after setup.
    return feeding_balance


# Record one simulated purchase against the selected category.
from decimal import Decimal, InvalidOperation


def spending_function(category_balances, daily_limits, budget_state=None):
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
    if budget_state is not None:
        advance_budget_day(category_balances, daily_limits, budget_state)
        if budget_state["remaining_days"] <= 0:
            raise ValueError("The allowance period has ended.")
        category_balance = category_balances[category]
        daily_remaining = daily_limits[category]
        maximum_purchase = min(category_balance, daily_remaining)
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


from decimal import Decimal, InvalidOperation, ROUND_DOWN


def user_menu(category_balances=None, daily_limits=None, budget_state=None):
    if (category_balances is None) != (daily_limits is None):
        raise ValueError("Supply both balances and limits.")
    if budget_state is None:
        budget_state = {}
    if category_balances is not None and not budget_state:
        raise ValueError("A resumed savings budget requires its saved budget state.")
    while category_balances is None:
        try:
            allowance, internet, transport, emergency, days = users_decision()
            balance, expenditure_balance = commitment_function(allowance, internet, transport, emergency)
            mode = choose_savings_mode()
            rate = None
            if mode == "non_reluctant":
                rate = choose_savings_rate()
            category_balances = {
                "feeding": balance, "internet": internet, "transport": transport,
                "emergency": emergency, "savings": Decimal("0"),
            }
            daily_limits = {}
            for category in ("feeding", "internet", "transport"):
                daily_limits[category] = allocation_function(
                    category_balances[category], days
                ).quantize(Decimal("0.01"), rounding=ROUND_DOWN)
            budget_state.update({
                "active_date": budget_today().isoformat(), "remaining_days": days,
                "original_daily_limits": daily_limits.copy(), "savings_mode": mode,
                "pending_savings_mode": None, "pending_mode_date": None,
                "savings_rate": rate, "pending_savings_rate": None,
                "last_savings_date": None, "last_closed_date": None,
                "savings_rule_version": 2,
            })
            break
        except (ValueError, InvalidOperation) as error:
            print(error)
    # Older manual-savings saves need a rate choice before future day releases.
    # Their already-open day is preserved without a retrospective deduction.
    if budget_state["savings_rule_version"] == 1:
        while True:
            try:
                if budget_state["savings_mode"] == "non_reluctant":
                    print("Choose the automatic rate for future daily releases.")
                    budget_state["savings_rate"] = choose_savings_rate()
                if budget_state["pending_savings_mode"] == "non_reluctant":
                    print("Choose the rate for your scheduled savings mode.")
                    budget_state["pending_savings_rate"] = choose_savings_rate()
                budget_state["savings_rule_version"] = 2
                break
            except ValueError as error:
                print(error)
    while True:
        advance_budget_day(category_balances, daily_limits, budget_state)
        choice = input(
            "\n1. View balances\n2. View daily availability\n3. Make a simulated purchase\n"
            "4. Exit\n5. Change savings mode or rate tomorrow\n"
        ).strip()
        advance_budget_day(category_balances, daily_limits, budget_state)
        try:
            match choice:
                case "1":
                    for category, amount in category_balances.items():
                        print(f"{category.capitalize()}: NGN {amount:,.2f}")
                    print(f"Total remaining: NGN {sum(category_balances.values()):,.2f}")
                    print(f"Savings mode: {budget_state['savings_mode']}")
                    if budget_state["savings_mode"] == "non_reluctant":
                        print(f"Automatic daily savings: {budget_state['savings_rate'] * 100}%")
                case "2":
                    for category, amount in daily_limits.items():
                        print(f"{category.capitalize()} available today: NGN {amount:,.2f}")
                case "3":
                    if budget_state["remaining_days"] <= 0:
                        raise ValueError("The allowance period has ended.")
                    transaction = spending_function(category_balances, daily_limits, budget_state)
                    if transaction is None:
                        print("Purchase cancelled.")
                    else:
                        print(f"Recorded {transaction['category']} purchase: NGN {transaction['amount']:,.2f}")
                case "4":
                    return category_balances, daily_limits
                case "5":
                    if budget_state["remaining_days"] <= 0:
                        raise ValueError("The allowance period has ended.")
                    new_mode = choose_savings_mode()
                    new_rate = None
                    if new_mode == "non_reluctant":
                        new_rate = choose_savings_rate()
                    schedule_savings_mode(budget_state, new_mode, new_rate=new_rate)
                    print("Mode choice recorded for the next day.")
                case _:
                    print("Choose an option from 1 to 5.")
        except (ValueError, InvalidOperation) as error:
            print(error)


import json
from datetime import date, timedelta
from pathlib import Path
from decimal import Decimal, InvalidOperation


def save_balances(category_balances, daily_limits, file_path="saved_balance.json", budget_state=None):
    user = {"ID": "1", "date": budget_today().isoformat(), "finances": {}, "daily_limits": {}}
    for category, amount in category_balances.items():
        user["finances"][category] = str(amount)
    for category, amount in daily_limits.items():
        user["daily_limits"][category] = str(amount)
    if budget_state is not None:
        user["date"] = budget_state["active_date"]
        user["budget_state"] = budget_state.copy()
        user["budget_state"]["original_daily_limits"] = {}
        for category, amount in budget_state["original_daily_limits"].items():
            user["budget_state"]["original_daily_limits"][category] = str(amount)
        # Save rates as strings, just like other Decimal money values.
        for key in ("savings_rate", "pending_savings_rate"):
            if budget_state[key] is not None:
                user["budget_state"][key] = str(budget_state[key])
    destination = Path(file_path)
    temporary_file = destination.with_name(destination.name + ".tmp")
    with temporary_file.open("w", encoding="utf-8") as file:
        json.dump(user, file, indent=4)
    temporary_file.replace(destination)


def load_balances(file_path="saved_balance.json", budget_state=None):
    with open(file_path, "r", encoding="utf-8") as file:
        user = json.load(file)
    if not isinstance(user, dict):
        raise ValueError("Saved balances must contain a user record.")
    saved_date = date.fromisoformat(user["date"])
    if saved_date > budget_today():
        raise ValueError("Saved budget date is in the future.")
    category_balances = {}
    daily_limits = {}
    for category in ("feeding", "internet", "transport", "emergency", "savings"):
        if category == "savings":
            raw = user["finances"].get(category, "0")
        else:
            raw = user["finances"][category]
        amount = Decimal(raw)
        if not amount.is_finite() or amount < 0:
            raise ValueError("Saved balances must be finite and non-negative.")
        category_balances[category] = amount
    for category in ("feeding", "internet", "transport"):
        amount = Decimal(user["daily_limits"][category])
        if not amount.is_finite() or amount < 0 or amount > category_balances[category]:
            raise ValueError("Invalid daily availability.")
        daily_limits[category] = amount
    if budget_state is not None:
        if not isinstance(user.get("budget_state"), dict):
            raise ValueError("Older save lacks original daily amounts and remaining days. Keep a backup before creating a new savings budget.")
        state = user["budget_state"].copy()
        if date.fromisoformat(state["active_date"]) != saved_date:
            raise ValueError("Saved dates disagree.")
        if type(state["remaining_days"]) is not int or state["remaining_days"] < 0:
            raise ValueError("Invalid remaining days.")
        if state["savings_mode"] not in ("reluctant", "non_reluctant"):
            raise ValueError("Invalid savings mode.")
        if state["pending_savings_mode"] not in (None, "reluctant", "non_reluctant"):
            raise ValueError("Invalid pending savings mode.")
        # Migrate earlier manual-savings state without charging its open day again.
        version = state.get("savings_rule_version", 1)
        if type(version) is not int or version not in (1, 2):
            raise ValueError("Unsupported savings rules version.")
        state["savings_rule_version"] = version
        if version == 1:
            state["last_savings_date"] = state["active_date"]
            state["savings_rate"] = None
            state["pending_savings_rate"] = None
        for key in ("savings_rate", "pending_savings_rate"):
            raw = state[key]
            if raw is not None:
                value = Decimal(raw)
                if not value.is_finite() or value not in (Decimal("0.10"), Decimal("0.20"), Decimal("0.30")):
                    raise ValueError("Saved savings rate must be 10%, 20%, or 30%.")
                state[key] = value
        if version == 2:
            if state["savings_mode"] == "non_reluctant" and state["savings_rate"] is None:
                raise ValueError("Saved automatic savings rate is missing.")
            if state["pending_savings_mode"] == "non_reluctant" and state["pending_savings_rate"] is None:
                raise ValueError("Pending automatic savings rate is missing.")
        state.pop("last_voluntary_savings_date", None)
        for key in ("last_savings_date", "last_closed_date"):
            if state[key] is not None and date.fromisoformat(state[key]) > saved_date:
                raise ValueError("Invalid processing date.")
        if (state["pending_savings_mode"] is None) != (state["pending_mode_date"] is None):
            raise ValueError("Incomplete mode-change record.")
        if state["pending_mode_date"] is not None:
            if date.fromisoformat(state["pending_mode_date"]) != saved_date + timedelta(days=1):
                raise ValueError("Invalid mode-change date.")
        original_limits = {}
        for category in ("feeding", "internet", "transport"):
            amount = Decimal(state["original_daily_limits"][category])
            if not amount.is_finite() or amount < 0:
                raise ValueError("Invalid original daily allowance.")
            original_limits[category] = amount
        state["original_daily_limits"] = original_limits
        budget_state.clear()
        budget_state.update(state)
    elif saved_date != budget_today():
        raise ValueError("Use the saved-budget menu to advance elapsed days.")
    return category_balances, daily_limits


# FIX: Pass saved budget state through the menu and save it with the balances.
def saved_budget_menu(file_path="saved_balance.json"):
    while True:
        choice = input("\n1. New budget (replaces save after session)\n2. Resume budget\n3. Exit\n").strip()
        budget_state = {}
        try:
            match choice:
                case "1":
                    category_balances, daily_limits = user_menu(budget_state=budget_state)
                case "2":
                    category_balances, daily_limits = load_balances(file_path, budget_state)
                    category_balances, daily_limits = user_menu(category_balances, daily_limits, budget_state)
                case "3":
                    return
                case _:
                    print("Choose 1, 2, or 3.")
                    continue
        except (OSError, ValueError, InvalidOperation, KeyError, TypeError, AttributeError) as error:
            print(f"Could not open the budget: {error}")
            continue
        while True:
            try:
                save_balances(category_balances, daily_limits, file_path, budget_state)
                print("Balances and savings state saved.")
                break
            except OSError as error:
                print(f"Could not save balances: {error}")
                choice = input("Enter 1 to retry or 2 to finish without saving: ").strip()
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

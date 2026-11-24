"""Student allowance budgeting prototype developed in the companion notebook."""
from decimal import Decimal, InvalidOperation

def users_decision():
    """Collect the allowance period and protected commitment amounts."""
    total_allowance_allocated = Decimal(input('Enter your total amount allowance: '))
    days = int(input('Enter period of usage for this amount: '))
    if days <= 0:
        raise ValueError('Enter a positive number')
    internet_allowance = Decimal(input('Enter amount for Airtime/Data: '))
    transportation_allowance = Decimal(input('Enter amount for Transportation: '))
    emergency_reserve_allowance = Decimal(input('Enter amount for Emergency reserve: '))
    return (
        total_allowance_allocated,
        internet_allowance,
        transportation_allowance,
        emergency_reserve_allowance,
        days,
    )

def commitment_function(total_allowance, internet, transportation, emergency):
    """Validate amounts and return spendable balance, then protected total."""
    total_allowance_received = Decimal(total_allowance)
    if not total_allowance_received.is_finite():
        raise ValueError('Enter a finite number')
    if total_allowance_received < 0:
        raise ValueError('Enter a non-negative number')
    internet_allocation = Decimal(internet)
    transportation_allocation = Decimal(transportation)
    emergency_reserve_allocation = Decimal(emergency)
    if (
        not internet_allocation.is_finite()
        or not transportation_allocation.is_finite()
        or not emergency_reserve_allocation.is_finite()
    ):
        raise ValueError('Enter a finite number')
    if (
        internet_allocation < 0
        or transportation_allocation < 0
        or emergency_reserve_allocation < 0
    ):
        raise ValueError('Enter non-negative numbers')
    protected_allowance_commitment = (
        internet_allocation + transportation_allocation + emergency_reserve_allocation
    )
    if protected_allowance_commitment > total_allowance_received:
        raise ValueError(
            'Commitments greater than available balance. '
            f'You are {protected_allowance_commitment - total_allowance_received} short'
        )
    non_protected_allowance = total_allowance_received - protected_allowance_commitment
    return (non_protected_allowance, protected_allowance_commitment)

def allocation_function(balance, days):
    """Calculate the daily feeding budget from the spendable balance."""
    if balance < 0:
        raise ValueError('Balance cannot be negative')
    if days <= 0:
        raise ValueError('Days must be greater than zero')
    feeding_balance = balance / days
    return feeding_balance

def spending_function(maximum_budget):
    """Prompt for and validate one expense against the daily spending limit."""
    student_expense = Decimal(input('Enter how much you want to spend:  '))
    if not student_expense.is_finite():
        raise ValueError('Enter a finite number')
    if student_expense < 0:
        raise ValueError('Expense cannot be negative')
    if student_expense > maximum_budget:
        raise ValueError('Expense exceeds daily budget')
    return student_expense

def allowance_allocation():
    """Run budget setup and one feeding purchase with separate retry loops."""
    while True:
        try:
            allowance, internet, transport, emergency, days = users_decision()
            balance, expenditure_balance = commitment_function(
                allowance, internet, transport, emergency
            )
            feeding_balance = allocation_function(balance, days)
            print(f'Feeding balance using allocation_function: NGN {feeding_balance:,.2f}')
            print(
                f'An amount of {expenditure_balance} has been reserved '
                'for certain important expenses such as \n'
                f'{internet} for Airtime/Data\n'
                f'{transport} for Transportation\n'
                f'{emergency} for Emergency Reserve'
            )
            print(f'Remaining balance for daily expenses: NGN {balance:,.2f}')
            print('\n\n')
            break
        except (ValueError, InvalidOperation) as e:
            print(e)
    while True:
        try:
            daily_spending = spending_function(feeding_balance)
            remaining_daily_budget = feeding_balance - daily_spending
            print(
                f'Today you spent NGN {daily_spending:,.2f} '
                f'a balance of NGN {remaining_daily_budget:,.2f} remains for the day'
            )
            print('\n\n')
            remaining_spendable_balance = balance - daily_spending
            print(f'Remaining spendable balance is NGN {remaining_spendable_balance:,.2f}')
            break
        except (ValueError, InvalidOperation) as e:
            print(e)


if __name__ == "__main__":
    allowance_allocation()

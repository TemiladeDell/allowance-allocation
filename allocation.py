from datetime import datetime, timedelta

def allowance_allocation():
    """
    This function calculates the allowance allocation for students.
    It takes into account various expenses such as essential expenditure, emergency reserves, savings...
    The allocation is then distributed accordingly to ensure fairness and transparency in the process.
    """
    student_total_balance = int(input("Enter allowance:"))
    student_recurring_income = ''

    reccuring_income = ''
    irregular_income = ''
    airtime_allowance = ''
    food_allowance = ''
    emergency_reserve = ''
    savings = ''
    essential_expenditure = ''
    enjoyment_funds = ''
    current_time = ''
    mobile_number = ''
    maximum_airtime_purchasable = 300.00
    desrired_airtime_purchase_amount = ''

    """Funds are recorded in the Nigerian currency as a local test.
    This will be used until the program has reached a global state, accomodating multiple currencies
    """


    """ These values are hard-coded until Machine learning is involved"""

    while datetime.now() < future_time:
        if student_recurring_income <= 30000:
            network_provider = input('What is your network provider: 1.MTN\n2.GLO\n3.Airtel\n ')
            match network_provider:
                case "1":
                    mobile_number = input("Enter your mobile number: ")
                    desrired_airtime_purchase_amount = input("How much airtime would you like to purchase: ")
                    while int(desrired_airtime_purchase_amount) > int(maximum_airtime_purchasable):
                        desrired_airtime_purchase_amount = input(f"You cannot purchase an amount greater than {maximum_airtime_purchasable}")
                    print(f"Your transaction was successful")
                    student_total_balance == student_total_balance - int(desrired_airtime_purchase_amount)
                case "2":
                    mobile_number = input("Enter your mobile number: ")
                    desrired_airtime_purchase_amount = input("How much airtime would you like to purchase: ")
                    while int(desrired_airtime_purchase_amount) > int(maximum_airtime_purchasable):
                        desrired_airtime_purchase_amount = input(f"You cannot purchase an amount greater than {maximum_airtime_purchasable}")
                    print(f"Your transaction was successful")
                    student_total_balance == student_total_balance - int(desrired_airtime_purchase_amount)
                case "3":
                    mobile_number = input("Enter your mobile number: ")
                    desrired_airtime_purchase_amount = input("How much airtime would you like to purchase: ")
                    while int(desrired_airtime_purchase_amount) > int(maximum_airtime_purchasable):
                        desrired_airtime_purchase_amount = input(f"You cannot purchase an amount greater than {maximum_airtime_purchasable}")
                    print(f"Your transaction was successful")
                    student_total_balance == student_total_balance - int(desrired_airtime_purchase_amount)

            current_time
            current_time = datetime.now()
            future_time = current_time + timedelta(hours=24)
            

            

            
            
            
        

    pass
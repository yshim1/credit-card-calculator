"""Perform credit card calculations."""
from argparse import ArgumentParser
import sys

def get_min_payment(balance, fees = 0):
    """Computes the minimum credit ard payment
    
    Arguments: 
        balance: Total amount of the balance of an account that is left to pay
        fees (int): Fees associated with the credit card account (defaults to zero)
    Returns:
        float: minimum payment required
    """
    M = .02 #Float constant representing percent of balance that needs to be paid
    b = balance
    f = fees
    min_payment = ((b * M ) + f)
    if min_payment < 25:
        min_payment = 25
    return min_payment

def interest_charged(balance, apr):
    """Computes the amount of interest accrued in the next payment
    
    Arguments:
        balance: Balance of credit card that has not been paid of yet
        apr (int): Annual APR
    Returns:
        float: amount of interest accrued
    """
    a = apr/100
    Y = 365 #constant representing number of days in a year
    D = 30 #constant representing number of days in a billing cycle
    b = balance
    i = (a/Y) * b * D
    return i

def remaining_payments(balance, apr, targetamount, credit_line = 5000, fees = 0):
    """Computes the number of payments required to pay off credit card balance
    
    Arguments:
        balance: balance of credit card that has not been paid off yet
        apr (int): annual APR
        targetamount: amount user wants to pay per payment
        credit_line (int): maximum amount of balance of an account
        fees (int): amount of fees that will be charged in addition to minimum payment
    Returns:
        tuple: number of payments, months spent above quarter, half, and three 
        quarters of credit line
    """
    num_payments = 0
    quarter_credit = 0 #counter for months spent above 25% of credit_line
    half_credit = 0 #counter for months spent above 50% of credit_line
    three_quarter_credit = 0 #counter for months spent above 75% of credit_line
    while balance > 0:
        if targetamount == None:
            payment_amount = get_min_payment(balance, fees)
        else:
            payment_amount = targetamount
        interest_payment = interest_charged(balance, apr)
        balance_payment = payment_amount - interest_payment
        if balance_payment < 0:
            print("The balance will never be paid off")
            break
        else:
            balance -= balance_payment
            if balance > .75 * credit_line:
                three_quarter_credit += 1
            if balance > .50 * credit_line:
                half_credit += 1
            if balance > .25 * credit_line:
                quarter_credit +=1
        num_payments += 1
    counters = (num_payments, quarter_credit, half_credit, three_quarter_credit)
    #counters variable represents tuple with all counters
    return counters
        
def main(balance, apr, targetamount, credit_line, fees):
    """Starts execution of script
    
    Arguments:
        balance (int): amount in account that has not been paid off
        apr (int): annual APR
        targetamount (int): amount that user wants to pay per payment
        credit_line (int): maximum amount of balance of an account
        fees (int): amount of fees that will be charged
    Returns:
        String: 3 statements indicating how many months account holder will 
    spend above 25%, 50%, and 75% of credit line
    Side effects:
        prints statements indicating recommended starting payment, and how long
    it will take to pay off balance
    """
    min_payment = get_min_payment(balance, fees)
    print(f"Your recommended starting minimum payment is {min_payment}")
    pays_minimum = False
    if targetamount == None:
        pays_minimum == True
    r = remaining_payments(balance, apr, targetamount, credit_line, fees)
    if pays_minimum == True:
        print(f"""If you pay the minimum payment payments each month,
              you will pay off your balance in {r[0]} payments""")
    else:
        print(f"""If you make payments of {min_payment}, 
              you will pay of your balance in {r[0]} payments""")
        
        tup = (f"You will spend a total of {r[1]} months over 25% of the credit line \n",
             f"You will spend a total of {r[2]} months over 50% of the credit line \n",
             f"You will spend a total of {r[3]} months over 75% of the credit line")
        str = ''.join(tup) #joins tuple together turning it into a string
    return str    
    
def parse_args(args_list):
    """Takes a list of strings from the command prompt and passes them through as
    arguments
    Args:
        args_list (list) : the list of strings from the command prompt
    Returns:
        args (ArgumentParser)
    """
    parser = ArgumentParser()
    parser.add_argument('balance_amount', type = float, help = 'The total amount of balance left on the credit account')
    parser.add_argument('apr', type = int, help = 'The annual APR, should be an int between 1 and 100')
    parser.add_argument('credit_line', type = int, help = 'The maximum amount of balance allowed on the credit line.')
    parser.add_argument('--payment', type = int, default = None, help = 'The amount the user wants to pay per payment, should be a positive number')
    parser.add_argument('--fees', type = float, default = 0, help = 'The fees that are applied monthly.')
    # parse and validate arguments
    args = parser.parse_args(args_list)
    if args.balance_amount < 0:
        raise ValueError("balance amount must be positive")
    if not 0 <= args.apr <= 100:
        raise ValueError("APR must be between 0 and 100")
    if args.credit_line < 1:
        raise ValueError("credit line must be positive")
    if args.payment is not None and args.payment < 0:
        raise ValueError("number of payments per year must be positive")
    if args.fees < 0:
        raise ValueError("fees must be positive")
    return args

if __name__ == "__main__":
    try:
        arguments = parse_args(sys.argv[1:])
    except ValueError as e:
        sys.exit(str(e))
    print(main(arguments.balance_amount, arguments.apr, credit_line = arguments
.credit_line, targetamount = arguments.payment, fees = arguments.fees))
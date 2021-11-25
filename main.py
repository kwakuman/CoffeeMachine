import sys

MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0,
    }
}

resources = {
    "water": [300, "ml"],
    "milk": [200, "ml"],
    "coffee": [100, "g"],
    "money": [0, "$"]
}


# Prompt user by asking "What would you like?"
def request_command() -> str:
    """
    Asks user for input.
    :return: string with the user input
    """
    user_request = input("What would you like? (espresso/latte/cappuccino):")
    return user_request


# Turn off the Coffee Machine by entering "off" to the prompt
def check_for_off_command(command: str):
    """
    Checks whether maintenance have given a command to turn the machine off.
    :param command: user input
    :return: turns the machine off
    """
    if command == "off":
        print("Turning off ...")
        print("...")
        print("Bye!")
        sys.exit()


# Print report of resources currently in the coffee machine
def print_resources_report(current_resources: dict):
    """
    prints out all the resources the coffee machine currently contains.
    :param current_resources: dictionary containing all the resources and its units.
    The expected form is {"resource": [amount, unit]}
    :return:
    """
    for resource in current_resources:
        if resource == "money":
            print(f"{resource}: {current_resources[resource][1]}{current_resources[resource][0]}")
        else:
            print(f"{resource}: {current_resources[resource][0]}{current_resources[resource][1]}")


# Check resources sufficient?
def check_if_resources_are_sufficient(command: str, current_resources: dict) -> bool:
    """
    checks whether there is enough resources to make the type of coffee user has ordered
    :param command: the user input
    :param current_resources: dictionary containing all the resources and its units.
    The expected form is {"resource": [amount, unit]}
    :return:
    """
    resources_types = [x for x in MENU[command]["ingredients"].keys()]
    for resource in resources_types:
        if current_resources[resource][0] < MENU[command]["ingredients"][resource]:
            print(f"Sorry, there is not enough {resource}")
            return False
    return True


# Process coins.
def drink_payment() -> float:
    """
    allows user to insert coins in the coffee machine
    :return: total amount of inserted cash
    """
    coin_types = {"quarters": 0, "dimes": 0, "nickles": 0, "pennies": 0}
    for coin_type in coin_types:
        coin_types[coin_type] += int(input(f"How many {coin_type} are inserted?"))
    amount_inserted = round(coin_types["quarters"] * 0.25 +
                            coin_types["dimes"] * 0.1 +
                            coin_types["nickles"] * 0.05 +
                            coin_types["pennies"] * 0.01, 2)
    return amount_inserted


# Check transaction successful
def enough_money_inserted(money_available: float, command: str) -> bool:
    """
    checks whether the user has inserted enough cash to pay the the drink they ordered
    :param money_available: the amount of money user has inserted
    :param command: the coffee type user has ordered
    :return:
    """
    if money_available < MENU[command]["cost"]:
        return False
    return True


# TODO: Make Coffee
def make_coffee(coffee_type: str, current_resources: dict):
    """
    makes the coffee type user has ordered. Depletes the resources neccessary for making the coffee and adds the money
    for the coffee to the coffee machine
    :param coffee_type: coffee type ordered by the user
    :param current_resources: dictionary containing all the resources and its units currently available in the machine.
    The expected form is {"resource": [amount, unit]}
    :return:
    """
    for resource in MENU[coffee_type]["ingredients"]:
        current_resources[resource][0] -= MENU[coffee_type]["ingredients"][resource]
    current_resources["money"][0] += MENU[coffee_type]["cost"]
    print(f"Here is your {coffee_type}. Enjoy!")


if __name__ == "__main__":
    while True:
        user_input = request_command()  # get input from user
        check_for_off_command(command=user_input)  # check if the machine should turn off
        if user_input == "report":  # print out report if requested
            print_resources_report(resources)
            continue
        # continue if there are enough resources for the ordered coffee
        if check_if_resources_are_sufficient(command=user_input, current_resources=resources):
            inserted_money = drink_payment()  # let user pay for coffee with coins
            # check if user gave enough cash
            sufficient_money = enough_money_inserted(money_available=inserted_money, command=user_input)
            if sufficient_money:
                if inserted_money > MENU[user_input]["cost"]:
                    change = round(inserted_money - MENU[user_input]["cost"], 2)
                    print(f"Here is ${change} dollars in change.")
                make_coffee(coffee_type=user_input, current_resources=resources)
            else:
                print("Sorry that's not enough money. Money refunded.")

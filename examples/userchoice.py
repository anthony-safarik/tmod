def get_user_choice(choices):
    '''
    Accepts a list of choices. List length of zero returns None. If the length of the list is 1, it will return the item in the list.
    If there is more than one item in the list, the user is asked to input a number, and it returns the user's chosen item.
    '''
    if len(choices) == 0:
        return None
    if len(choices) == 1:
        return choices[0]
    else:
        print("Choose one:")
        for i, choice in enumerate(choices, start=1):
            print(f"{i}. {choice}")
        while True:
            try:
                user_input = int(input("Enter the number corresponding to your choice: "))
                if 1 <= user_input <= len(choices):
                    return choices[user_input - 1]
                else:
                    print("Invalid choice. Please enter a valid number.")
            except ValueError:
                print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    # Multiple choice question
    uc = get_user_choice(['I am not focused on my priorities.', 'I am focused on my priorities'])
    print(f"It sounds like {uc}")

    # Empty list gets you nothing in return
    uc = get_user_choice([])
    print(f"When user choice list has zero elements we get {type(uc)}")

    # When there is only one choice you get one response
    uc = get_user_choice(['Thanks for taking the time.'])
    print(uc)
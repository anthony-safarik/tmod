import socket

def get_computer_name():
    computer_name = socket.gethostname()
    return computer_name

if __name__ == "__main__":
    # print the computer name
    print(f'Computer Name: {get_computer_name()}')
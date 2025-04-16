# Make file for testing

def maketempfile(filename = "temp.txt", filetext = "'temp file for testing'"):
    with open(filename, 'w') as file:
        file.write(filetext)
        print(f'Temp file {filename} created')

if __name__ == "__main__":

    import time

    def get_now():
        return time.strftime("%y%m%d%H%M%S")

    filename = f'trashme_{get_now()}.txt'
    maketempfile(filename)
import time

def time_it(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function {func.__name__} took {end_time - start_time} seconds to run.")
        return result
    return wrapper

if __name__ == "__main__":
    
    @time_it
    def sleep2seconds():
        time.sleep(2)  # Introduce a 3-second delay

    sleep2seconds()

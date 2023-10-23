import os
import random

def save_random_numbers_to_file(file_name):
    # Generate 5000 random numbers between 0 and 1000
    random_numbers = [random.randint(0, 1000) for _ in range(5000)]

    # Convert the list of integers to a string with each number separated by a comma
    random_numbers_str = ",".join(map(str, random_numbers))

    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Combine the script directory with the file name
    file_path = os.path.join(script_dir, file_name)

    # Write the string to a file
    with open(file_path, 'w') as file:
        file.write(random_numbers_str)

# Usage
save_random_numbers_to_file('test.txt')

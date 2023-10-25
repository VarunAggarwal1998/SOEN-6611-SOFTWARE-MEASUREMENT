class metricstics:
    """
    A class used to calculate statistical measures on a list of numbers without using any built-in functions.

    Methods
    -------
    calculate_mean(numbers):
        Returns the arithmetic mean of the provided numbers.
    calculate_median(numbers):
        Returns the median value of the provided numbers.
    calculate_mode(numbers):
        Returns the mode of the provided numbers.
    calculate_min(numbers):
        Returns the smallest number in the provided list of numbers.
    calculate_max(numbers):
        Returns the largest number in the provided list of numbers.
    calculate_mean_absolute_deviation(numbers):
        Returns the mean absolute deviation of the provided numbers.
    calculate_standard_deviation(numbers):
        Returns the standard deviation of the provided numbers.
    """

    @staticmethod
    def calculate_mean(numbers):
        """Calculate the arithmetic mean of a list of numbers."""
        total = 0
        for num in numbers:
            total += num
        return total / len(numbers) if numbers else None

    @staticmethod
    def calculate_median(numbers):
        """Calculate the median of a list of numbers."""
        # First, we need to sort the numbers manually
        sorted_numbers = metricstics.sort_numbers(numbers)
        n = len(sorted_numbers)
        middle = n // 2
        if n % 2 == 0:
            return (sorted_numbers[middle - 1] + sorted_numbers[middle]) / 2
        else:
            return sorted_numbers[middle]

    @staticmethod
    def calculate_mode(numbers):
        """Calculate the mode of a list of numbers."""
        if not numbers:
            return None

        frequency_dict = {}
        for num in numbers:
            if num in frequency_dict:
                frequency_dict[num] += 1
            else:
                frequency_dict[num] = 1

        highest_frequency = 0
        for freq in frequency_dict.values():
            if freq > highest_frequency:
                highest_frequency = freq

        modes = [num for num, freq in frequency_dict.items() if freq == highest_frequency]

        # Return the mode if there's only one, otherwise, return the list of modes
        return modes[0] if len(modes) == 1 else modes

    @staticmethod
    def calculate_min(numbers):
        """Find the minimum number in a list of numbers."""
        if not numbers:
            return None

        min_num = numbers[0]
        for num in numbers[1:]:
            if num < min_num:
                min_num = num
        return min_num

    @staticmethod
    def calculate_max(numbers):
        """Find the maximum number in a list of numbers."""
        if not numbers:
            return None

        max_num = numbers[0]
        for num in numbers[1:]:
            if num > max_num:
                max_num = num
        return max_num

    @staticmethod
    def calculate_mean_absolute_deviation(numbers):
        """Calculate the mean absolute deviation of a list of numbers."""
        if not numbers:
            return None

        mean_value = metricstics.calculate_mean(numbers)
        total_deviation = 0
        for num in numbers:
            total_deviation += abs(num - mean_value)
        return total_deviation / len(numbers)

    @staticmethod
    def calculate_standard_deviation(numbers):
        """Calculate the standard deviation of a list of numbers."""
        if len(numbers) < 2:
            return None

        mean_value = metricstics.calculate_mean(numbers)
        sum_of_squared_differences = 0
        for num in numbers:
            sum_of_squared_differences += (num - mean_value) ** 2

        variance = sum_of_squared_differences / (len(numbers) - 1)  # Sample variance

        return metricstics.sqrt(variance)  # Standard deviation is the square root of variance

    @staticmethod
    def sort_numbers(numbers):
        """A simple sorting function specifically for this class."""
        if not numbers:
            return []

        # Implementing a simple bubble sort for the sake of example
        n = len(numbers)
        sorted_numbers = numbers[:]  # Create a copy of the list to sort
        for i in range(n):
            for j in range(0, n - i - 1):
                if sorted_numbers[j] > sorted_numbers[j + 1]:
                    sorted_numbers[j], sorted_numbers[j + 1] = sorted_numbers[j + 1], sorted_numbers[j]  # Swap

        return sorted_numbers

    @staticmethod
    def sqrt(number):
        """Calculate the square root of a number without using math.sqrt."""
        # Implementing a simple square root calculation using Newton's method
        if number < 0:
            raise ValueError("Cannot compute the square root of a negative number.")

        # Initial guess will be half of the number
        guess = number / 2.0
        # Loop for a number of times to refine the guess (this can be adjusted)
        for _ in range(20):  # This number can be increased for more precision
            guess = (guess + (number / guess)) / 2

        return guess

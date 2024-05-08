# ---------------------------- Libraries ------------------------------- #
import math

# ---------------------------- Constants ------------------------------- #
LOGO = """
             _   __  __      _   _               _ 
 _ __       / | |  \/  | ___| |_| |__   ___   __| |
| '_ \ _____| | | |\/| |/ _ \ __| '_ \ / _ \ / _` |
| |_) |_____| | | |  | |  __/ |_| | | | (_) | (_| |
| .__/      |_| |_|  |_|\___|\__|_| |_|\___/ \__,_|
|_|                                                
"""

# ---------------------------- Classes ------------------------------- #
class PMinus1Method:

    # Methods
    @staticmethod
    def __sieve_of_eratosthenes(bound: int) -> list[int]:
        """
        Generate all prime numbers up to a given number.
        :param int bound: The upper limit for generating prime numbers.
        :return: A list of prime numbers up to the bound.
        """

        primes = []
        sieve = [True] * (bound + 1)
        sieve[0] = sieve[1] = False

        for p in range(2, bound + 1):
            if sieve[p]:
                primes.append(p)

                for i in range(p * p, bound + 1, p):
                    sieve[i] = False

        return primes

    @staticmethod
    def __max_prime_powers(n: int, prime_numbers: list[int]) -> list[int]:
        """
        Find the powers of prime numbers less than or equal to a given number.
        :param int n: The upper limit for finding prime powers.
        :return: A list of prime numbers raised to their maximum powers less than or equal to n.
        """

        prime_powers = []

        for p in prime_numbers:
            power = 1

            while p ** power <= n:
                power += 1

            prime_powers.append(p ** (power - 1))

        return prime_powers

    @staticmethod
    def __montgomery_ladder(base: int, exponent: int, modulo: int) -> int:
        """
        Perform the Montgomery Ladder algorithm.
        :param int base: The base number for the calculation.
        :param int exponent: The exponent for the calculation.
        :param int modulo: The modulo for the calculation.
        :return: The result of the Montgomery Ladder calculation.
        """

        x = 1
        y = base % modulo
        exponent_in_bit = bin(exponent)[2:]

        for bit in exponent_in_bit:
            if bit == "1":
                x = (x * y) % modulo
                y = (y ** 2) % modulo
            else:
                y = (x * y) % modulo
                x = (x ** 2) % modulo

        return x

    @staticmethod
    def __extended_euclid_algorithm(a: int, b: int) -> tuple:
        """
        Perform the Extended Euclidean Algorithm.
        :param int a: The first number for the calculation.
        :param int b: The second number for the calculation.
        :return: The greatest common divisor of a and b, and the coefficients of Bézout's identity.
        """

        x = 0
        y = 1
        x_prev, y_prev = 1, 0

        while b != 0:
            quotient = a // b
            a, b = b, a % b
            x, x_prev = x_prev - quotient * x, x
            y, y_prev = y_prev - quotient * y, y

        return a, x_prev, y_prev


    def find_factors(self, number: int) -> list[int]:
        """
        Find the factors of a given number using the Pollard's p-1 method.
        :param int number: The number to find the factors of.
        :return: A list of factors of the number.
        """

        factors = []
        iteration = 0

        while True:
            b = int(math.sqrt(number))
            prime_numbers = self.__sieve_of_eratosthenes(b)
            prime_powers = self.__max_prime_powers(b, prime_numbers)
            k = math.prod(prime_powers)
            a = (self.__montgomery_ladder(prime_numbers[iteration], k, number) - 1) % number
            g = self.__extended_euclid_algorithm(a, number)[0]

            if g != 1 and g != number:
                factors.append(g)
                number //= g

                if number in prime_numbers:
                    factors.append(number)
                    break

            elif g == number:
                iteration += 1

            elif g == 1:
                print(f"Could not find all valid factors!")
                print(f"Increasing the bound could help.")
                break

        return factors


# ---------------------------- Functions ------------------------------- #
def validate_user_input(prompt: str) -> int:
    """
    Validate the user input.
    :param str prompt: The prompt message to display to the user.
    :return: The validated integer input from the user.
    """

    while True:
        user_input = input(prompt)

        try:
            value = int(user_input)

            if value <= 0:
                raise ValueError("Invalid Input: Please enter a positive number.")
            break

        except ValueError:
            print("Invalid Input: Please enter a positiv number.")

    return value

def main():
    """
    Main function of the program.
    :return: None
    """

    print(LOGO)

    # Variables
    p_1_method = PMinus1Method()
    number = validate_user_input("Please enter a positiv number: ")

    # Body
    print()
    print("-" * 50)
    print(f"The dividers of {number} are: {p_1_method.find_factors(number)}")


# ------------------------------ Main ---------------------------------- #

if __name__ == "__main__":
    main()

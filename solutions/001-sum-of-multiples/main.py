"""
Solve the sample problem: sum all numbers below 1000 divisible
by 3 or 5.

"""

def solve(limit: int = 1000) -> int:
    return sum(number for number in range(limit) if number % 3 == 0 or number % 5 == 0)


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()

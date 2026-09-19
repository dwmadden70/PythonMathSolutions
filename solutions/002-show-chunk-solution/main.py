from typing import NamedTuple

# NamedTuple provides an immutable, tuple-like result object with named fields.
# Type hints document expected types but are not enforced at runtime.
class ChunkedDivisionResult(NamedTuple):
    quotient: int
    remainder: int
    chunks: tuple[int, ...]

def chunked_division(dividend: int, divisor: int) -> ChunkedDivisionResult:
    """Return the quotient, remainder, and chunks used for the division.

    Args:
        dividend: The non-negative number to divide.
        divisor: The positive number to divide by.

    Raises:
        ValueError: If the dividend is negative or the divisor is not positive.
    """
    # Validate explicitly because Python type hints do not enforce value constraints.
    if dividend < 0:
        raise ValueError("Dividend must be non-negative.")
    if divisor <= 0:
        raise ValueError("Divisor must be greater than zero.")

    remaining_dividend = dividend
    chunks: list[int] = []

    # Start with the largest power of ten that could produce a useful chunk.
    multiplier_power = len(str(remaining_dividend)) - len(str(divisor))
    if multiplier_power < 0:
        multiplier_power = 0

    # range() stops before its end value, so -1 includes power 0 while counting down.
    for power in range(multiplier_power, -1, -1):
        factor = 10 ** power
        # // performs floor division. With these non-negative inputs, it gives the
        # same whole-number result as C# integer division.
        count = remaining_dividend // (divisor * factor)

        if count > 0:
            # Save the chunk and remove it from the amount still to divide.
            chunk_value = divisor * factor * count
            chunks.append(chunk_value)
            remaining_dividend -= chunk_value

    # divmod returns both results at once: (whole quotient, remainder).
    quotient, remainder = divmod(dividend, divisor)
    return ChunkedDivisionResult(
        quotient=quotient,
        remainder=remainder,
        chunks=tuple(chunks),
    )


def display_solution(
    dividend: int, divisor: int, result: ChunkedDivisionResult
) -> None:
    """Print the chunking steps and final result for a completed division.

    Args:
        dividend: The original number that was divided.
        divisor: The number used to divide the dividend.
        result: The quotient, remainder, and chunks from the division.
    """
    print(f"Solving {dividend:,} ÷ {divisor:,} using the chunking strategy:\n")

    remaining_dividend = dividend
    for chunk in result.chunks:
        quotient_piece = chunk // divisor
        # Subtract each chunk so the displayed leftover matches the process.
        remaining_dividend -= chunk
        print(f" -> Found chunk: {chunk:,} ({divisor} x {quotient_piece:,})")
        print(f" Leftover remaining: {remaining_dividend:,}\n")

    print("-" * 40)
    print("Combining the pieces:")

    chunks_str = " + ".join(f"{chunk:,}" for chunk in result.chunks) or "0"
    if result.remainder > 0:
        chunks_str += f" + {result.remainder:,} (remainder)"
    print(f"Original number broken down: {dividend:,} = {chunks_str}")

    quotients_str = " + ".join(
        f"{chunk // divisor:,}" for chunk in result.chunks
    ) or "0"
    print(f"Dividing each chunk gives: {quotients_str} = {result.quotient:,}")

    if result.remainder > 0:
        print(
            f"\nFinal Result: {result.quotient:,} "
            f"with a remainder of {result.remainder:,}"
        )
        print(f"Fraction Form: {result.quotient:,} {result.remainder}/{divisor}")
    else:
        print(f"\nFinal Result: {result.quotient:,} (Perfect division, no remainder!)")


def get_user_input() -> tuple[int | None, int | None]:
    try:
        # input() always returns text; int() converts it and raises ValueError if invalid.
        dividend = int(input("Enter the dividend: "))
        divisor = int(input("Enter the divisor: "))
        return dividend, divisor
    except ValueError as error:
        print(f"Error: {error}")
        return None, None

# This guard runs main() only when the file is executed directly, not imported.
def main() -> None:
    try:
        dividend, divisor = get_user_input()
        if dividend is None or divisor is None:
            return
        result = chunked_division(dividend, divisor)
    except ValueError as error:
        print(f"Error: {error}")
        return

    display_solution(dividend, divisor, result)


if __name__ == "__main__":
    main()

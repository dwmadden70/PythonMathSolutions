# Show Chunk Solution

This solution demonstrates **chunked division**. Instead of dividing the whole
number in one step, it repeatedly finds large pieces that can be divided by the
divisor.

For example, when dividing `17` by `5`, the solution finds a chunk of `15`:

```text
15 = 5 x 3
17 - 15 = 2
```

The final answer is therefore `3` with a remainder of `2`.

## How It Works

The program:

1. Reads a dividend and divisor from the user.
2. Checks powers of ten from largest to smallest.
3. Selects each divisor-sized chunk that fits into the amount remaining.
4. Adds the chunk quotients to produce the final quotient.
5. Reports any amount left over as the remainder.

The divisor must be greater than zero, and the dividend must be zero or
greater. Invalid values produce an error message instead of attempting the
calculation.

## Example

Run the solution from the repository root:

```bash
python solutions/002-show-chunk-solution/main.py
```

Example session:

```text
Enter the dividend: 17
Enter the divisor: 5
Solving 17 ÷ 5 using the chunking strategy:

 -> Found chunk: 15 (5 x 3)
 Leftover remaining: 2

----------------------------------------
Combining the pieces:
Original number broken down: 17 = 15 + 2 (remainder)
Dividing each chunk gives: 3 = 3

Final Result: 3 with a remainder of 2
Fraction Form: 3 2/5
```

The program also handles exact division. For example, `20` divided by `5`
produces a quotient of `4` with no remainder.

## Tests

The tests check normal division, exact division, zero values, invalid input,
displayed output, and the command-line error message. Run them from the
repository root:

```bash
python -m unittest discover -s solutions/002-show-chunk-solution -p "test_*.py"
```

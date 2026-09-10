from contextlib import redirect_stdout
from io import StringIO
import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch


# Load main.py directly because the solution folder name contains hyphens and
# therefore cannot be imported using Python's normal import statement.
MODULE_PATH = Path(__file__).with_name("main.py")
SPEC = importlib.util.spec_from_file_location("chunk_solution", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise ImportError(f"Unable to load {MODULE_PATH}")

chunk_solution = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(chunk_solution)


class ChunkedDivisionTests(unittest.TestCase):
    # These tests check the quotient, remainder, and chunks for normal inputs.
    def test_division_with_remainder(self) -> None:
        self.assertEqual(
            chunk_solution.chunked_division(17, 5),
            chunk_solution.ChunkedDivisionResult(3, 2, (15,)),
        )

    def test_exact_division(self) -> None:
        self.assertEqual(
            chunk_solution.chunked_division(20, 5),
            chunk_solution.ChunkedDivisionResult(4, 0, (20,)),
        )

    def test_dividend_smaller_than_divisor(self) -> None:
        self.assertEqual(
            chunk_solution.chunked_division(3, 5),
            chunk_solution.ChunkedDivisionResult(0, 3, ()),
        )

    def test_zero_dividend(self) -> None:
        self.assertEqual(
            chunk_solution.chunked_division(0, 5),
            chunk_solution.ChunkedDivisionResult(0, 0, ()),
        )

    def test_zero_or_negative_divisor(self) -> None:
        for divisor in (0, -5):
            with self.subTest(divisor=divisor):
                with self.assertRaises(ValueError):
                    chunk_solution.chunked_division(17, divisor)

    def test_negative_dividend(self) -> None:
        with self.assertRaises(ValueError):
            chunk_solution.chunked_division(-17, 5)

    # Redirect printed text into memory so it can be checked without cluttering
    # the test output shown in the terminal.
    def test_display_solution_shows_chunks_and_remainder(self) -> None:
        result = chunk_solution.chunked_division(17, 5)
        output = StringIO()

        with redirect_stdout(output):
            chunk_solution.display_solution(17, 5, result)

        displayed = output.getvalue()
        self.assertIn("Found chunk: 15 (5 x 3)", displayed)
        self.assertIn("Final Result: 3 with a remainder of 2", displayed)

    def test_main_reports_invalid_input(self) -> None:
        output = StringIO()

        # Replace input() with predictable answers for a repeatable CLI test.
        with patch.object(chunk_solution, "input", side_effect=["17", "0"]):
            with redirect_stdout(output):
                chunk_solution.main()

        self.assertEqual(
            output.getvalue(), "Error: Divisor must be greater than zero.\n"
        )


if __name__ == "__main__":
    unittest.main()
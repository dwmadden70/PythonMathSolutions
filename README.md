# PythonMathSolutions

A collection of standalone Python solutions for mathematical problems, exercises, and algorithms.

## Layout

Each problem lives in its own folder under `solutions`:

```text
solutions/
	001-sum-of-multiples/
		main.py
```

Use a zero-padded number and a short name for new folders. Keep the executable entry point in `main.py`; put problem-specific modules and tests beside it as the solution grows.

## Run a solution

Run a solution directly with Python:

```bash
python solutions/001-sum-of-multiples/main.py
```

List all discovered solutions:

```bash
python build.py --list
```

## Build executables

PyInstaller is used to create one-file executables in `dist/<solution-name>`:

```bash
python -m pip install -r requirements-build.txt

# Build one solution
python build.py --solution 001-sum-of-multiples

# Build every solution
python build.py --all
```

On Windows, the resulting executable is `dist/001-sum-of-multiples/001-sum-of-multiples.exe`. The equivalent VS Code tasks are available from **Terminal > Run Task**.

Python 3.10 or newer is recommended.

## Contributing

Contributions are welcome. Please open an issue to discuss substantial changes, then submit a pull request with a clear description of the solution and any relevant tests.

## License

License information will be added as the project develops.

More 

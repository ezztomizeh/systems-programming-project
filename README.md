# Systems Programming Project - SIC Assembler (Pass 1)

A Python implementation of **Pass 1** of a SIC assembler.

This project reads SIC assembly source code, validates opcodes/directives, builds a symbol table (`SYMTAB`), computes addresses using `LOCCTR`, and generates an intermediate file for later assembly stages.

## Features

- Parses SIC assembly source lines (label/opcode/operand)
- Supports comments starting with `.` or `;`
- Handles SIC machine opcodes from `op_codes/op_table.py`
- Handles directives:
  - `START`
  - `END`
  - `WORD`
  - `RESW`
  - `RESB`
  - `BYTE` (`C'...'` and `X'...'`)
- Detects duplicate symbols
- Generates intermediate address listing in `output/`
- Prints symbol table in a formatted terminal table
- Calculates and prints program length

## Project Structure

- `main.py` - CLI entry point
- `core/pass1.py` - Pass 1 logic (parsing, `SYMTAB`, `LOCCTR`, intermediate generation)
- `op_codes/op_table.py` - SIC opcode table
- `samples/` - sample SIC programs
- `output/` - generated intermediate files

## Requirements

- Python 3.8+
- `prettytable`

Install dependency:

```bash
pip install prettytable
```

## Usage

Run the assembler pass from the project root:

```bash
python main.py -filename <input_file> -output <output_file>
```

### Example 1

```bash
python main.py -filename samples/sample_code_1.txt -output intermediate_COPY.mdt
```

### Example 2

```bash
python main.py -filename samples/sample_code_2.txt -output intermediate_INLOOP.mdt
```

## Input Format

Each line is expected in one of these forms:

- `LABEL OPCODE OPERAND`
- `OPCODE OPERAND`
- `OPCODE`

Examples:

```asm
COPY      START      1000
FIRST     STL        RETADR
          RSUB
EOF       BYTE       C'EOF'
BUFFER    RESB       4096
          END        FIRST
```

## Output

1. **Intermediate file** (saved in `output/`) containing line addresses and source statements.
2. **SYMTAB printout** in terminal.
3. **Program length** printout in hex.

## Notes / Current Limitations

- This project currently implements **Pass 1 only**.
- Parsing is whitespace-based and expects standard SIC assembly formatting.
- For `BYTE X'..'`, hex digit count should be even.
- Global state (`SYMTAB`, `LOCCTR`) is reused within one run of the process.

## Quick Test

Try:

```bash
python main.py -filename samples/sample_code_1.txt -output test_output.mdt
```

Then check:

- `output/test_output.mdt`
- Terminal symbol table and program length

## Author

Systems Programming Project coursework implementation.

from core.pass1 import read_file, pass1, print_symtab, calculate_prog_length
import argparse

def main():
    parser = argparse.ArgumentParser(description="SIC assembler")
    parser.add_argument("-filename", help="Input assembly file")
    parser.add_argument("-output", help="Output file for intermediate code")

    args = parser.parse_args()

    if args.filename is None:
        raise ValueError("Please provide an input file using -filename\nExample: python pass1.py -filename code.txt -output intermediate.mdt")
    if args.output is None:
        raise ValueError("Please provide an output file using -output\nExample: python pass1.py -filename code.txt -output intermediate.mdt")

    lines = read_file(args.filename)
    pass1(lines, args.output)
    print_symtab()
    PRGLTH = calculate_prog_length()
    print(f"Program length: {hex(PRGLTH)}")

if __name__ == "__main__":
    main()
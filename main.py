from core.pass1 import read_file, pass1, print_symtab, calculate_prog_length
import argparse

def main():
    parser = argparse.ArgumentParser(description="Pass 1 of SIC assembler")
    parser.add_argument("-filename", help="Input assembly file")

    args = parser.parse_args()

    if args.filename is None:
        raise ValueError("Please provide an input file using -filename\nExample: python pass1.py -filename code.txt")
        

    lines = read_file(args.filename)
    pass1(lines)
    print_symtab()
    PRGLTH = calculate_prog_length()
    print(f"Program length: {hex(PRGLTH)}")

if __name__ == "__main__":
    main()

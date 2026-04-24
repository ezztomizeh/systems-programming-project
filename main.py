from core.pass1 import read_file, pass1, print_symtab, calculate_prog_length, SYMTAB
from core.pass2 import pass2
import argparse

def main():
    parser = argparse.ArgumentParser(description="SIC assembler")
    parser.add_argument("-filename", help="Input assembly file")
    parser.add_argument("-output", help="Output file for intermediate code")
    parser.add_argument("-pass2", action="store_true", help="Run pass2 after pass1")

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
    if args.pass2:
        pass2(SYMTAB=SYMTAB, 
              intermediate_file=f"./output/intermediate_files/{args.output}",
              object_output_file=f"./output/object_code_files/{args.output.replace('.mdt', '.obj')}",
              listing_output_file=f"./output/listing_files/{args.output.replace('.mdt', '.lst')}",
              program_length=PRGLTH)
if __name__ == "__main__":
    main()
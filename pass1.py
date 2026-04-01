from op_codes.op_table import op_table
from prettytable import PrettyTable

SYMTAB = {}
LOCCTR = None
PROGNAME = None

table = PrettyTable()
table.field_names = ["Symbol", "Address"]

def check_opcode(opcode: str) -> bool:
    if opcode in op_table:
        return True
    else:
        return False
    
def set_loctr(start_addr: int = None) -> None:
    global LOCCTR
    if start_addr is not None:
        LOCCTR = start_addr
    else:
        LOCCTR = 0

def set_progname(name: str) -> None:
    global PROGNAME
    PROGNAME = name

def check_symbol(symbol: str) -> bool:
    if symbol in SYMTAB:
        return True
    else:
        return False
    
def add_symbol(symbol: str, address: int) -> None:
    SYMTAB[symbol] = address

 
def analyze_lines(line: str) -> None:
    line = line.strip()
    if line.startswith(".") or line.startswith(";") or line == "":
        return None
    parts = line.split()
    if len(parts) == 3:
        label, opcode, operand = parts
    elif len(parts) == 2:
        label = None
        opcode, operand = parts
    elif len(parts) == 1:
        label = None
        opcode = parts[0]
        operand = None
    else:
        raise ValueError("Invalid line format")
    
    return label, opcode, operand


def read_file(filename: str) -> list:
    file = open(filename, "r")
    lines = file.readlines()
    file.close()
    return lines


def pass1(lines: list) -> None:
    global LOCCTR

    first_line = analyze_lines(lines[0])
    if first_line is None:
        raise ValueError("First line is empty or a comment")

    first_label, first_opcode, first_operand = first_line

    if first_opcode == "START":
        set_progname(first_label)
        set_loctr(int(first_operand, 16))
    else:
        set_progname(first_label)
        set_loctr()

    intermediate_file = open("intermediate.txt", "w")
    
    for line in lines[1:]:
        result = analyze_lines(line)
        if result is None:
            continue
        label, opcode, operand = result

        if opcode == "END":
            break

        if label is not None:
            if check_symbol(label):
                raise ValueError(f"Duplicate symbol: {label}")
            add_symbol(label, LOCCTR)
        
        if check_opcode(opcode):
            LOCCTR += 3
        elif opcode == "WORD":
            LOCCTR += 3
        elif opcode == "RESW":
            LOCCTR += 3 * int(operand)
        elif opcode == "RESB":
            LOCCTR += int(operand)
        elif opcode == "BYTE":
            if operand.startswith("C'") and operand.endswith("'"):
                LOCCTR += len(operand[2:-1])
            elif operand.startswith("X'") and operand.endswith("'"):
                LOCCTR += len(operand[2:-1]) // 2
            else:
                raise ValueError(f"Invalid BYTE operand: {operand}")
        else:
            raise ValueError(f"Invalid opcode: {opcode}")

    intermediate_file.close()

def print_symtab():
    for symbol, address in SYMTAB.items():
        table.add_row([symbol, hex(address)])
    print(table)


def main():
    lines = read_file("sample_code.txt")
    pass1(lines)
    print_symtab()

if __name__ == "__main__":
    main()
from op_codes.op_table import op_table as OPTAB

MAX_TEXT_RECORD_BYTES = 30


def read_file(file_path: str) -> list:
    with open(file_path, "r") as file:
        return file.readlines()


def create_header_record(progname: str, start_addr: int, prog_length: int) -> str:
    return f"H{progname:<6}{start_addr:06X}{prog_length:06X}"


def create_text_record(start_addr: int, object_codes: list) -> str:
    object_code_str = "".join(object_codes)
    record_length = len(object_code_str) // 2
    return f"T{start_addr:06X}{record_length:02X}{object_code_str}"


def create_end_record(start_addr: int) -> str:
    return f"E{start_addr:06X}"


def analyze_intermediate_line(line: str):
    parts = line.strip().split()

    if len(parts) == 4:
        address, label, opcode, operand = parts
    elif len(parts) == 3:
        address, opcode, operand = parts
        label = ""
    elif len(parts) == 2:
        address, opcode = parts
        label = ""
        operand = ""
    else:
        return None

    return int(address, 16), label, opcode, operand


def create_object_code(opcode: str, operand: str, SYMTAB: dict) -> str:
    if opcode not in OPTAB:
        raise ValueError(f"Invalid opcode: {opcode}")

    instruction = OPTAB[opcode]
    machine_opcode = instruction["opcode"]
    operand_exists = instruction["operand_exits"]

    if not operand_exists:
        return f"{machine_opcode:02X}0000"

    if operand == "":
        raise ValueError(f"Missing operand for opcode: {opcode}")

    indexed = False

    if operand.endswith(",X"):
        indexed = True
        operand = operand.replace(",X", "")

    if operand not in SYMTAB:
        raise ValueError(f"Undefined symbol: {operand}")

    address = SYMTAB[operand]

    if indexed:
        address = address | 0x8000

    return f"{machine_opcode:02X}{address:04X}"


def create_byte_object_code(operand: str) -> str:
    if operand.startswith("C'") and operand.endswith("'"):
        return "".join(f"{ord(c):02X}" for c in operand[2:-1])

    if operand.startswith("X'") and operand.endswith("'"):
        return operand[2:-1].upper()

    value = int(operand)

    if value < 0:
        value = (1 << 8) + value

    return f"{value:02X}"


def create_word_object_code(operand: str) -> str:
    value = int(operand)

    if value < 0:
        value = (1 << 24) + value

    return f"{value:06X}"


def write_listing_line(listing_file, address, label, opcode, operand, object_code):
    listing_file.write(
        f"{address:04X}           "
        f"{label:<14}"
        f"{opcode:<15}"
        f"{operand:<15}"
        f"{object_code.lower()}\n"
    )


def flush_text_record(output_file, text_start, text_codes):
    if text_codes:
        output_file.write(create_text_record(text_start, text_codes) + "\n")


def pass2(
    SYMTAB: dict,
    intermediate_file: str,
    object_output_file: str,
    listing_output_file: str,
    program_length: int
) -> None:

    lines = read_file(intermediate_file)

    text_start = None
    text_codes = []
    text_length = 0

    start_addr = 0
    progname = ""

    with open(object_output_file, "w") as obj_file, open(listing_output_file, "w") as lst_file:
        for line in lines:
            result = analyze_intermediate_line(line)

            if result is None:
                continue

            address, label, opcode, operand = result
            object_code = ""

            if opcode == "START":
                progname = label
                start_addr = int(operand, 16)

                obj_file.write(create_header_record(progname, start_addr, program_length) + "\n")
                write_listing_line(lst_file, address, label, opcode, operand, object_code)
                continue

            if opcode == "END":
                flush_text_record(obj_file, text_start, text_codes)

                if operand in SYMTAB:
                    execution_start = SYMTAB[operand]
                else:
                    execution_start = start_addr

                obj_file.write(create_end_record(execution_start) + "\n")
                write_listing_line(lst_file, address, label, opcode, operand, object_code)
                break

            if opcode in OPTAB:
                object_code = create_object_code(opcode, operand, SYMTAB)

            elif opcode == "WORD":
                object_code = create_word_object_code(operand)

            elif opcode == "BYTE":
                object_code = create_byte_object_code(operand)

            elif opcode in ["RESW", "RESB"]:
                flush_text_record(obj_file, text_start, text_codes)

                text_start = None
                text_codes = []
                text_length = 0

                write_listing_line(lst_file, address, label, opcode, operand, object_code)
                continue

            else:
                raise ValueError(f"Invalid opcode: {opcode}")

            object_length = len(object_code) // 2

            if text_start is None:
                text_start = address

            if text_length + object_length > MAX_TEXT_RECORD_BYTES:
                flush_text_record(obj_file, text_start, text_codes)

                text_start = address
                text_codes = []
                text_length = 0

            text_codes.append(object_code)
            text_length += object_length

            write_listing_line(lst_file, address, label, opcode, operand, object_code)
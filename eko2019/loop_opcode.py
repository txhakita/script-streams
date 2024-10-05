import subprocess
import os

opcode_file = "opcodes.txt"
temp_bin = "temp.bin"
result_file = "results-opcodes.txt"

def clean_opcode(opcode):
    return bytes.fromhex(opcode.replace('\\x', ''))

def create_opcodes():
    opcode = "488b01"
    n = len(opcode)

    for i in range(0x00, 0x100):
        if 0 <= i <= 15:
            res = ''.join(f'\\x0{hex(i)}').replace('0x', '')
        else:
            res = ''.join(f'\\x{hex(i)}').replace('0x', '')
        for i in range(0, n, 2):
            res += ''.join(f'\\x{opcode[i:i+2]}')
        with open(opcode_file, 'a') as f:
            f.write(res + "\n")

def disassemble(opcode):
    with open(temp_bin, "wb") as f:
        f.write(opcode)

    result = subprocess.run(['ndisasm', '-b', '64', temp_bin], capture_output=True, text=True)
    return result


def main():
    create_opcodes()

    with open(opcode_file) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            opcode_bytes = clean_opcode(line)
            
            with open(result_file, "a") as f:
                f.write(f"Disassembling: {line}\n")
                r = disassemble(opcode_bytes)
                f.write(r.stdout)
                f.write("-" * 40 + "\n")

    os.remove(opcode_file)
    os.remove(temp_bin)

if __name__ == '__main__':
    main()

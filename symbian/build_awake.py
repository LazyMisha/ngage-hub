"""Build the EKA1 keep-awake extension using GNU ARM binutils."""

import argparse
import binascii
from pathlib import Path
import struct
import subprocess
import tempfile


HERE = Path(__file__).resolve().parent
HEADER_SIZE = 124
CODE_BASE = 0x10000000


def words(*values):
    return struct.pack("<" + "I" * len(values), *values)


def assemble(tool_prefix):
    with tempfile.TemporaryDirectory() as tmp:
        obj = Path(tmp) / "awake.o"
        code_file = Path(tmp) / "awake.bin"
        subprocess.run([tool_prefix + "as", "-march=armv4t", "-o", obj,
                        HERE / "awake.s"], check=True)
        subprocess.run([tool_prefix + "objcopy", "-O", "binary", "-j", ".text",
                        obj, code_file], check=True)
        symbol_table = subprocess.check_output([tool_prefix + "nm", obj], text=True)
        symbols = {name: int(address, 16) for address, _, name in
                   (line.split() for line in symbol_table.splitlines())}
        return code_file.read_bytes(), symbols


def e32_image(code, symbols):
    text_size = symbols["import_reset_idle"]
    export_offset = symbols["export_table"]
    ordinals = struct.unpack_from("<3I", code, text_size)
    assert export_offset == text_size + 16
    assert len(code) == export_offset + 4

    # EUSER ordinal from the EKA1 EPOC6 export table. The Python ordinals are
    # from Python222.lib in Nokia's PyS60 1.3.1 First Edition SDK.
    euser = b"EUSER[100039e5].DLL\0"
    python = b"PYTHON222.DLL\0"
    names_offset = 4 + (2 + 1) * 4 + (2 + 2) * 4
    imports = (words(0, names_offset, 1, ordinals[0],
                     names_offset + len(euser), 2, ordinals[1], ordinals[2])
               + euser + python)
    imports += b"\0" * (-len(imports) % 4)
    imports = words(len(imports)) + imports[4:]

    # Both method-table pointers are in code page zero. Use the original
    # EKA1 inferred relocations (0x3000), as PETRAN does for these pointers.
    relocations = (symbols["method_name_pointer"], symbols["method_function_pointer"])
    assert all(0 <= offset < 4096 for offset in relocations)
    page_record = words(0, 8 + 2 * len(relocations))
    page_record += struct.pack("<2H", *(0x3000 + offset for offset in relocations))
    reloc_section = words(len(page_record), len(relocations)) + page_record

    uids = words(0x10000079, 0, 0)
    uid_check = binascii.crc_hqx(uids[::2], 0)
    uid_check |= binascii.crc_hqx(uids[1::2], 0) << 16
    code_check = sum(value[0] for value in struct.iter_unpack("<I", code)) & 0xffffffff
    import_offset = HEADER_SIZE + len(code)
    header = uids + words(
        uid_check, int.from_bytes(b"EPOC", "little"), 0x2000,
        code_check, 0, 0x00af0001, 0, 0,
        3, len(code), 0, 4096, 1048576, 8192, 0,
        symbols["entry"], CODE_BASE, 0, 2, HEADER_SIZE + export_offset,
        1, text_size, HEADER_SIZE, 0, import_offset,
        import_offset + len(imports), 0, 350,
    )
    assert len(header) == HEADER_SIZE
    return header + code + imports + reloc_section


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tool-prefix", default="arm-none-eabi-")
    parser.add_argument("output", nargs="?", type=Path,
                        default=HERE / "_ngageawake_v1.pyd")
    args = parser.parse_args()
    args.output.write_bytes(e32_image(*assemble(args.tool_prefix)))
    print(args.output.resolve())


if __name__ == "__main__":
    main()

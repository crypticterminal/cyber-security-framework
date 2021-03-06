from core.modules import base
from crypto.modules import hkbit
import argparse, sys, os


class HKBit(base.Program):
    """Symmetric index based bit inversion cryptography."""
    def __init__(self):
        super().__init__()
        self.parser.add_argument("input", type = argparse.FileType("rb"), help = "Input file.")
        self.parser.add_argument("-o", "--output", type = argparse.FileType("wb"), default = sys.stdout.buffer, help = "Output file.")
        self.parser.add_argument("-k", "--key", type = argparse.FileType("ab+"), default = None, help = "Key file.")
    
    def run(self):
        if not self.arguments.key:
            self.arguments.key = open("./hkbit.key", "ab+")
        self.arguments.key.seek(0)
        self.arguments.key.size = os.fstat(self.arguments.key.fileno()).st_size
        if not self.arguments.key.size:
            self.arguments.key.write(os.urandom(0xFFFF))
            self.arguments.key.size = 0xFFFF
        self.arguments.key.seek(0)
        
        chunk = self.arguments.input.read(0xFFF)
        ran = 0
        while chunk:
            if ran >= self.arguments.key.size:
                ran = 0
                self.arguments.key.seek(0)
            self.arguments.output.write(hkbit.crypt(chunk, self.arguments.key.read(0xFFF))[0])
            self.arguments.output.flush()
            chunk = self.arguments.input.read(0xFFF)
            ran += 0xFFF

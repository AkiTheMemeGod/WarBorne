import secrets as se
from collections import Counter
import os

def create_key():
    if not os.path.exists("key.key"):
        with open("key.key", "w") as f:
            key = se.token_urlsafe(64)
            f.write(key)
        return key.strip()
    else:
        with open("key.key", "r") as f:
            key = f.read()
        return key.strip()


class WarBorne:
    def __init__(self):
        if os.path.exists("key.key"):
            with open("key.key", "r") as f:
                key = f.read().strip()
        else:
            key = create_key()
        self.key = key
        self.key_len = len(key)

    def hash(self, message):
        return self.wb_hash(message)

    @staticmethod
    def get_vowel_count(content):
        vowels = 'aeiou'
        content = content.lower()
        count = Counter(content)
        return {v: count.get(v, 0) for v in vowels}

    def wb_hash(self, content):
        if not content:
            return "_WarBorne_Hash_"
        content = content.lower()
        vcount = self.get_vowel_count(content)
        key_nums = [ord(c) for c in self.key]
        key_seed = sum([n * (i + 1) for i, n in enumerate(key_nums)]) % 10**9
        a = vcount['a']
        e = vcount['e']
        i = vcount['i']
        o = vcount['o']
        u = vcount['u']

        hash_val = (
            a * (self.key_len ** 5) +
            e * (self.key_len ** 4) +
            i * (self.key_len ** 3) +
            o * (self.key_len ** 2) +
            u * self.key_len +
            len(content)
        )
        final_hash = (hash_val * key_seed) % (10**18)
        return hex(final_hash)[2:]

    def hash_file(self, filepath: str, encoding='utf-8'):
        try:
            with open(filepath, 'rb') as f:
                file_bytes = f.read()
                try:
                    content = file_bytes.decode(encoding)
                except UnicodeDecodeError:
                    content = file_bytes.hex()
            return self.wb_hash(content)
        except FileNotFoundError:
            return "File not found."


wb = WarBorne()
print(wb.hash_file("test.txt"))

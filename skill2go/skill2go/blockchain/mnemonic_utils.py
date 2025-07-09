import os
from mnemonic import Mnemonic

MNEMONIC_FILE = os.path.join(os.path.dirname(__file__), 'mnemonic.txt')
def get_or_generate_mnemonic():
    if os.path.exists(MNEMONIC_FILE):
        with open(MNEMONIC_FILE, 'r') as f:
            return f.read().strip()
    mnemo = Mnemonic("english")
    mnemonic_phrase = mnemo.generate(strength = 128)
    with open(MNEMONIC_FILE, 'w') as f:
        f.write(mnemonic_phrase)
        
    return mnemonic_phrase
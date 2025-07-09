import os
import subprocess
import time
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from skill2go.blockchain.mnemonic_utils import get_or_generate_mnemonic
def start_ganache():
    mnemonic = get_or_generate_mnemonic()
    os.environ["GANACHE_MNEMONIC"] = mnemonic
    ganache_command = f"ganache-cli --accounts 10 --mnemonic \"{mnemonic}\""
    print(f"Starting Ganache with mnemonic: {mnemonic}")
    subprocess.Popen(ganache_command, shell=True)

if __name__ == "__main__":
    start_ganache()

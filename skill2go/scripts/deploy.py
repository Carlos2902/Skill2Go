import sys
import os
import django

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skill2go.settings')
django.setup()

from skill2go.blockchain.blockchain_integration import deploy_contract
from exchange.models import BlockchainContract

def deploy():
    print("Deploying contract to the current ganache session...")
    contract_address, deployer_address = deploy_contract()  
    
    BlockchainContract.objects.update_or_create(
        id=1,   
        defaults=(
            {
                "contract_address": contract_address,
                "deployer_address": deployer_address,
            }
        )
    )

if __name__ == "__main__":
    deploy()

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile
from web3 import Web3
from eth_account import Account
from .models import BlockchainContract
web3 = Web3()  

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Automatically create a UserProfile when a new User is registered."""
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Ensure the UserProfile is saved whenever the User model is saved."""
    instance.userprofile.save()

@receiver(post_save, sender=UserProfile)
def assign_ethereum_address(sender, instance, created, **kwargs):
    """Assign an Ethereum address to the UserProfile upon creation."""
    if created and not instance.ethereum_address:
        ganache_accounts = web3.eth.accounts
        deployer_account = BlockchainContract.objects.values_list('deployer_address', flat=True).first()
        used_addresses = set(UserProfile.objects.exclude(ethereum_address=None).values_list('ethereum_address', flat=True))
        if deployer_account:
            used_addresses.add(deployer_account)
        available_accounts = [acc for acc in ganache_accounts if acc not in used_addresses]
        if available_accounts:
            checksum_address = web3.to_checksum_address(available_accounts[0])
            instance.ethereum_address = checksum_address
            instance.save()
            print(f"Assigned Ethereum address {checksum_address} to {instance.user.username}")
        else:
            raise ValueError("No more Ganache accounts available for use.")

import sys
import os
from web3 import Web3
from django.contrib import admin, messages
from django.utils import timezone
from .models import SkillCategory, SkillProvider, Skill, SkillExchange, SkillCertification
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','skill2go')))
from blockchain.blockchain_integration import record_certification_on_chain, get_certification_index, verify_certification_on_chain, reject_certification_on_chain


# Register models
admin.site.register(SkillCategory)
admin.site.register(SkillProvider)
admin.site.register(Skill)


@admin.register(SkillCertification)
class SkillCertificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'skill', 'status', 'blockchain_tx', 'created_at')
    actions = ['approve_certifications', 'reject_certifications']
    
    def _process_chain_actions(self, request, queryset, action_fn, target_status, success_msg):
        for cert in queryset.filter(status="Pending").exlcude(on_chain_id=None):
            checksum_address = Web3.to_checksum_address(cert.user.userprofile.ethereum_address)

# skill exchange to be implemented
# @admin.register(SkillExchange)
# class SkillExchangeAdmin(admin.ModelAdmin):
#     list_display = ['id', 'requester', 'skill', 'status', 'blockchain_tx', 'created_at']
#     actions = ['record_exchange_on_chain']
#     def record_exchange_on_chain(self, request, queryset):
#         for exchange in queryset:
#             if exchange.status == "Accepted" and not exchange.blockchain_tx:  
#                 tx_hash = record_exchange(exchange)  
#                 exchange.blockchain_tx = tx_hash
#                 exchange.save()
#         self.message_user(request, "Accepted skill exchanges have been recorded on the blockchain.")
#     record_exchange_on_chain.short_description = "Record accepted exchanges on blockchain"

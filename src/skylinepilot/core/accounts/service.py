"""
账号服务层（兼容层）
"""
from typing import Dict, List, Optional

from account_manager import account_manager


class AccountsService:
    """账号查询能力封装，隔离接口层与 manager 直接耦合"""

    def list_accounts(self) -> List[Dict]:
        return account_manager.list_accounts()

    def get_qr_status(self, account_id: str) -> Dict:
        return account_manager.check_qr_status(account_id)

    def export_session(self, account_id: str) -> Optional[str]:
        return account_manager.export_session(account_id)

    async def list_friends(self, account_id: str) -> List[Dict]:
        return await account_manager.get_friends(account_id)

    def get_phone_login_status(self, account_id: str) -> Dict:
        return account_manager.get_phone_login_status(account_id)


accounts_service = AccountsService()


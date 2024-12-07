from utils.error_code import ErrorCode
from utils.reply import reply
from ..models import accounts
from lib.logger import logger
from ..logic import request_detail
import random

# route
async def detail(id: str, xsec_token: str):
    """
    获取笔记信息
    """
    _accounts = await accounts.load()
    random.shuffle(_accounts)
    for account in _accounts:
        if account.get('expired', 0) == 1:
            continue
        account_id = account.get('id', '')
        res, succ = await request_detail(id, xsec_token, account.get('cookie', ''))
        if not succ:
            logger.error(f'get note detail failed, account: {account_id}, id: {id}')
            continue
        if res == {} and succ:
            logger.warning(f'get note detail failed, account: {account_id}, id: {id}, res: {res}')
        logger.info(f'get note detail success, account: {account_id}, id: {id}, res: {res}')
        return reply(ErrorCode.OK, '成功' , res)
    logger.warning(f'get note detail failed. id: {id}')
    return reply(ErrorCode.NO_ACCOUNT, '请先添加账号')

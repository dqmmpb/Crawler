from utils.error_code import ErrorCode
from utils.reply import reply
from ..models import accounts
from lib.logger import logger
from ..logic import request_search
import random

async def search(keyword: str, offset: int = 0, limit: int = 10, sort_type: int = 0, content_type: int = 0, search_id: str = None):
    """
    获取视频搜索
    "sort_type": 0: 综合(默认), 1：最热, 2：最新
    "content_type": 0: 全部, 1: 视频, 2: 图文
    """
    _accounts = await accounts.load()
    random.shuffle(_accounts)
    for account in _accounts:
        if account.get('expired', 0) == 1:
            continue
        account_id = account.get('id', '')
        res, succ, search_id = await request_search(keyword, account.get('cookie', ''), offset, limit, sort_type, content_type, search_id)
        if res == {} or not succ:
            logger.error(f'search failed, account: {account_id}, keyword: {keyword}, offset: {offset}, limit: {limit}, res: {res}')
            continue
        logger.info(f'search success, account: {account_id}, keyword: {keyword}, offset: {offset}, limit: {limit}, res: {res}')
        return reply(ErrorCode.OK, '成功' , res, search_id)
    logger.warning(f'search failed, keyword: {keyword}, offset: {offset}, limit: {limit}')
    return reply(ErrorCode.NO_ACCOUNT, '请先添加账号')

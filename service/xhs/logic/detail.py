from .common import COMMON_HEADERS
from lib import requests
from lib.logger import logger
from bs4 import BeautifulSoup
import re
import json



async def request_detail(id: str, xsec_token: str, cookie: str) -> tuple[dict, bool]:
    """
    请求小红书获取视频信息
    """
    # 获取xsec_token
    url = f'https://www.xiaohongshu.com/explore/{id}'
    params = {
        "xsec_token": xsec_token,
        "type": "normal",
        "xsec_source": "pc_share",
        "exSource": ""
    }
    headers = {"cookie": cookie}
    headers.update(COMMON_HEADERS)
    resp = await requests.get(url, headers=headers, params=params)
    if resp.status_code == 302:
        # 解析重定向
        soup = BeautifulSoup(resp.text, 'html.parser')
        # 访问频次异常，请勿频繁操作或重启试试
        pattern = re.compile('https://www\\.xiaohongshu\\.com/website-login/error\?redirectPath=.*')
        a_tag = soup.find('a', href=pattern)
        if a_tag is not None:
            logger.error(f"failed to get detail: {id}, resp: {resp.text}")
            return {}, False

        # 验证码
        pattern = re.compile('https://www\\.xiaohongshu\\.com/website-login/captcha\?redirectPath=.*')
        a_tag = soup.find('a', href=pattern)
        if a_tag is not None:
            logger.error(f"failed to get detail: {id}, resp: {resp.text}")
            return {}, False

        pattern = re.compile('window\\.__INITIAL_STATE__={.*}')
        text = soup.find(
            'script', text=pattern).text.replace('window.__INITIAL_STATE__=', '').replace('undefined', '""')
        target = json.loads(text)
        detail_errMsg_code = target.get('note', {}).get('serverRequestInfo', {}).get('errorCode', 0)
        # 笔记不存在
        if detail_errMsg_code == -510000:
            return {}, True
        # 当前内容无法展示
        if detail_errMsg_code == -510001:
            return {}, True
        return {}, False
    if resp.status_code != 200 or resp.text == '':
        return {}, False
    try:
        soup = BeautifulSoup(resp.text, 'html.parser')
        pattern = re.compile('window\\.__INITIAL_STATE__={.*}')
        text = soup.find(
            'script', text=pattern).text.replace('window.__INITIAL_STATE__=', '').replace('undefined', '""')
        target = json.loads(text)
        detail_data = target.get('note', {}).get('noteDetailMap', {}).get(id, {})
    except Exception as e:
        logger.error(f"failed to get detail: {id}, err: {e}")
        return {}, False
    return detail_data, True

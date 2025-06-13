import json

from .common import common_request

async def request_search(keyword: str, cookie: str, offset: int = 0, limit: int = 10, sort_type: int = 0, content_type: int = 0, search_id: str = None) -> tuple[dict, bool]:
    """
    请求抖音获取搜索信息
    """
    params = {
        "keyword": keyword,
        "search_channel": 'aweme_general',
        "search_source": 'normal_search',
        "filter_selected": json.dumps({
            "sort_type": f'{sort_type}',
            "publish_time": "0",
            "content_type": f'{content_type}'
        }, separators=(',', ':')),
        "query_correct_type": '1',
        "is_filter_search": '1',
        "need_filter_settings": "0",
        "enable_history": "1",
        "offset": offset,
        "count": limit,
    }
    if search_id:
        params['search_id'] = search_id
    headers = {"cookie": cookie}
    resp, succ = await common_request('/aweme/v1/web/general/search/single/', params, headers)
    if not succ:
        return resp, succ, search_id
    ret = resp.get('data', {})
    return ret, succ, resp.get("extra", {}).get("logid", None)

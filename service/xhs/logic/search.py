from .common import common_request
import execjs
import asyncio

async def request_search(keyword: str, cookie: str, sort: str, offset: int = 0, limit: int = 20, note_type: int = 0, search_id: str = None) -> dict:
    """
    请求小红书获取搜索信息
    """
    page_size = 20
    start_page = int( offset / page_size ) + 1
    end_page = int((offset + limit - 1) / page_size) + 1
    with open('lib/js/xhs.js', encoding='utf-8') as f:
        xhs_sign_obj = execjs.compile(f.read())
    tasks = [request_page(page, keyword, cookie, sort, page_size, xhs_sign_obj, note_type, search_id) for page in range(start_page, end_page + 1)]
    pages = await asyncio.gather(*tasks)
    results = []
    for result in pages:
        results.extend(result)
    results = results[(offset % page_size):(offset % page_size + limit)]
    return results

async def request_page(page: int, keyword: str, cookie: str, sort: str, page_size: int, xhs_sign_obj, note_type: int = 0, search_id: str = None) -> list:
    headers = {"cookie": cookie}
    params = {
        "ext_flags": [],
        "image_formats": ["jpg", "webp", "avif"],
        "keyword": keyword,
        "note_type": note_type,
        "sort": sort,
        "page": page,
        "page_size": page_size,
        'search_id': search_id or xhs_sign_obj.call('searchId')
    }
    resp, succ = await common_request('/api/sns/web/v1/search/notes', params, headers, True, True)
    if not succ:
        return []
    return resp.get('data', {}).get('items', [])

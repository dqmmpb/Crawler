from .common import common_request
import execjs

async def request_search(keyword: str, cookie: str, offset: int = 0, limit: int = 20, sort: str = "general", note_type: int = 0, search_id: str = None) -> dict:
    """
    请求小红书获取搜索信息
    """
    page_size = 20
    start_page = int( offset / page_size ) + 1
    end_page = int((offset + limit - 1) / page_size) + 1
    with open('lib/js/xhs.js', encoding='utf-8') as f:
        xhs_sign_obj = execjs.compile(f.read())
    results = []
    for page in range(start_page, end_page + 1):
        if search_id is None:
            items, succ, search_id = await request_page(page, keyword, cookie, page_size, xhs_sign_obj, sort, note_type, search_id)
        else:
            items, succ, _ = await request_page(page, keyword, cookie, page_size, xhs_sign_obj, sort, note_type, search_id)
        if not succ:
            return items, succ, search_id

        results.extend(items)

    ret = results[(offset % page_size):(offset % page_size + limit)]
    return ret, succ, search_id

async def request_page(page: int, keyword: str, cookie: str, page_size: int, xhs_sign_obj, sort: str = "general", note_type: int = 0, search_id: str = None) -> list:
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
        return resp, succ, params.get("search_id", None)
    return resp.get('data', {}).get('items', []), succ, params.get("search_id", None)

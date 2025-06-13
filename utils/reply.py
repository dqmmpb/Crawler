from .error_code import ErrorCode

def reply(code: ErrorCode = ErrorCode.OK, msg: str = "OK", data: dict = None, search_id: str = None):
    return {
        "code": code.value,
        "msg": msg,
        "data": data,
        "search_id": search_id,
    }

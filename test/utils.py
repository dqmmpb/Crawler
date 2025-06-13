import errno
import os
import jsonlines

from urllib.parse import urlparse, unquote


COMMON_HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "cache-control": "no-cache",
    "content-type": "application/json;charset=UTF-8",
    "dnt": "1",
    "origin": "https://www.xiaohongshu.com",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://www.xiaohongshu.com/",
    "sec-ch-ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
}


def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def get_file_size(file_path):
    size = os.path.getsize(file_path)
    return size


def extract_path(url):
    # 解析URL
    parsed_url = urlparse(unquote(url))

    # 获取网络位置(域名)和路径，并解码可能存在的百分比编码
    netloc_path = parsed_url.netloc + parsed_url.path
    path = unquote(netloc_path)

    # 构造保存路径，去掉URL中的http或https部分，只保留域名和后续路径
    image_path = netloc_path[1:] if path.startswith('/') else netloc_path

    return image_path


def read_jsonlines(file_path: str) -> list[dict]:
    """
    从 jsonlines 文件中读取数据。
    :param file_path: 文件路径。
    :return: 数据列表（每个元素是一个字典）。
    """
    data = []
    with jsonlines.open(file_path, mode="r") as reader:
        for item in reader:
            data.append(item)
    return data


def write_jsonlines(file_path: str, data: list[dict]) -> None:
    """
    将数据写入 jsonlines 文件。
    :param file_path: 文件路径。
    :param data: 要写入的数据（列表，每个元素是一个字典）。
    """
    with jsonlines.open(file_path, mode="w") as writer:
        writer.write_all(data)


def append_jsonlines(file_path: str, data: list[dict]) -> None:
    """
    向现有的 jsonlines 文件中追加数据。
    :param file_path: 文件路径。
    :param data: 要追加的数据（列表，每个元素是一个字典）。
    """
    with jsonlines.open(file_path, mode="a") as writer:
        writer.write_all(data)


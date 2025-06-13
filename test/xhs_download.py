import asyncio
import copy
import json
import os
import random
import time

import requests

from utils import ensure_dir, get_file_size, extract_path, read_jsonlines
from xhs_utils import COMMON_HEADERS


async def request_download(media_url: str, media_path: str, headers=None):
    # 默认请求头
    if headers is None:
        headers = copy.deepcopy(COMMON_HEADERS)

    try:
        response = requests.get(media_url, headers=headers, timeout=10)
        if response.status_code == 200:
            # 写入文件
            with open(media_path, "wb") as f:
                f.write(response.content)

            print(f"Download success: {media_path}")
            return media_path
        else:
            print(f"Download failed: {response.status_code} - {media_url}")
            return None
    except Exception as e:
        print(f"Download error: {e} - {media_url}")
        return None


async def download(media_url: str, media_path: str, no_media_note: set, note, media: dict):
    # 确保路径存在
    ensure_dir(media_path)

    if os.path.exists(media_path):
        print(f"Exist {media_url} to {media_path}")
        size = get_file_size(media_path)
        if size == 0:
            no_media_note.add(note['id'])
            try:
                os.remove(media_path)
                print("Deleted the incomplete file: {}".format(media_path))
            except OSError as e:
                print("Failed to delete the incomplete file: {}. Error: {}".format(media_path, str(e)))

    else:
        print("Saving {} to {}".format(media_url, media_path))
        try:
            await request_download(media_url, media_path)
            print("Saved {} to {}".format(media_url, media_path))
            size = get_file_size(media_path)
            if size == 0:
                no_media_note.add(note['id'])
                try:
                    os.remove(media_path)
                    print("Deleted the incomplete file: {}".format(media_path))
                except OSError as e:
                    print("Failed to delete the incomplete file: {}. Error: {}".format(media_path, str(e)))
        except Exception as e:
            print("Error {} to {} {}".format(media_url, media_path, str(e)))
            # 如果下载失败，尝试删除可能存在的部分下载的本地文件
            if os.path.exists(media_path):
                try:
                    os.remove(media_path)
                    print("Deleted the incomplete file: {}".format(media_path))
                except OSError as e:
                    print("Failed to delete the incomplete file: {}. Error: {}".format(media_path, str(e)))
        time.sleep(random.randint(1, 5))


async def download_photo(output_dir: str, no_media_note: set, note, media: dict):
    print(f"[{note['type']}]: {media['urlDefault']}")

    media_url = media['urlDefault']

    path = extract_path(media_url)
    media_path = os.path.join(output_dir, path[1:]) if path.startswith('/') else os.path.join(output_dir, path)
    media_path = media_path.rsplit("!")[0]
    media_path = os.path.join(os.path.dirname(media_path), os.path.basename(media_path) + ('.jpg' if '.' not in os.path.basename(media_path) else ''))
    print(f"media_path: {media_path}")

    await download(media_url, media_path, no_media_note, note, media)


async def download_video(output_dir: str, no_media_note: set, note, media: dict):
    for stream_type in media['media']['stream']:
        streams = media['media']['stream'][f"{stream_type}"]
        if streams is not None:
            for key, stream in enumerate(streams):
                print(f"[{note['type']}]: {stream['masterUrl']}")
                media_url = stream['masterUrl']
                path = extract_path(media_url)
                media_path = os.path.join(output_dir, path[1:]) if path.startswith('/') else os.path.join(output_dir, path)
                media_path = media_path.rsplit("!")[0]
                media_path = os.path.join(os.path.dirname(media_path), os.path.basename(media_path) + ('.mp4' if '.' not in os.path.basename(media_path) else ''))
                await download(media_url, media_path, no_media_note, note, stream)


async def download_media(output_dir: str, no_media_note: set, results: list[dict]):
    for i, result in enumerate(results):
        print(f"Index {i}/{len(results)}: {json.dumps(result, ensure_ascii=False)}")
        note = result['note']
        if note is not None:
            if note['type'] == 'normal':
                print(f"[{note['type']}]: {note['imageList']}")
                for media in note['imageList']:
                    if media is not None:
                        await download_photo(output_dir, no_media_note, note, media)
            if note['type'] == 'video':
                print(f"[{note['type']}]: {note['imageList']}")
                for media in note['imageList']:
                    if media is not None:
                        await download_photo(output_dir, no_media_note, note, media)
                await download_video(output_dir, no_media_note, note, note['video'])


async def main():
    ###########################################

    input_files = [
        f"../result/xhs/search__荨麻疹__1749720904.211481__unique__note__1749721158.15949.jsonl",
    ]

    for input_file in input_files:

        results = read_jsonlines(input_file)
        print(f"input_file: {input_file}, result: {len(results)}")

        output_base_dir = os.path.dirname(input_file)
        output_dir_name = os.path.splitext(os.path.basename(input_file))[0]
        output_dir = os.path.join(output_base_dir, output_dir_name + "/")
        # 确保存储目录存在
        ensure_dir(output_dir)

        no_media_note = set()

        await download_media(output_dir, no_media_note, results)



    ###########################################


if __name__ == '__main__':
    asyncio.run(main())

import copy
import random

import execjs
import requests
from cookie import HOST, XHS_COOKIE
import unittest
import time

from xhs_utils import write_jsonlines, read_jsonlines


# from lib.logger import logger
#
# config = {
#     'logger': {
#         'type': 'file',
#         'level': 'INFO',
#         'backupcount': 144,
#         'format': '[%(asctime)s][%(name)s][%(levelname)s]: %(message)s',
#         'path': '.log/crawler.log'
#     }
# }
# logger.setup(config)


class TestModule(unittest.TestCase):
    # 添加账户接口
    def test_add_account(self):
        data = {
            "id": "66f69f62000000001c00265a",
            "cookie": XHS_COOKIE
        }
        response = requests.post(f'{HOST}/xhs/add_account', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)

    # 账户列表接口
    def test_account_list(self):
        # 添加账户
        data = {
            "id": "66f69f62000000001c00265a",
            "cookie": XHS_COOKIE
        }
        response = requests.post(f'{HOST}/xhs/add_account', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)

        # 获取账户列表
        response = requests.get(f'{HOST}/xhs/account_list')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertGreater(len(response.json()['data']), 0)

    # 过期账户接口
    def test_expire_account(self):
        # 添加账户
        data = {
            "id": "66f69f62000000001c00265a",
            "cookie": XHS_COOKIE
        }
        response = requests.post(f'{HOST}/xhs/add_account', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)

        # 过期账户
        data = {
            "id": "66f69f62000000001c00265a",
        }
        response = requests.post(f'{HOST}/xhs/expire_account', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)

    # 获取详情接口
    def test_detail(self):
        # 添加账户
        data = {
            "id": "66f69f62000000001c00265a",
            "cookie": XHS_COOKIE
        }
        response = requests.post(f'{HOST}/xhs/add_account', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)

        # 获取详情
        param = {
            "id": '66864b41000000001e012734',
            "xsec_token": 'ABAsaFmYws_TVON7WrKRRzSyC2q8Akx7V1qRCeAbPppa8=',
        }
        response = requests.get(f'{HOST}/xhs/detail', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertEqual(response.json()['data']['note']['noteId'], param['id'])

    # 获取详情接口
    def test_feed(self):
        # 添加账户
        data = {
            "id": "66f69f62000000001c00265a",
            "cookie": XHS_COOKIE
        }
        response = requests.post(f'{HOST}/xhs/add_account', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)

        # 获取详情
        param = {
            "id": '66864b41000000001e012734',
            "xsec_token": 'ABAsaFmYws_TVON7WrKRRzSyC2q8Akx7V1qRCeAbPppa8=',
        }
        response = requests.get(f'{HOST}/xhs/feed', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertEqual(response.json()['data']['id'], param['id'])

    # 获取评论接口
    def test_comments(self):
        # 添加账户
        data = {
            "id": "66f69f62000000001c00265a",
            "cookie": XHS_COOKIE
        }
        response = requests.post(f'{HOST}/xhs/add_account', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)

        # 获取评论
        param = {
            "id": '66864b41000000001e012734',
            "xsec_token": 'ABAsaFmYws_TVON7WrKRRzSyC2q8Akx7V1qRCeAbPppa8=',
        }
        response = requests.get(f'{HOST}/xhs/comments', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertGreater(len(response.json()['data']['comments']), 0)

        time.sleep(1)
        # 测试翻页 page_size = 20
        offset = 55
        limit = 5
        param = {
            "id": '66864b41000000001e012734',
            "xsec_token": 'ABAsaFmYws_TVON7WrKRRzSyC2q8Akx7V1qRCeAbPppa8=',
            "offset": offset,
            "limit": limit
        }
        response = requests.get(f'{HOST}/xhs/comments', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertGreater(len(response.json()['data']['comments']), 0)
        first_page = [comment['id'] for comment in response.json()['data']['comments']]

        time.sleep(1)
        offset = 60
        limit = 5
        param = {
            "id": '66864b41000000001e012734',
            "xsec_token": 'ABAsaFmYws_TVON7WrKRRzSyC2q8Akx7V1qRCeAbPppa8=',
            "offset": offset,
            "limit": limit
        }
        response = requests.get(f'{HOST}/xhs/comments', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertGreater(len(response.json()['data']['comments']), 0)
        second_page = [comment['id'] for comment in response.json()['data']['comments']]

        time.sleep(1)
        offset = 55
        limit = 10
        param = {
            "id": '66864b41000000001e012734',
            "xsec_token": 'ABAsaFmYws_TVON7WrKRRzSyC2q8Akx7V1qRCeAbPppa8=',
            "offset": offset,
            "limit": limit
        }
        response = requests.get(f'{HOST}/xhs/comments', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertGreater(len(response.json()['data']['comments']), 0)
        self.assertSequenceEqual([comment['id'] for comment in response.json()['data']['comments']], first_page + second_page)

    # 获取评论回复接口
    def test_reply(self):
        # 添加账户
        data = {
            "id": "66f69f62000000001c00265a",
            "cookie": XHS_COOKIE
        }
        response = requests.post(f'{HOST}/xhs/add_account', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)

        # 获取评论回复
        param = {
            "id": '66864b41000000001e012734',
            "comment_id": '66864b5e000000000303a2db',
            "xsec_token": 'ABAsaFmYws_TVON7WrKRRzSyC2q8Akx7V1qRCeAbPppa8=',
        }
        response = requests.get(f'{HOST}/xhs/replys', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertGreater(len(response.json()['data']['comments']), 0)

        time.sleep(1)
        # 测试翻页 page_size = 20
        offset = 5
        limit = 5
        param = {
            "id": '66864b41000000001e012734',
            "comment_id": '66864b5e000000000303a2db',
            "xsec_token": 'ABAsaFmYws_TVON7WrKRRzSyC2q8Akx7V1qRCeAbPppa8=',
            "offset": offset,
            "limit": limit
        }
        response = requests.get(f'{HOST}/xhs/replys', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertGreater(len(response.json()['data']['comments']), 0)
        first_page = [comment['id'] for comment in response.json()['data']['comments']]

        time.sleep(1)
        offset = 10
        limit = 5
        param = {
            "id": '66864b41000000001e012734',
            "comment_id": '66864b5e000000000303a2db',
            "xsec_token": 'ABAsaFmYws_TVON7WrKRRzSyC2q8Akx7V1qRCeAbPppa8=',
            "offset": offset,
            "limit": limit
        }
        response = requests.get(f'{HOST}/xhs/replys', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertGreater(len(response.json()['data']['comments']), 0)
        second_page = [comment['id'] for comment in response.json()['data']['comments']]

        time.sleep(1)
        offset = 5
        limit = 10
        param = {
            "id": '66864b41000000001e012734',
            "comment_id": '66864b5e000000000303a2db',
            "xsec_token": 'ABAsaFmYws_TVON7WrKRRzSyC2q8Akx7V1qRCeAbPppa8=',
            "offset": offset,
            "limit": limit
        }
        response = requests.get(f'{HOST}/xhs/replys', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertGreater(len(response.json()['data']['comments']), 0)
        self.assertSequenceEqual([comment['id'] for comment in response.json()['data']['comments']], first_page + second_page)

    # 搜索接口
    def test_search(self, filepath, keywords: list[str], page: int = 1, pages: int = 10):
        # # 添加账户
        # data = {
        #     "id": "66f69f62000000001c00265a",
        #     "cookie": XHS_COOKIE
        # }
        # response = requests.post(f'{HOST}/xhs/add_account', json=data)
        # self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.json()['code'], 0)

        print(f"文件路径: {filepath}")
        print(f"搜索开始")

        # with open('../lib/js/xhs.js', encoding='utf-8') as f:
        #     xhs_sign_obj = execjs.compile(f.read())
        # search_id = xhs_sign_obj.call('searchId')
        search_id = None
        # search_id = '2e484bol38lny2adh5rmk'
        print(f"search_id: {search_id}")

        results = []

        try:
            for i in range(page, pages + 1):
                # 搜索
                param = {
                    "keyword": ' '.join(keywords),
                    # "sort": "popularity_descending",
                    "offset": (i - 1) * 20,
                    "note_type": 0,
                    "search_id": search_id,
                }
                print(f"第{i}/{pages}页, {param}, 搜索开始")
                response = requests.get(f'{HOST}/xhs/search', params=param)
                print(response.json())
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json()['code'], 0)
                # self.assertGreater(len(response.json()['data']), 0)
                for note in response.json()["data"]:
                    result = copy.deepcopy(note)
                    result['keywords'] = ' '.join(keywords)
                    result = dict(sorted(result.items()))
                    results.append(result)
                # 保存到json文件中
                write_jsonlines(filepath, results)
                print(f"文件路径: {filepath}, result: {len(results)}")
                print(f"第{i}/{pages}页, {len(response.json()['data'])}条, 搜索结束")
                time.sleep(random.randint(3, 10))
        except Exception as e:
            print(f"搜索失败: {e}")
            raise e
        finally:
            print(f"搜索结束: {len(results)}条")
            write_jsonlines(filepath, results)
            print(f"文件路径: {filepath}, result: {len(results)}")
            return results

    # 合并去重
    def test_search_unique_merge(self, filepaths, unique_filepath):
        ids = set()
        unique_results = []

        for filepath in filepaths:
            results = read_jsonlines(filepath)
            print(f"filepath: {filepath}, result: {len(results)}")

            for result in results:
                if result['id'] not in ids:
                    ids.add(result['id'])
                    unique_results.append(result)

            write_jsonlines(unique_filepath, unique_results)
            print(f"filepath: {unique_filepath}, result: {len(unique_results)}")

        write_jsonlines(unique_filepath, unique_results)
        print(f"filepath: {unique_filepath}, result: {len(unique_results)}")

        return unique_results

    def test_search_job(self):
        # keywords = ['荨麻疹', '湿疹', '痤疮', '银屑病', '毛囊炎', '灰指甲', '水痘']
        keywords = ['荨麻疹']

        print("关键词: ", keywords, ' '.join(keywords))

        filepath = f'../result/search__{"_".join(keywords)}__{time.time()}.jsonl'
        print(f"文件路径: {filepath}")

        results = self.test_search(filepath, keywords, 1, 5)

        print(f"文件路径: {filepath}, result: {len(results)}")

        # 保存到json文件中，合并去重
        filepaths = [filepath]
        unique_filepath = filepath.replace('.jsonl', '__unique.jsonl')
        unique_results = self.test_search_unique_merge(filepaths, unique_filepath)

        print(f"文件路径: {unique_filepath}, result: {len(unique_results)}")

        # 笔记信息
        note_filepath = unique_filepath.replace('.jsonl', f'__note__{time.time()}.jsonl')
        note_results = self.test_note(note_filepath, unique_results)
        print(f"文件路径: {note_filepath}, result: {len(note_results)}")

    def test_search_unique(self):
        filepath = f'../result/search__宝妈__减脂__女__1734001263.812774.jsonl'
        filepaths = [filepath]
        unique_filepath = filepath.replace('.jsonl', '__unique.jsonl')
        self.test_search_unique_merge(filepaths, unique_filepath)

    def test_search_merge(self):
        filepaths = [
            f'../result/search__考研__减脂__女__1734325284.533468__unique.jsonl',
            f'../result/search__考研__减脂__女__1734332189.8059452__unique.jsonl',
        ]
        unique_filepath = f'../result/search__考研__减脂__女__{time.time()}__unique__merged.jsonl'
        self.test_search_unique_merge(filepaths, unique_filepath)

    def test_search_file_results(self):
        filepath = f'../result/search__宝妈__减脂__女__1734001263.812774__unique.jsonl'
        results = read_jsonlines(filepath)
        print(f"filepath: {filepath}, result: {len(results)}")

    # 笔记接口
    def test_note(self, filepath, notes: list[any]):
        # # 添加账户
        # data = {
        #     "id": "66f69f62000000001c00265a",
        #     "cookie": XHS_COOKIE
        # }
        # response = requests.post(f'{HOST}/xhs/add_account', json=data)
        # self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.json()['code'], 0)

        print(f"文件路径: {filepath}")
        print(f"笔记开始")

        results = []

        try:
            for index, note in enumerate(notes, start=1):
                if note["model_type"] == 'note':
                    try:
                        param = {
                            "id": note["id"],
                            "xsec_token": note["xsec_token"]
                        }
                        detail_url = f'https://www.xiaohongshu.com/explore/{note["id"]}?type=normal&xsec_token={note["xsec_token"].replace("=","")}=&xsec_source=pc_share&exSource='
                        print(f"第{index}/{len(notes)}条, 笔记开始: {detail_url}")
                        response = requests.get(f'{HOST}/xhs/detail', params=param)
                        print(response.json())
                        self.assertEqual(response.status_code, 200)
                        self.assertEqual(response.json()['code'], 0)
                        # self.assertGreater(len(response.json()['data']), 0)
                        result = copy.deepcopy(response.json()["data"])
                        # 笔记不存在|当前内容无法展示
                        if result == {}:
                            print(f"笔记不存在|当前内容无法展示")
                        else:
                            result['url'] = detail_url
                            result['keywords'] = note.get('keywords', None)
                            result = dict(sorted(result.items()))
                            results.append(result)
                        write_jsonlines(filepath, results)
                        print(f"文件路径: {filepath}, result: {len(results)}")
                        print(f"第{index}/{len(notes)}条, 笔记结束: {detail_url}")
                        time.sleep(random.randint(1, 10))
                    except Exception as e:
                        print(f"第{index}/{len(notes)}条, 笔记失败: {detail_url}")
                        raise e
                else:
                    print(f"第{index}/{len(notes)}条, 跳过非笔记类型: {note['model_type']}, {note['id']}")
                    continue
        except Exception as e:
            print(f"笔记失败: {e}")
            raise e
        finally:
            print(f"笔记结束")
            write_jsonlines(filepath, results)
            print(f"文件路径: {filepath}, result: {len(results)}")
            return results

    def test_note_unique_merge(self, filepaths, unique_filepath):
        ids = set()
        unique_results = []

        for filepath in filepaths:
            results = read_jsonlines(filepath)
            print(f"filepath: {filepath}, result: {len(results)}")

            for result in results:
                if result['note']['noteId'] not in ids:
                    ids.add(result['note']['noteId'])
                    unique_results.append(result)

            write_jsonlines(unique_filepath, unique_results)
            print(f"filepath: {unique_filepath}, result: {len(unique_results)}")

        write_jsonlines(unique_filepath, unique_results)
        print(f"filepath: {unique_filepath}, result: {len(unique_results)}")

        return unique_results

    def test_note_job(self):
        filepath = f'../result/search__荨麻疹__1749720904.211481__unique.jsonl'
        results = read_jsonlines(filepath)
        print(f"文件路径: {filepath}, result: {len(results)}")

        filepath = filepath.replace('.jsonl', f'__note__{time.time()}.jsonl')

        results = self.test_note(filepath, results)

        print(f"文件路径: {filepath}, result: {len(results)}")

    def test_note_unique(self):
        filepath = f'../result/search__宝妈__减脂__女__1734001263.812774__unique__note.jsonl'
        filepaths = [filepath]
        unique_filepath = filepath.replace('.jsonl', '__unique.jsonl')
        self.test_note_unique_merge(filepaths, unique_filepath)

    def test_note_merge(self):
        filepaths = [
            f'../result/search__律师__减肥__女__1734406505.440327__unique__note__1734406585.228847.jsonl',
            f'../result/search__律师__减肥__女__1734408201.775307__unique__note__1734408288.631787.jsonl',
            f'../result/search__律师__减肥__女__1734408201.775307__unique__note__1734410953.368926.jsonl',
        ]
        unique_filepath = f'../result/search__律师__减肥__女__{time.time()}__unique__note__unique__merged.jsonl'
        self.test_note_unique_merge(filepaths, unique_filepath)

    def test_note_file_results(self):
        filepath = f'../result/search__考研__减脂__女__1734325284.533468__unique__note__1734325364.1416771.jsonl'
        results = read_jsonlines(filepath)
        print(f"filepath: {filepath}, result: {len(results)}")

    # 用户接口
    def test_user(self):
        # 添加账户
        data = {
            "id": "66f69f62000000001c00265a",
            "cookie": XHS_COOKIE
        }
        response = requests.post(f'{HOST}/xhs/add_account', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)

        # 获取用户信息
        param = {
            "id": "5c25edc50000000007019f8c"
        }
        response = requests.get(f'{HOST}/xhs/user', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertNotEqual(response.json()['data']['user'], {})

        time.sleep(1)
        # 测试翻页 page_size = 10
        offset = 25
        limit = 5
        param = {
            "id": '5c25edc50000000007019f8c',
            "offset": offset,
            "limit": limit
        }
        response = requests.get(f'{HOST}/xhs/user', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertGreater(len(response.json()['data']['user']['notes']), 0)
        first_page = [note['note_id'] for note in response.json()['data']['user']['notes']]

        time.sleep(1)
        offset = 30
        limit = 5
        param = {
            "id": '5c25edc50000000007019f8c',
            "offset": offset,
            "limit": limit
        }
        response = requests.get(f'{HOST}/xhs/user', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertGreater(len(response.json()['data']['user']['notes']), 0)
        second_page = [note['note_id'] for note in response.json()['data']['user']['notes']]

        time.sleep(1)
        offset = 25
        limit = 10
        param = {
            "id": '5c25edc50000000007019f8c',
            "offset": offset,
            "limit": limit
        }
        response = requests.get(f'{HOST}/xhs/user', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertGreater(len(response.json()['data']['user']['notes']), 0)
        self.assertSequenceEqual([note['note_id'] for note in response.json()['data']['user']['notes']], first_page + second_page)

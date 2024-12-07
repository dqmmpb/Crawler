import copy
import random
import json

import execjs
import requests
from cookie import HOST, XHS_COOKIE
import unittest
import time
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
    def test_search(self, filepath, persona_keywords: list[str], pain_keywords: list[str], other_keywords: list[str], page: int = 1, pages: int = 10):
        # # 添加账户
        # data = {
        #     "id": "66f69f62000000001c00265a",
        #     "cookie": XHS_COOKIE
        # }
        # response = requests.post(f'{HOST}/xhs/add_account', json=data)
        # self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.json()['code'], 0)

        print(f'文件路径: {filepath}')
        print(f'搜索开始')

        # with open('../lib/js/xhs.js', encoding='utf-8') as f:
        #     xhs_sign_obj = execjs.compile(f.read())
        # search_id = xhs_sign_obj.call('searchId')
        search_id = None
        # search_id = '2e484bol38lny2adh5rmk'
        print(f'search_id: {search_id}')

        results = []

        try:
            for i in range(page, pages + 1):
                # 搜索
                param = {
                    "keyword": ' '.join(persona_keywords + pain_keywords + other_keywords),
                    # "sort": "popularity_descending",
                    "offset": (i - 1) * 20,
                    "note_type": 2,
                    "search_id": search_id,
                }
                print(f'第{i}/{pages}页, {param}, 搜索开始')
                response = requests.get(f'{HOST}/xhs/search', params=param)
                print(response.json())
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json()['code'], 0)
                # self.assertGreater(len(response.json()['data']), 0)
                for note in response.json()["data"]:
                    result = copy.deepcopy(note)
                    result['persona_keywords'] = ' '.join(persona_keywords)
                    result['pain_keywords'] = ' '.join(pain_keywords)
                    result['other_keywords'] = ' '.join(other_keywords)
                    results.append(result)
                # 保存到json文件中
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(results, f, ensure_ascii=False, indent=4)
                print(f'文件路径: {filepath}, result: {len(results)}')
                print(f'第{i}/{pages}页, {len(response.json()["data"])}条, 搜索结束')
                time.sleep(random.randint(3, 10))
        except Exception as e:
            print(f'搜索失败: {e}')
            raise e
        finally:
            print(f'搜索结束: {len(results)}条')
            # 保存到json文件中
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=4)
            print(f'文件路径: {filepath}, result: {len(results)}')
            return results

    # 合并去重
    def test_search_unique_merge(self, filepaths, unique_filepath):
        ids = set()
        unique_results = []

        for filepath in filepaths:
            with open(filepath, 'r', encoding='utf-8') as f:
                results = json.load(f)
            print(f'filepath: {filepath}, result: {len(results)}')

            for result in results:
                if result['id'] not in ids:
                    ids.add(result['id'])
                    unique_results.append(result)

            with open(unique_filepath, 'w', encoding='utf-8') as f:
                json.dump(unique_results, f, ensure_ascii=False, indent=4)
            print(f'filepath: {unique_filepath}, result: {len(unique_results)}')

        with open(unique_filepath, 'w', encoding='utf-8') as f:
            json.dump(unique_results, f, ensure_ascii=False, indent=4)
        print(f'filepath: {unique_filepath}, result: {len(unique_results)}')

        return unique_results

    def test_search_job(self):
        # persona_keywords = ['宝妈', '二胎', '一胎', '怀孕', '哺乳期', '月子', '考公', '考研', '教师', '老师', '律师', '新媒体', '运营', '博主', '经纪人', '编导', '模特', '化妆师']
        persona_keywords = ['律师']
        # pain_keywords = ['减脂', '减肥', '胖', '瘦', '长肉', '掉秤', '失眠', '睡不着', '惊醒', '睡不好', '脱发', '掉头发', '秃头', '生发']
        pain_keywords = ['减肥']
        other_keywords = ['女']

        print("人设关键词: ", persona_keywords, ' '.join(persona_keywords))
        print("痛点关键词: ", pain_keywords, ' '.join(pain_keywords))
        print("其他关键词: ", other_keywords, ' '.join(other_keywords))

        filepath = f'../result/search__{"_".join(persona_keywords)}__{"_".join(pain_keywords)}__{"_".join(other_keywords)}__{time.time()}.json'
        print(f'文件路径: {filepath}')

        results = self.test_search(filepath, persona_keywords, pain_keywords, other_keywords, 1, 10)

        print(f'文件路径: {filepath}, result: {len(results)}')

        # 保存到json文件中，合并去重
        filepaths = [filepath]
        unique_filepath = filepath.replace('.json', '__unique.json')
        unique_results = self.test_search_unique_merge(filepaths, unique_filepath)

        print(f'文件路径: {unique_filepath}, result: {len(unique_results)}')

        # 笔记信息
        note_filepath = unique_filepath.replace('.json', f'__note__{time.time()}.json')
        note_results = self.test_note(note_filepath, unique_results)
        print(f'文件路径: {note_filepath}, result: {len(note_results)}')

    def test_search_unique(self):
        filepath = f'../result/search__宝妈__减脂__女__1734001263.812774.json'
        filepaths = [filepath]
        unique_filepath = filepath.replace('.json', '__unique.json')
        self.test_search_unique_merge(filepaths, unique_filepath)

    def test_search_merge(self):
        filepaths = [
            f'../result/search__考研__减脂__女__1734325284.533468__unique.json',
            f'../result/search__考研__减脂__女__1734332189.8059452__unique.json',
        ]
        unique_filepath = f'../result/search__考研__减脂__女__{time.time()}__unique__merged.json'
        self.test_search_unique_merge(filepaths, unique_filepath)

    def test_search_file_results(self):
        filepath = f'../result/search__宝妈__减脂__女__1734001263.812774__unique.json'
        with open(filepath, 'r', encoding='utf-8') as f:
            results = json.load(f)
        print(f'filepath: {filepath}, result: {len(results)}')

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

        print(f'文件路径: {filepath}')
        print(f'笔记开始')

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
                        print(f'第{index}/{len(notes)}条, 笔记开始: {detail_url}')
                        response = requests.get(f'{HOST}/xhs/detail', params=param)
                        print(response.json())
                        self.assertEqual(response.status_code, 200)
                        self.assertEqual(response.json()['code'], 0)
                        # self.assertGreater(len(response.json()['data']), 0)
                        result = copy.deepcopy(response.json()["data"])
                        # 笔记不存在|当前内容无法展示
                        if result == {}:
                            print(f'笔记不存在|当前内容无法展示')
                        else:
                            result['url'] = detail_url
                            result['persona_keywords'] = note.get('persona_keywords', None)
                            result['pain_keywords'] = note.get('pain_keywords', None)
                            result['other_keywords'] = note.get('other_keywords', None)
                            results.append(result)
                        # 保存到json文件中
                        with open(filepath, 'w', encoding='utf-8') as f:
                            json.dump(results, f, ensure_ascii=False, indent=4)
                        print(f'文件路径: {filepath}, result: {len(results)}')
                        print(f'第{index}/{len(notes)}条, 笔记结束: {detail_url}')
                        time.sleep(random.randint(1, 10))
                    except Exception as e:
                        print(f'第{index}/{len(notes)}条, 笔记失败: {detail_url}')
                        raise e
        except Exception as e:
            print(f'笔记失败: {e}')
            raise e
        finally:
            print(f'笔记结束')
            # 保存到json文件中
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=4)
            print(f'文件路径: {filepath}, result: {len(results)}')
            return results

    def test_note_unique_merge(self, filepaths, unique_filepath):
        ids = set()
        unique_results = []

        for filepath in filepaths:
            with open(filepath, 'r', encoding='utf-8') as f:
                results = json.load(f)
            print(f'filepath: {filepath}, result: {len(results)}')

            for result in results:
                if result['note']['noteId'] not in ids:
                    ids.add(result['note']['noteId'])
                    unique_results.append(result)

            with open(unique_filepath, 'w', encoding='utf-8') as f:
                json.dump(unique_results, f, ensure_ascii=False, indent=4)
            print(f'filepath: {unique_filepath}, result: {len(unique_results)}')

        with open(unique_filepath, 'w', encoding='utf-8') as f:
            json.dump(unique_results, f, ensure_ascii=False, indent=4)
        print(f'filepath: {unique_filepath}, result: {len(unique_results)}')

        return unique_results

    def test_note_job(self):
        # # 添加账户
        # data = {
        #     "id": "66f69f62000000001c00265a",
        #     "cookie": XHS_COOKIE
        # }
        # response = requests.post(f'{HOST}/xhs/add_account', json=data)
        # self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.json()['code'], 0)

        filepath = f'../result/search__律师__减肥__女__1734408201.775307__unique.json'
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f'文件路径: {filepath}, result: {len(data)}')

        filepath = filepath.replace('.json', f'__note__{time.time()}.json')

        results = self.test_note(filepath, data)

        print(f'文件路径: {filepath}, result: {len(results)}')

    def test_note_unique(self):
        filepath = f'../result/search__宝妈__减脂__女__1734001263.812774__unique__note.json'
        filepaths = [filepath]
        unique_filepath = filepath.replace('.json', '__unique.json')
        self.test_note_unique_merge(filepaths, unique_filepath)

    def test_note_merge(self):
        filepaths = [
            f'../result/search__律师__减肥__女__1734406505.440327__unique__note__1734406585.228847.json',
            f'../result/search__律师__减肥__女__1734408201.775307__unique__note__1734408288.631787.json',
            f'../result/search__律师__减肥__女__1734408201.775307__unique__note__1734410953.368926.json',
        ]
        unique_filepath = f'../result/search__律师__减肥__女__{time.time()}__unique__note__unique__merged.json'
        self.test_note_unique_merge(filepaths, unique_filepath)

    def test_note_file_results(self):
        filepath = f'../result/search__考研__减脂__女__1734325284.533468__unique__note__1734325364.1416771.json'
        with open(filepath, 'r', encoding='utf-8') as f:
            results = json.load(f)
        print(f'filepath: {filepath}, result: {len(results)}')

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

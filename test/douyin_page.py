import copy
import random

import requests
from cookie import HOST, DY_COOKIE
import unittest
import time

from utils import write_jsonlines, read_jsonlines, ensure_dir


class TestModule(unittest.TestCase):
    # 添加账户接口
    def test_add_account(self):
        data = {
            "id": "test",
            "cookie": DY_COOKIE
        }
        response = requests.post(f'{HOST}/douyin/add_account', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)

    # 账户列表接口
    def test_account_list(self):
        # 添加账户
        data = {
            "id": "test",
            "cookie": DY_COOKIE
        }
        response = requests.post(f'{HOST}/douyin/add_account', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)

        # 获取账户列表
        response = requests.get(f'{HOST}/douyin/account_list')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertGreater(len(response.json()['data']), 0)

    # 过期账户接口
    def test_expire_account(self):
        # 添加账户
        data = {
            "id": "test",
            "cookie": DY_COOKIE
        }
        response = requests.post(f'{HOST}/douyin/add_account', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)

        # 过期账户
        data = {
            "id": "test",
        }
        response = requests.post(f'{HOST}/douyin/expire_account', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)

    # 获取详情接口
    def test_detail(self):
        # 添加账户
        data = {
            "id": "test",
            "cookie": DY_COOKIE
        }
        response = requests.post(f'{HOST}/douyin/add_account', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)

        # 获取详情
        param = {
            "id": '6911683747733671175'
        }
        response = requests.get(f'{HOST}/douyin/detail', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertEqual(response.json()['data']['aweme_id'], param['id'])

    # 获取评论接口
    def test_comments(self):
        # 添加账户
        data = {
            "id": "test",
            "cookie": DY_COOKIE
        }
        response = requests.post(f'{HOST}/douyin/add_account', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)

        # 获取评论
        param = {
            "id": '6911683747733671175'    # 抖音官方视频
        }
        response = requests.get(f'{HOST}/douyin/comments', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertGreater(len(response.json()['data']['comments']), 0)

        time.sleep(1)
        # 测试翻页 page_size = 20
        offset = 55
        limit = 5
        param = {
            "id": '6911683747733671175',   # 抖音官方视频
            "offset": offset,
            "limit": limit
        }
        response = requests.get(f'{HOST}/douyin/comments', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertGreater(len(response.json()['data']['comments']), 0)
        first_page = [comment['cid'] for comment in response.json()['data']['comments']]

        time.sleep(1)
        offset = 60
        limit = 5
        param = {
            "id": '6911683747733671175',   # 抖音官方视频
            "offset": offset,
            "limit": limit
        }
        response = requests.get(f'{HOST}/douyin/comments', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertGreater(len(response.json()['data']['comments']), 0)
        second_page = [comment['cid'] for comment in response.json()['data']['comments']]

        time.sleep(1)
        offset = 55
        limit = 10
        param = {
            "id": '6911683747733671175',   # 抖音官方视频
            "offset": offset,
            "limit": limit
        }
        response = requests.get(f'{HOST}/douyin/comments', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertGreater(len(response.json()['data']['comments']), 0)
        self.assertSequenceEqual([comment['cid'] for comment in response.json()['data']['comments']], first_page + second_page)

    # 获取评论回复接口
    def test_reply(self):
        # 添加账户
        data = {
            "id": "test",
            "cookie": DY_COOKIE
        }
        response = requests.post(f'{HOST}/douyin/add_account', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)

        # 获取评论回复
        param = {
            "id": '6911683747733671175', # 抖音官方视频
            "comment_id": '6912088044888031236'
        }
        response = requests.get(f'{HOST}/douyin/replys', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertGreater(len(response.json()['data']['comments']), 0)

        time.sleep(1)
        # 测试翻页 page_size = 20
        offset = 5
        limit = 5
        param = {
            "id": '6911683747733671175',   # 抖音官方视频
            "comment_id": '6912088044888031236',
            "offset": offset,
            "limit": limit
        }
        response = requests.get(f'{HOST}/douyin/replys', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertGreater(len(response.json()['data']['comments']), 0)
        first_page = [comment['cid'] for comment in response.json()['data']['comments']]

        time.sleep(1)
        offset = 10
        limit = 5
        param = {
            "id": '6911683747733671175',   # 抖音官方视频
            "comment_id": '6912088044888031236',
            "offset": offset,
            "limit": limit
        }
        response = requests.get(f'{HOST}/douyin/replys', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertGreater(len(response.json()['data']['comments']), 0)
        second_page = [comment['cid'] for comment in response.json()['data']['comments']]

        time.sleep(1)
        offset = 5
        limit = 10
        param = {
            "id": '6911683747733671175',   # 抖音官方视频
            "comment_id": '6912088044888031236',
            "offset": offset,
            "limit": limit
        }
        response = requests.get(f'{HOST}/douyin/replys', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertGreater(len(response.json()['data']['comments']), 0)
        self.assertSequenceEqual([comment['cid'] for comment in response.json()['data']['comments']], first_page + second_page)

    # 搜索接口
    def test_search(self, filepath, keywords: list[str], page: int = 1, pages: int = 10, page_size: int = 10):
        # # 添加账户
        # data = {
        #     "id": "test",
        #     "cookie": DY_COOKIE
        # }
        # response = requests.post(f'{HOST}/douyin/add_account', json=data)
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
                    "offset": (i - 1) * page_size,
                    "limit": page_size,
                    "sort_type": 0,
                    "content_type": 0,
                    "search_id": search_id,
                }
                print(f"第{i}/{pages}页, {param}, 搜索开始")
                response = requests.get(f'{HOST}/douyin/search', params=param)
                print(response.json())
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json()['code'], 0)
                # self.assertGreater(len(response.json()['data']), 0)
                search_id = response.json()["search_id"] if search_id is None else search_id
                for detail in response.json()["data"]:
                    result = copy.deepcopy(detail)
                    result['keywords'] = ' '.join(keywords)
                    result = dict(sorted(result.items()))
                    results.append(result)
                # 保存到json文件中
                ensure_dir(filepath)
                write_jsonlines(filepath, results)
                print(f"文件路径: {filepath}, result: {len(results)}")
                print(f"第{i}/{pages}页, {len(response.json()['data'])}条, 搜索结束")
                time.sleep(random.randint(3, 10))
        except Exception as e:
            print(f"搜索失败: {e}")
            raise e
        finally:
            print(f"搜索结束: {len(results)}条")
            ensure_dir(filepath)
            write_jsonlines(filepath, results)
            print(f"文件路径: {filepath}, result: {len(results)}")
            return results

    def test_search_job(self):
        # keywords = ['荨麻疹', '湿疹', '痤疮', '银屑病', '毛囊炎', '灰指甲', '水痘']
        # keywords = ['荨麻疹']
        keywords = ['佳荔']

        print("关键词: ", keywords, ' '.join(keywords))

        filepath = f'../result/douyin/search__{"_".join(keywords)}__{time.time()}.jsonl'
        print(f"文件路径: {filepath}")

        results = self.test_search(filepath, keywords, 1, 10, 10)

        print(f"文件路径: {filepath}, result: {len(results)}")

        # # 保存到json文件中，合并去重
        # filepaths = [filepath]
        # unique_filepath = filepath.replace('.jsonl', '__unique.jsonl')
        # unique_results = self.test_search_unique_merge(filepaths, unique_filepath)
        #
        # print(f"文件路径: {unique_filepath}, result: {len(unique_results)}")
        #
        # # 详情信息
        # detail_filepath = unique_filepath.replace('.jsonl', f'__detail__{time.time()}.jsonl')
        # detail_results = self.test_detail(detail_filepath, unique_results)
        # print(f"文件路径: {detail_filepath}, result: {len(detail_results)}")

    # 合并去重
    def test_search_unique_merge(self, filepaths, unique_filepath):
        ids = set()
        unique_results = []

        for filepath in filepaths:
            results = read_jsonlines(filepath)
            print(f"filepath: {filepath}, result: {len(results)}")

            for result in results:
                if "aweme_info" in result:
                    if result['aweme_info']['aweme_id'] not in ids:
                        ids.add(result['aweme_info']['aweme_id'])
                        unique_results.append(result)

            ensure_dir(unique_filepath)
            write_jsonlines(unique_filepath, unique_results)
            print(f"filepath: {unique_filepath}, result: {len(unique_results)}")

        ensure_dir(unique_filepath)
        write_jsonlines(unique_filepath, unique_results)
        print(f"filepath: {unique_filepath}, result: {len(unique_results)}")

        return unique_results

    def test_search_unique(self):
        # filepath = f'../result/douyin/search__荨麻疹__1749801171.7424262.jsonl'
        filepath = f'../result/douyin/search__佳荔__1749820493.9978392.jsonl'
        filepaths = [filepath]
        unique_filepath = filepath.replace('.jsonl', '__unique.jsonl')
        self.test_search_unique_merge(filepaths, unique_filepath)

    def test_search_merge(self):
        filepaths = [
            f'../result/douyin/search__考研__减脂__女__1734325284.533468__unique.jsonl',
            f'../result/douyin/search__考研__减脂__女__1734332189.8059452__unique.jsonl',
        ]
        unique_filepath = f'../result/douyin/search__考研__减脂__女__{time.time()}__unique__merged.jsonl'
        self.test_search_unique_merge(filepaths, unique_filepath)

    def test_search_file_results(self):
        filepath = f'../result/douyin/search__宝妈__减脂__女__1734001263.812774__unique.jsonl'
        results = read_jsonlines(filepath)
        print(f"filepath: {filepath}, result: {len(results)}")

    # 详情接口
    def test_detail_list(self, filepath, awemes: list[any]):
        # # 添加账户
        # data = {
        #     "id": "66f69f62000000001c00265a",
        #     "cookie": DY_COOKIE
        # }
        # response = requests.post(f'{HOST}/xhs/add_account', json=data)
        # self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.json()['code'], 0)

        print(f"文件路径: {filepath}")
        print(f"详情开始")

        results = []

        try:
            for index, aweme in enumerate(awemes, start=1):
                if "aweme_info" in aweme:
                    try:
                        param = {
                            "id": aweme['aweme_info']['aweme_id'],    # 抖音官方视频
                        }
                        if aweme['aweme_info']['media_type'] == 4:
                            detail_url = f'https://www.douyin.com/video/{aweme["aweme_info"]["aweme_id"]}'
                        elif aweme['aweme_info']['media_type'] == 2:
                            detail_url = f'https://www.douyin.com/note/{aweme["aweme_info"]["aweme_id"]}'

                        print(f"第{index}/{len(awemes)}条, 详情开始: {detail_url}")
                        response = requests.get(f'{HOST}/douyin/detail', params=param)
                        print(response.json())
                        self.assertEqual(response.status_code, 200)
                        self.assertEqual(response.json()['code'], 0)
                        # self.assertGreater(len(response.json()['data']), 0)
                        result = copy.deepcopy(response.json()["data"])
                        # 详情不存在|当前内容无法展示
                        if result == {}:
                            print(f"详情不存在|当前内容无法展示")
                        else:
                            result['url'] = detail_url
                            result['keywords'] = aweme.get('keywords', None)
                            result = dict(sorted(result.items()))
                            results.append(result)
                        ensure_dir(filepath)
                        write_jsonlines(filepath, results)
                        print(f"文件路径: {filepath}, result: {len(results)}")
                        print(f"第{index}/{len(awemes)}条, 详情结束: {detail_url}")
                        time.sleep(random.randint(1, 10))
                    except Exception as e:
                        print(f"第{index}/{len(awemes)}条, 详情失败: {detail_url}")
                        raise e
                else:
                    print(f"第{index}/{len(awemes)}条, 跳过非详情类型: {aweme['model_type']}, {aweme['id']}")
                    continue
        except Exception as e:
            print(f"详情失败: {e}")
            raise e
        finally:
            print(f"详情结束")
            ensure_dir(filepath)
            write_jsonlines(filepath, results)
            print(f"文件路径: {filepath}, result: {len(results)}")
            return results

    def test_detail_job(self):
        # filepath = f'../result/douyin/search__荨麻疹__1749801171.7424262__unique.jsonl'
        filepath = f'../result/douyin/search__佳荔__1749820493.9978392__unique.jsonl'
        results = read_jsonlines(filepath)
        print(f"文件路径: {filepath}, result: {len(results)}")

        filepath = filepath.replace('.jsonl', f'__detail__{time.time()}.jsonl')

        results = self.test_detail_list(filepath, results)

        print(f"文件路径: {filepath}, result: {len(results)}")

    def test_detail_unique_merge(self, filepaths, unique_filepath):
        ids = set()
        unique_results = []

        for filepath in filepaths:
            results = read_jsonlines(filepath)
            print(f"filepath: {filepath}, result: {len(results)}")

            for result in results:
                if result['note']['noteId'] not in ids:
                    ids.add(result['note']['noteId'])
                    unique_results.append(result)

            ensure_dir(unique_filepath)
            write_jsonlines(unique_filepath, unique_results)
            print(f"filepath: {unique_filepath}, result: {len(unique_results)}")

        ensure_dir(unique_filepath)
        write_jsonlines(unique_filepath, unique_results)
        print(f"filepath: {unique_filepath}, result: {len(unique_results)}")

        return unique_results

    def test_detail_unique(self):
        filepath = f'../result/douyin/search__宝妈__减脂__女__1734001263.812774__unique__detail.jsonl'
        filepaths = [filepath]
        unique_filepath = filepath.replace('.jsonl', '__unique.jsonl')
        self.test_detail_unique_merge(filepaths, unique_filepath)

    def test_detail_merge(self):
        filepaths = [
            f'../result/douyin/search__律师__减肥__女__1734406505.440327__unique__detail__1734406585.228847.jsonl',
            f'../result/douyin/search__律师__减肥__女__1734408201.775307__unique__detail__1734408288.631787.jsonl',
            f'../result/douyin/search__律师__减肥__女__1734408201.775307__unique__detail__1734410953.368926.jsonl',
        ]
        unique_filepath = f'../result/douyin/search__律师__减肥__女__{time.time()}__unique__detail__unique__merged.jsonl'
        self.test_detail_unique_merge(filepaths, unique_filepath)

    def test_detail_file_results(self):
        filepath = f'../result/douyin/search__考研__减脂__女__1734325284.533468__unique__detail__1734325364.1416771.jsonl'
        results = read_jsonlines(filepath)
        print(f"filepath: {filepath}, result: {len(results)}")

    # 用户接口
    def test_user(self):
        # 添加账户
        data = {
            "id": "test",
            "cookie": DY_COOKIE
        }
        response = requests.post(f'{HOST}/douyin/add_account', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)

        # 获取用户信息
        param = {
            "id": "MS4wLjABAAAA3y0gs9xhygmvZhVEHWt5Y4aLHi9KooKSNxVQ2pslu10"    # 抖音官方账号
        }
        response = requests.get(f'{HOST}/douyin/user', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertNotEqual(response.json()['data']['user'], {})

        time.sleep(1)
        # 测试翻页 page_size = 10
        offset = 25
        limit = 5
        param = {
            "id": 'MS4wLjABAAAA3y0gs9xhygmvZhVEHWt5Y4aLHi9KooKSNxVQ2pslu10',   # 抖音官方账号
            "offset": offset,
            "limit": limit
        }
        response = requests.get(f'{HOST}/douyin/user', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertGreater(len(response.json()['data']['aweme_list']), 0)
        first_page = [aweme['aweme_id'] for aweme in response.json()['data']['aweme_list']]

        time.sleep(1)
        offset = 30
        limit = 5
        param = {
            "id": 'MS4wLjABAAAA3y0gs9xhygmvZhVEHWt5Y4aLHi9KooKSNxVQ2pslu10',   # 抖音官方账号
            "offset": offset,
            "limit": limit
        }
        response = requests.get(f'{HOST}/douyin/user', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertGreater(len(response.json()['data']['aweme_list']), 0)
        second_page = [aweme['aweme_id'] for aweme in response.json()['data']['aweme_list']]

        time.sleep(1)
        offset = 25
        limit = 10
        param = {
            "id": 'MS4wLjABAAAA3y0gs9xhygmvZhVEHWt5Y4aLHi9KooKSNxVQ2pslu10',   # 抖音官方账号
            "offset": offset,
            "limit": limit
        }
        response = requests.get(f'{HOST}/douyin/user', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertGreater(len(response.json()['data']['aweme_list']), 0)
        self.assertSequenceEqual([aweme['aweme_id'] for aweme in response.json()['data']['aweme_list']], first_page + second_page)

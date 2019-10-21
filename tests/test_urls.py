import unittest
import requests
import importlib
import os
import warnings
import sys

TO_SKIP = ['./parlai/tasks/taskntalk', './parlai/tasks/cnn_dm', './parlai/tasks/woz']

GOOGLE = [
    './parlai/tasks/dialogue_nli',
    './parlai/tasks/qacnn',
    './parlai/tasks/qangaroo',
    './parlai/tasks/qadailymail',
]


class TestUtils(unittest.TestCase):
    def test_http_response(self):
        sys.path.insert(0, './lib')
        tasks = [f.path for f in os.scandir('./parlai/tasks') if f.is_dir()]
        for task in tasks:
            if task in TO_SKIP or task in GOOGLE:
                continue
            if 'build.py' in os.listdir(task):
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", ResourceWarning)
                    warnings.simplefilter("ignore", DeprecationWarning)
                    mod = importlib.import_module(
                        (task[2:].replace('/', '.') + '.build')
                    )
                    for url in mod.URLS:
                        with self.subTest(f"{task}: {url}"):
                            session = requests.Session()
                            headers = {
                                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
                            }
                            header = session.head(
                                url, allow_redirects=True, headers=headers
                            )
                            status = header.status_code
                            session.close()
                            self.assertEqual(status, 200)


if __name__ == '__main__':
    unittest.main()

#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import os

from parlai.core import build_data

URLS = ['https://drive.google.com/uc?export=download&id=0B2MvoQfXtqZmMTJqclpBdGN2bmc']
FILE_NAMES = ['dialog-bAbI-plus.zip']
SHA256 = ['e67dfecbde5e6250833143a6148150a313204237b765d39e7b8ebc111cb3204e']


def build(opt):
    dpath = os.path.join(opt['datapath'], 'dialog-bAbI-plus')
    version = None

    if not build_data.built(dpath, version_string=version):
        print('[building data: ' + dpath + ']')
        if build_data.built(dpath):
            # An older version exists, so remove these outdated files.
            build_data.remove_dir(dpath)
        build_data.make_dir(dpath)

        build_data.download_check(dpath, URLS, FILE_NAMES, SHA256)

        for zipfile in FILE_NAMES:
            build_data.untar(dpath, zipfile)

        build_data.mark_done(dpath, version)

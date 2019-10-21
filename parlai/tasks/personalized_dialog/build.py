#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
# Download and build the data if it does not exist.

import parlai.core.build_data as build_data
import os

URLS = [
    'https://www.dropbox.com/s/4i9u4y24pt3paba/'
    + 'personalized-dialog-dataset.tar.gz'
    + '?dl=1'
]
FILE_NAMES = ['personalized-dialog-dataset.tar.gz']
SHA256 = ['0da3d5ba631d672e9e2d108dfd6721c8201cc41b837425540faba6815c375c52']


def build(opt):
    dpath = os.path.join(opt['datapath'], 'personalized-dialog')
    version = None

    if not build_data.built(dpath, version_string=version):
        print('[building data: ' + dpath + ']')
        if build_data.built(dpath):
            # An older version exists, so remove these outdated files.
            build_data.remove_dir(dpath)
        build_data.make_dir(dpath)

        # Download the data.
        build_data.download_check(dpath, URLS, FILE_NAMES, SHA256)

        for zipfile in FILE_NAMES:
            build_data.untar(dpath, zipfile)

        # Mark the data as built.
        build_data.mark_done(dpath, version_string=version)

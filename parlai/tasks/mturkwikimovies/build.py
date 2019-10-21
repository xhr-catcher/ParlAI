#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
# Download and build the data if it does not exist.

import parlai.core.build_data as build_data
import parlai.tasks.wikimovies.build as wikimovies_build
import os

URLS = ['http://parl.ai/downloads/mturkwikimovies/' + 'mturkwikimovies.tar.gz']
FILE_NAMES = ['mturkwikimovies.tar.gz']
SHA256 = ['41a85a17e813bfecd975d448f9a08178f65aba32fc10eaa1a48c0bed65431361']


def build(opt):
    # Depends upon another dataset, wikimovies, build that first.
    wikimovies_build.build(opt)

    dpath = os.path.join(opt['datapath'], 'MTurkWikiMovies')
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

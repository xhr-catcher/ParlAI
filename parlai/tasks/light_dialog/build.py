#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import parlai.core.build_data as build_data
import os
from parlai.tasks.light_dialog.builder import build_from_db

URLS = [
    'http://parl.ai/downloads/light/light-dialog-processed-small7.pkl',
    'http://parl.ai/downloads/light/light-unseen-processed2.pkl',
    'http://parl.ai/downloads/light/light-environment.pkl',
]
FILE_NAMES = ['light_data.pkl', 'light_unseen_data.pkl', 'light_environment.pkl']
SHA256 = [
    '7c83cf49818586db9999ea67a4a6ad087afbd91c26ed629a9f00e21d0b84058f',
    '489b98d08dd94eaf1ba95439d04200ccc54623ade056839f87a5c4207bc5699c',
    '162389202f22063e1c32af7f9261aac13d20fc05598388d1e9748735996ec016',
]


def download(opt):
    version = 'v2.03'
    # download pickled database
    dpath = os.path.join(opt['datapath'], 'light_dialogue')
    if not build_data.built(dpath, version):
        print('[building data: ' + dpath + ']')
        if build_data.built(dpath):
            # An older version exists, so remove these outdated files.
            build_data.remove_dir(dpath)
        build_data.make_dir(dpath)
        # Download the data.
        build_data.download_check(dpath, URLS, FILE_NAMES, SHA256)

        # Mark the data as built.
        build_data.mark_done(dpath, version)

    return dpath, version


def build(opt):
    dpath, version = download(opt)

    # create particular instance of dataset depending on flags..
    fields = [
        'setting',
        'objects',
        'person_names',
        'persona',
        'emote',
        'speech',
        'action',
        'affordances',
        'repeat',
        'cands',
        'current_self_output',
        'clip_cands',
    ]
    fpath = ''
    for f in fields:
        fpath += f + str(opt['light_use_' + f]) + "_"
    dpath2 = os.path.join(opt['datapath'], 'light_dialogue', fpath[:-1])
    if not build_data.built(dpath2, version):
        if build_data.built(dpath2):
            # An older version exists, so remove these outdated files.
            build_data.remove_dir(dpath2)
        build_data.make_dir(dpath2)
        fname = 'light_data.pkl'
        fname2 = 'light_unseen_data.pkl'
        build_from_db(opt, dpath, dpath2, fname, fname2)
        # Mark the data as built.
        build_data.mark_done(dpath2, version)

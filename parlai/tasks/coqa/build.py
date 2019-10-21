#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
# Download and build the data if it does not exist.

import parlai.core.build_data as build_data
import os
import json

VERSION = '1.0'
URLS = [
    'https://nlp.stanford.edu/data/coqa/coqa-train-v1.0.json',
    'https://nlp.stanford.edu/data/coqa/coqa-dev-v1.0.json',
]
FILE_NAMES = ['coqa-train-v1.0.json', 'coqa-dev-v1.0.json']
SHA256 = []


def make_parlai_format(outpath, dtype, data):
    print('building parlai:' + dtype)
    with open(os.path.join(outpath, dtype + '.txt'), 'w') as fout:
        for each in data:
            output = []
            story = each['story'].replace('\n', '\\n')
            for question, ans in zip(each['questions'], each['answers']):
                question_txt = ''
                if question['turn_id'] == 1:
                    # include the context in the very first turn
                    question_txt = story + '\\n' + question['input_text']
                else:
                    question_txt = question['input_text']
                output.append(
                    'text:{question}\tlabels:{labels}'.format(
                        question=question_txt,
                        labels=ans['input_text'].replace('|', ' __PIPE__ '),
                    )
                )
                if question['turn_id'] < len(each['questions']):
                    output.append('\n')
            output.append('\t\tepisode_done:True\n')
            fout.write(''.join(output))


def build(opt):
    dpath = os.path.join(opt['datapath'], 'CoQA')
    version = VERSION

    if not build_data.built(dpath, version_string=version):
        print('[building data: ' + dpath + ']')
        if build_data.built(dpath):
            # An older version exists, so remove these outdated files.
            build_data.remove_dir(dpath)
        build_data.make_dir(dpath)

        # Download the data.
        build_data.download_check(dpath, URLS, FILE_NAMES, SHA256)

        with open(os.path.join(dpath, 'coqa-train-v1.0.json')) as f:
            data = json.load(f)['data']
            make_parlai_format(dpath, 'train', data)

        with open(os.path.join(dpath, 'coqa-dev-v1.0.json')) as f:
            data = json.load(f)['data']
            make_parlai_format(dpath, 'valid', data)

        # Mark the data as built.
        build_data.mark_done(dpath, version_string=version)

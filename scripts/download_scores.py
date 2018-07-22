#!/usr/bin/env python3

"""
Modified from example download script by
Eelco van der Wel and sebasgverde
"""

import json
import os
import shutil
import urllib.request

data_dir = '../data'
api_key = '../data/musescore_api_key'
score_json_url = 'http://api.musescore.com/services/rest/score/{}.json?oauth_consumer_key='
score_file_url = 'http://static.musescore.com/{}/{}/score'
datasets = ['train', 'validation', 'evaluation']
# Valid filetypes are pdf, mid, mxl, mscz, mp3
# Interestingly, mxl (compressed xml) seems to be smaller than mscz (compressed musescore)
filetypes = ['mxl']
# for download safety
tmpdir = '../data/tmpdir'

def download_dataset(dataset_name):
    # Read score ids
    with open(os.path.join(data_dir, dataset_name + '_keys.txt'), 'r') as f:
        score_ids = f.read().splitlines()

    failed_ids = []
    os.makedirs(tmpdir, exist_ok=True)
    for index, score_id in enumerate(score_ids):
        print('downloading %s id %s (%d / %d)' % (dataset_name, score_id, index, len(score_ids)))

        score_dir = os.path.join(data_dir, dataset_name, score_id)
        os.makedirs(score_dir, exist_ok=True)

        downloaded = [os.path.isfile(os.path.join(score_dir, score_id + '.' + filetype)) for filetype in filetypes]

        if all (downloaded):
            print('already downloaded')
            continue

        try:
            # First download score JSON to get secret
            r = urllib.request.urlopen(score_json_url.format(score_id))
            score_json = json.loads(r.read().decode(r.info().get_param('charset') or 'utf-8'))
            score_secret = score_json['secret']

            for idx, filetype in enumerate(filetypes):
                if not downloaded[idx]:
                    extension = '.' + filetype
                    file_url = score_file_url + extension
                    tmpfile = os.path.join(tmpdir, score_id + extension)
                    urllib.request.urlretrieve(file_url.format(score_id, score_secret), tmpfile)
                    shutil.move(tmpfile, score_dir)
        except:
            # Some scores are now protected from when original dataset was produced
            print('failed to download')
            os.rmdir(score_dir)
            failed_ids.append(score_id)

    if failed_ids:
        with open(os.path.join(data_dir, dataset_name, 'failed.txt'), 'w') as f:
            f.write('\n'.join(failed_ids))

    print('Downloaded %d / %d ids' % (len(score_ids) - len(failed_ids), len(score_ids)))

if __name__ == '__main__':
    # Read api key from file
    with open(api_key, 'r') as myfile:
        api_key = myfile.read()
    assert api_key != '', 'Failed to read api key from ' + data_dir

    # We need to download 2 components:
    # - a json with the score information, containing the secret id
    # - score files, using the public and secret id
    score_json_url += api_key

    for dataset in datasets:
        download_dataset(dataset)

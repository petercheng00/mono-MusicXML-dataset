"""
An example of how to use the MuseScore API
with the MuseScore Monophonic MusicXML dataset.

Author: Eelco van der Wel
Date: April 2017
"""

import urllib.request
import json
import os
import pickle

def download_folder(folder_name):
    general_string = ''

    if not os.path.exists(folder_name):
        # os.makedirs(folder_name)
        os.makedirs(folder_name + '/midi')
        os.makedirs(folder_name + '/musicxml')

    # Read train id's
    with open('../data/' + folder_name + '_keys.txt', 'r') as f:
        train_ids = f.read().splitlines()

    # We download the first score
    for score_id in train_ids:
        # score_id = train_ids[0]
        print('downloading id:', score_id)

        try:
            # First download score JSON to get secret
            r = urllib.request.urlopen(score_json_url.format(score_id))
            score_json = json.loads(r.read().decode(r.info().get_param('charset') or 'utf-8'))
            score_secret = score_json['secret']

            # Define save location
            filename = './' + folder_name + '/musicxml/{}.mxl'.format(score_id)
            # Download score
            urllib.request.urlretrieve(score_file_url.format(score_id, score_secret),
                                       filename)
            
            filename = './' + folder_name + '/midi/{}.mid'.format(score_id)
            # Download score
            urllib.request.urlretrieve(score_file_midi_url.format(score_id, score_secret),
                                       filename)
        except:
            general_string += score_id + '\n'

    # with open(folder_name+'.pickle', 'wb') as handle:
    #     pickle.dump(general_string, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open(folder_name+'_protected.txt', 'w') as file:
        file.write(general_string)

    print("Done!")    

if __name__ == "__main__":
    # **Define your API key here**
    api_key = ''
    assert api_key != '', 'Define your API key first.'

    # We need to download 2 components: 
    # - a json with the score information, containing the secret id
    # - the score mxl file, using the public and secret id
    score_json_url = 'http://api.musescore.com/services/rest/score/{}.json?oauth_consumer_key='
    score_json_url += api_key
    score_file_url = 'http://static.musescore.com/{}/{}/score.mxl'
    # http://developers.musescore.com/
    # {id}/{secret}/score.{extension} Where extension can be anything in pdf, mid (General MIDI), 
    # mxl (Compressed MusicXML), mscz (MuseScore file), mp3.
    score_file_midi_url = 'http://static.musescore.com/{}/{}/score.mid'


    download_folder('train')
    download_folder('evaluation')
    download_folder('validation')

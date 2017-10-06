#!/bin/bash
# it test if the three floders have the same files with different extension
# if correct shouldn't show nothing

ls -1 compressedmusicxml| sed -e 's/\.mxl$//' > list_compressed_music.txt
ls -1 midi/| sed -e 's/\.mid$//' > list_midi.txt
ls -1 musescore/| sed -e 's/\.mscz$//' > list_musescore.txt
diff list_compressed_music.txt list_midi.txt 
diff list_compressed_music.txt list_musescore.txt 
diff list_midi.txt list_musescore.txt 

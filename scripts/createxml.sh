#!/bin/bash
mkdir musicxml
for file in musescore/*.mscz; do
	musescore "$file" -o "musicxml/$(basename "$file" .mscz).xml"
done

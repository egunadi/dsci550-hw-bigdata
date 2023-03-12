# convert pixstory_final.tsv to ../aggregate-json/aggregate.json
tsvtojson -t ../../data/pixstory/pixstory_final.tsv -j ../aggregate-json/aggregate.json -c ../conf/colheaders.conf -o pixstoryposts -e ../conf/encoding.conf -s 0.8 -v

# split ../aggregate-json/aggregate.json up into individual JSON files.
repackage -j ../aggregate-json/aggregate.json -o pixstoryposts -v

# split the 95k JSON dataset up into 100-file chunks
# takes a while to finish!
# https://stackoverflow.com/questions/29116212/split-a-folder-into-multiple-subfolders-in-terminal-bash-script
i=0; for f in *; do d=dir_$(printf %03d $((i/100+1))); mkdir -p $d; mv "$f" $d; let i++; done

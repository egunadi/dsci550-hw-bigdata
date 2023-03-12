# stage 100-file chunk (ex. dir_001) for processing
cp -R ../../etl/json/dir_001 splits/
# (optional) rename files for ease of visual identification 
i=1; for file in splits/dir_001/*; do mv "$file" "splits/dir_001/row$i.json"; let i++; done

# circlepacking.html, cluster-d3.html, and levelCluster-d3.html from etllib must be present
# cp -R /Users/egunadi/Git/etllib/html/* .

# jaccard 
# --------
# create jaccard.csv
python ../jaccard_similarity.py --inputDir splits/dir_001 --outCSV jaccard.csv
# create circle.json
python ../edit-cosine-circle-packing.py --inputCSV jaccard.csv --cluster 2
# create clusters.json
python ../edit-cosine-cluster.py --inputCSV jaccard.csv --cluster 2
# create levelCluster.json
python ../generateLevelCluster.py
# host visualization at http://localhost:8082/levelCluster-d3.html
python -mhttp.server 8082

# save previous pipeline results
mkdir jaccard
mv *.json jaccard.csv jaccard

# edit distance
# ------------------
# create edit.csv
python ../edit-value-similarity.py --inputDir splits/dir_001 --outCSV edit.csv
# create circle.json
python ../edit-cosine-circle-packing.py --inputCSV edit.csv --cluster 0
# create clusters.json
python ../edit-cosine-cluster.py --inputCSV edit.csv --cluster 2
# create levelCluster.json
python ../generateLevelCluster.py
# host visualization at http://localhost:8082/levelCluster-d3.html
python -mhttp.server 8082

# save previous pipeline results
mkdir edit
mv *.json edit.csv edit

# cosine similarity
# ------------------
# create cosine.csv
python ../cosine_similarity.py --inputDir splits/dir_001 --outCSV cosine.csv
# create circle.json
python ../edit-cosine-circle-packing.py --inputCSV cosine.csv --cluster 2
# create clusters.json
python ../edit-cosine-cluster.py --inputCSV cosine.csv --cluster 2
# create levelCluster.json
python ../generateLevelCluster.py
# host visualization at http://localhost:8082/levelCluster-d3.html
python -mhttp.server 8082

# save previous pipeline results
mkdir cosine
mv *.json cosine.csv cosine



#!/usr/bin/env python2.7
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#

from tika import parser
from vector import Vector
import os, itertools, argparse, csv
from requests import ConnectionError
from time import sleep
import ast
import sys

def filterFiles(inputDir, acceptTypes):
    filename_list = []

    for root, dirnames, files in os.walk(inputDir):
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]
        for filename in files:
            if not filename.startswith('.'):
                filename_list.append(os.path.join(root, filename))
    try:
        filename_list = [filename for filename in filename_list if "metadata" in parser.from_file(filename)]
    except ConnectionError:
        sleep(1)
    if acceptTypes:
        filename_list = [filename for filename in filename_list if str(parser.from_file(filename)['metadata']['Content-Type'].encode('utf-8').decode('utf-8')).split('/')[-1] in acceptTypes]
    else:
        print("Accepting all MIME Types.....")

    return filename_list


def computeScores(inputDir, outCSV, acceptTypes):

    if sys.version_info[0] >= 3:
        openMode = "w"
    else:
        openMode = "wb"
    
    with open(outCSV, openMode) as outF:
        a = csv.writer(outF, delimiter=',')
        a.writerow(["x-coordinate","y-coordinate","Similarity_score"])        

        files_tuple = itertools.combinations(filterFiles(inputDir, acceptTypes), 2)
        for file1, file2 in files_tuple:
            try:
                row_cosine_distance = [file1, file2]
            
                file1_parsedData = parser.from_file(file1)
                file2_parsedData = parser.from_file(file2)
           
                v1 = Vector(file1, file1_parsedData["metadata"])
                v2 = Vector(file2, file2_parsedData["metadata"])
            

                row_cosine_distance.append(v1.cosTheta(v2))            

                a.writerow(row_cosine_distance)  
            except ConnectionError:
                sleep(1)
            except KeyError:
                continue

'''
Takes an input file and generates similarity scores for all combinations of row entries.
'''
def computeScores2(inputFile, outCSV):
    if sys.version_info[0] >= 3:
        openMode = "w"
    else:
        openMode = "wb"
        
    with open(outCSV, openMode) as outF:
        a = csv.writer(outF, delimiter=',')
        a.writerow(["x-coordinate", "y-coordinate", "Similarity_score"])

        file1_parsedData = parser.from_file(inputFile)
        row_list = ast.literal_eval(file1_parsedData["content"])

        rows_tuple = itertools.combinations(row_list, 2)
        for row1, row2 in rows_tuple:

            try:
                row_cosine_distance = [row_list.index(row1), row_list.index(row2)]

                v1 = Vector(inputFile, row1)
                v2 = Vector(inputFile, row2)

                row_cosine_distance.append(v1.cosTheta(v2))

                a.writerow(row_cosine_distance)
            except ConnectionError:
                sleep(1)
            except KeyError:
                continue


if __name__ == "__main__":

    argParser = argparse.ArgumentParser('Cosine similarity based on Metadata values')
    argParser.add_argument('--inputFile', required=False, help='path to file')
    argParser.add_argument('--inputDir', required=False, help='path to directory containing files')
    argParser.add_argument('--outCSV', required=True, help='path to directory for storing the output CSV File, containing pair-wise Cosine similarity Scores')
    argParser.add_argument('--accept', nargs='+', type=str, help='Optional: compute similarity only on specified IANA MIME Type(s)')
    args = argParser.parse_args()

    if args.inputDir and args.outCSV:
        computeScores(args.inputDir, args.outCSV, args.accept)
    if args.inputFile and args.outCSV:
        computeScores2(args.inputFile, args.outCSV)

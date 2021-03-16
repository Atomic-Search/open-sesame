#!/usr/bin/env python3
# -*- coding: utf8 -*-
"""
This module takes a directory and optionally a max number of files 
(these should be in json), breaks each one up into sentences, 
and writes them to a plain text file.
"""

# Hacky fix so that I can import from AtomicCloud.py.
# TODO: Definitely fix this when things are integrated
# into packages. Since this is still experimental,
# I'm not going to try to do that stuff right now.

import sys
sys.path.append('/home/ubuntu/src/mvp/single_article_search')


import json
import os
import argparse
import spacy


nlp = spacy.load("en_core_web_lg")

def main(args):
    """  """
    with open("sentences.txt", "w") as sentf:
        directory = args.directory
        max_files = args.max
        
        print(f"Getting list of files from directory: {directory}.")
        filenames = []
        try:
            for filename in os.listdir(directory):
                if filename.endswith(".json"):
                    filenames.append(filename)
        except:
            print(f"Can't find directory: {directory}")
        if len(filenames) < 1:
            raise Exception(f"No JSON files found in directory: {directory}")
        else:
            print(f"Files found: {len(filenames)}")
        i = 0
        for filename in filenames:
            i += 1
            if i > max_files:
                break
            with open(f"{directory}/{filename}", "r") as f:
                json_doc = json.load(f)
            body = json_doc['text']
            title = json_doc['title']
            url = json_doc['source']
            doc = nlp(body)
            for span in doc.sents:
                sentence = span.text
                sentence.strip()
                if sentence:
                    print(sentence, file=sentf)


if __name__ == "__main__":
    """  """
    
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument("directory", 
                        help="The absolute path to the directory in which \
                            the input documents are found.")
    parser.add_argument("-m", "--max", action="store", type=int,
                        help="Optionally enter a maximum number of \
                            documents to process.")
     
    # Optional verbosity counter (eg. -v, -vv, -vvv, etc.)
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Verbosity (-v, -vv, etc)")

    args = parser.parse_args()
    if args.max < 1:
        raise TypeError("Only positive integers allowed for optional \
                        --max argument.")
    
    main(args)


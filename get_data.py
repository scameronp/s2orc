"""

Example of how one would download & process a single batch of S2ORC to filter to specific field of study.
Can be useful for those who can't store the full dataset onto disk easily.
Please adapt this to your own field of study.


Creates directory structure:

|-- metadata/
    |-- raw/
        |-- metadata_0.jsonl.gz      << input; deleted after processed
    |-- medicine/
        |-- metadata_0.jsonl         << output
|-- pdf_parses/
    |-- raw/
        |-- pdf_parses_0.jsonl.gz    << input; deleted after processed
    |-- medicine/
        |-- pdf_parses_0.jsonl       << output

"""


import os
import subprocess
import gzip
import io
import json
from turtle import down
from tqdm import tqdm
from collections import defaultdict
import re
import glob

# TODO: update with right info
FIELD_OF_STUDY = 'Computer Science'
FOLDER_NAME = 'computer_science'
URLS_EXPIRES = '20220715'

METADATA_INPUT_DIR = 'metadata/raw/'
METADATA_OUTPUT_DIR = f'metadata/{FOLDER_NAME}/'
PDF_PARSES_INPUT_DIR = 'pdf_parses/raw/'
PDF_PARSES_OUTPUT_DIR = f'pdf_parses/{FOLDER_NAME}/'

METADATA_FILE_LIST = [os.path.basename(x) for x in glob.glob(METADATA_OUTPUT_DIR + "*.jsonl.gz")]
PDF_PARSES_FILE_LIST = [os.path.basename(x) for x in glob.glob(PDF_PARSES_OUTPUT_DIR + "*.jsonl.gz")]


# process single batch
def process_batch(batch: dict):
    # this downloads both the metadata & full text files for a particular shard
    cmd = ["wget", "-O", batch['input_metadata_path'], batch['input_metadata_url']]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)

    cmd = ["wget", "-O", batch['input_pdf_parses_path'], batch['input_pdf_parses_url']]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)

    # first, let's filter metadata JSONL to only papers with a particular field of study.
    # we also want to remember which paper IDs to keep, so that we can get their full text later.
    paper_ids_to_keep = set()
    with gzip.open(batch['input_metadata_path'], 'rb') as gz, open(batch['output_metadata_path'], 'wb') as f_out:
        f = io.BufferedReader(gz)
        for line in tqdm(f.readlines()):
            metadata_dict = json.loads(line)
            paper_id = metadata_dict['paper_id']
            mag_field_of_study = metadata_dict['mag_field_of_study']
            if mag_field_of_study and FIELD_OF_STUDY in mag_field_of_study:     # TODO: <<< change this to your filter
                paper_ids_to_keep.add(paper_id)
                f_out.write(line)

    # now, we get those papers' full text
    with gzip.open(batch['input_pdf_parses_path'], 'rb') as gz, open(batch['output_pdf_parses_path'], 'wb') as f_out:
        f = io.BufferedReader(gz)
        for line in tqdm(f.readlines()):
            metadata_dict = json.loads(line)
            paper_id = metadata_dict['paper_id']
            if paper_id in paper_ids_to_keep:
                f_out.write(line)

    # now delete the raw files to clear up space for other shards
    os.remove(batch['input_metadata_path'])
    os.remove(batch['input_pdf_parses_path'])


def already_downloaded(download_links):
    metadata_filename = os.path.basename(download_links['metadata'].split('?')[0])
    pdf_parses_filename = os.path.basename(download_links['pdf_parses'].split('?')[0])
    return metadata_filename in METADATA_FILE_LIST and pdf_parses_filename in PDF_PARSES_FILE_LIST


if __name__ == '__main__':

    os.makedirs(METADATA_INPUT_DIR, exist_ok=True)
    os.makedirs(METADATA_OUTPUT_DIR, exist_ok=True)
    os.makedirs(PDF_PARSES_INPUT_DIR, exist_ok=True)
    os.makedirs(PDF_PARSES_OUTPUT_DIR, exist_ok=True)

    # TODO: make sure to put the links we sent to you here
    # there are 100 shards with IDs 0 to 99. make sure these are paired correctly.

    download_linkss_dict = defaultdict(lambda: {"metadata": None, "pdf_parses": None})

    with open(f'dl_s2orc_20200705v1_full_urls_expires_{URLS_EXPIRES}.sh', 'r', encoding='utf-8') as f:
        for line in f:
            if metadata_match := re.search(r"^wget -O 20200705v1/full/metadata/metadata_(?P<shard_number>\d+).jsonl.gz '(?P<link>.+)'$", line):
                download_linkss_dict[metadata_match.group("shard_number")]["metadata"] = metadata_match.group("link")
            elif pdf_match := re.search(r"^wget -O 20200705v1/full/pdf_parses/pdf_parses_(?P<shard_number>\d+).jsonl.gz '(?P<link>.+)'$", line):
                download_linkss_dict[pdf_match.group("shard_number")]["pdf_parses"] = pdf_match.group("link")

    download_linkss = download_linkss_dict.values()

    # turn these into batches of work
    # TODO: feel free to come up with your own naming convention for 'input_{metadata|pdf_parses}_path'
    batches = [{
        'input_metadata_url': download_links['metadata'],
        'input_metadata_path': os.path.join(METADATA_INPUT_DIR,
                                            os.path.basename(download_links['metadata'].split('?')[0])),
        'output_metadata_path': os.path.join(METADATA_OUTPUT_DIR,
                                             os.path.basename(download_links['metadata'].split('?')[0])),
        'input_pdf_parses_url': download_links['pdf_parses'],
        'input_pdf_parses_path': os.path.join(PDF_PARSES_INPUT_DIR,
                                              os.path.basename(download_links['pdf_parses'].split('?')[0])),
        'output_pdf_parses_path': os.path.join(PDF_PARSES_OUTPUT_DIR,
                                               os.path.basename(download_links['pdf_parses'].split('?')[0])),
    } for download_links in download_linkss
               if not already_downloaded(download_links)]

    for batch in batches:
        process_batch(batch=batch)

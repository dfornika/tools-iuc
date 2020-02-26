#!/usr/bin/env python

import argparse
import errno
import json
import os
import subprocess


DATA_TABLE_NAME = "amrfinderplus_databases"

def wget_download_amrfinderplus_database(wget_args, target_directory, data_table_name=DATA_TABLE_NAME):
    
    args = [
        '--mirror',
        '--no-host-directories',
        wget_args['url'] + '/',
    ]
    
    subprocess.check_call(['wget'] + args, cwd=target_directory)

    data_table_entry = {
        'data_tables': {
            data_table_name: [
                {
                    "value": "amrfinder",
                    "name": "amrfinder",
                    "path": "amrfinder",
                }
            ]
        }
    }

    return data_table_entry

def main(args):

    data_manager_input = json.loads(open(args.data_manager_json).read())

    target_directory = data_manager_input['output_data'][0]['extra_files_path']

    try:
        os.mkdir( target_directory )
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir( target_directory ):
            pass
        else:
            raise

    data_manager_output = {}

    wget_args = {
        'url': args.url + args.db_version
    }

    data_manager_output = wget_download_amrfinderplus_database(
        wget_args,
        target_directory,
    )

    open(args.data_manager_json, 'w').write(json.dumps(data_manager_output))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('data_manager_json')
    parser.add_argument('--url', dest='url', action='store', default='ftp://ftp.ncbi.nlm.nih.gov/pathogen/Antimicrobial_resistance/AMRFinderPlus/database/', help='Download URL')
    parser.add_argument('--db-version', dest='db_version', default='latest', help='Download URL')
    args = parser.parse_args()

    main(args)

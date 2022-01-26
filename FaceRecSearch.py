#!/usr/bin/python3

import argparse
import face_recognition as fr
import numpy as np
import os
import shutil
import sys
import time
import concurrent.futures


def list_full_paths(directory):
    return [os.path.join(directory, file) for file in os.listdir(directory)]


class FaceRecSearch:

    image_file_types = ('.jpg', '.jpeg', '.JPG', '.JPEG', '.png', '.PNG')
    image_files = []

    def __init__(self, _options):
        self.source_directory = os.path.abspath(_options.sourcedir)
        if not os.path.isdir(self.source_directory):
            print('ERROR: source directory must exist')
            sys.exit(1)

        if not any(filename.endswith(self.image_file_types)
           for filename in os.listdir(self.source_directory)):
            print('ERROR: source directory must contain image files')
            sys.exit(1)

        if _options.outputdir:
            self.target_directory = os.path.abspath(_options.outputdir)
        else:
            parser.print_help()
            print('ERROR: target directory must be specified')
            sys.exit(1)
        if not os.path.isdir(self.target_directory):
            print('ERROR: target directory must exist')
            sys.exit(1)

        if _options.facedir:
            self.faces_directory = os.path.abspath(_options.facedir)
        else:
            parser.print_help()
            print('ERROR: faces directory must be specified')
            sys.exit(1)
        if not os.path.isdir(self.faces_directory):
            print('ERROR: faces directory must exist')
            sys.exit(1)

        if not any(filename.endswith(self.image_file_types)
           for filename in os.listdir(self.faces_directory)):
            print('ERROR: faces directory must contain image files')
            sys.exit(1)

        self.cpus = _options.cpus
        self.recursive = _options.recursive
        self.tolerance = _options.tolerance

        self.processed_face_encodings = []

    def process_image(self, file):
        print(f'Started processing {file}...')
        try:
            image = fr.load_image_file(file)
            face_locations = fr.face_locations(
                image, number_of_times_to_upsample=0)
            face_encodings = fr.face_encodings(image, face_locations)
            print(f'Processed {file}...')
            return file, face_encodings

        except Exception as err:
            print('ERROR: %s' % err)

    def run(self):
        if self.recursive:
            for root, directories, files in os.walk(self.source_directory):
                for file in files:
                    if file.endswith(self.image_file_types):
                        self.image_files.append(os.path.join(root, file))
        else:
            for file in os.listdir(self.source_directory):
                if file.endswith(self.image_file_types):
                    self.image_files.append(
                        os.path.join(self.source_directory, file))

        for face in list_full_paths(self.faces_directory):
            print(f'Started scanning for target faces in {face}...')
            try:
                image = fr.load_image_file(face)
                face_locations = fr.face_locations(image)
                if len(face_locations) > 1:
                    print('Multiple faces found, only using the first one')
                face_encoding = fr.face_encodings(
                    image, face_locations)
                print(f'Processed {face}...')
                self.processed_face_encodings.append(face_encoding[0])
            except Exception as err:
                print('ERROR: %s' % err)

        with concurrent.futures.ProcessPoolExecutor(max_workers=self.cpus) as executor:
            print('Running jobs...')
            results = executor.map(self.process_image, self.image_files)
            counter = 0
            for file, face_encodings in results:
                print(f'Checking {file}...')
                try:
                    for face_encoding in face_encodings:
                        matches = fr.compare_faces(self.processed_face_encodings, face_encoding, self.tolerance)

                        if np.any(matches):
                            print(f'Face found in {file}!')
                            counter = counter + 1
                            shutil.copyfile(file, os.path.join(
                                self.target_directory, str(counter) + '_' + os.path.basename(file)))
                            break
                except Exception as err:
                    print('ERROR: %s' % err)


if __name__ == '__main__':
    start = time.perf_counter()
    desc = " FaceRecSearch - Quick and dirty image search using facial recognition"

    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('sourcedir', help='where to search for matching images')
    parser.add_argument('outputdir', help='where found images should be stored')
    parser.add_argument('facedir', help='directory containing examples of the face you are looking for')
    parser.add_argument('--tolerance', default=0.6, help='distance between faces to consider it a match, lower is more strict.', metavar='0.6')
    parser.add_argument('--cpus', default=os.cpu_count(), help="number of CPUs to use, defaults to all")
    parser.add_argument('--recursive', action='store_false', help='search in all subdirectories of sourcedir')
    options = parser.parse_args()

    if not (options.sourcedir and options.outputdir and options.facedir):
        parser.print_help()
        print('ERROR: source, face and output directory must be specified')
        sys.exit(1)

    face_search = FaceRecSearch(options)
    face_search.run()

    finish = time.perf_counter()
    print(f'Finished in {round(finish - start, 2)} second(s)')

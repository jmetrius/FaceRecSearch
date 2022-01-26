# FaceRecSearch
This script attempts to search for people in pictures by comparing all faces in the picture with the faces in a prespecified set of images. All matching pictures will be copied and stored in the output folder.

### Installing
This script depends on [face_recognition](https://github.com/ageitgey/face_recognition) for all the heavy lifting.
Install it first by running:
```
$ pip install face_recognition
```
Afterwards, clone this Git repository or download the script separatly:
```
$ git clone https://github.com/jmetrius/FaceRecSearch.git
$ cd FaceRecSearch
```

## Usage
```
$ python FaceRecSearch.py [-h] [--tolerance 0.6] [--cpus CPUS] [--recursive] sourcedir outputdir facedir

FaceRecSearch - Quick and dirty image search using facial recognition

positional arguments:
  sourcedir        where to search for matching images
  outputdir        where found images should be stored
  facedir          directory containing examples of the face you are looking for

options:
  -h, --help       show this help message and exit
  --tolerance 0.6  distance between faces to consider it a match, lower is more strict.
  --cpus CPUS      number of CPUs to use, defaults to all
  --recursive      search in all subdirectories of sourcedir
```

## Additional hints
* The default tolerance is based on the recommendations of the face_recognition module. For my use case, a stricter setting of 0.45 was better but your experience might differ.
* If a picture in facedir contains faces of multiple people, only the first one will be used. This might lead to unexpected behaviour, therefore make sure only one face is visible in each example picture.
* It's advisable to place multiple example pictures of the same person (showing the face in different angles or with different expressions) in facedir. You can also place pictures of different people if you want to search for more than one person at once. However, since every example face is compared with all faces of pictures in the sourcedir, runtime may increase drastically with additional faces. 2-3 pictures per person should be enough.

## Credits
Credit goes to greatwhitehat for providing [faceoff](https://github.com/greatwhitehat/faceoff) which served as the inital codebase for this script.

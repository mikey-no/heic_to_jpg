# heic file convert to jpg

Simple command line python programme to convert heic image files to jpg.

It uses [pillow_heif](https://pypi.org/project/pillow-heif/) and [pillow heif home page](https://github.com/bigcat88/pillow_heif)
and PIL or should I say pillow supported version of [pillow](https://pillow.readthedocs.io/en/stable/reference/Image.html).

All the cleaver stuff is done by the above two packages.

I have added a simple python wrapper to allow a folder to be supplied as an argument (```--source```) and 
a destination (```--destination```) in which to save any heic files converted to jpg. If no destination argument
is supplied then the source directory is use.

## Usage

```commandline
python heic_to_jpg.py --source ..\test-files\001 --destination ..\test-files
```

## Instalation

### Runs on

- Python 3.10 (Windows 10)

## Setup

from the project root folder ```heic_to_jpg```

```commandline
python -m venv venv
.\venv\scripts\activate.bat
pip install -r requirements.txt
```

# Future

1) add proper tests rather than the informal ones done to date.
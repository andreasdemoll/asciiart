asciiart
========

Description
-----------
asciiart is a python project that converts images into asciiart images, using a palette of ascii characters with different brightness levels.
A given .jpg file is converted to an ascii-art .png file and stored in the same folder. asciiart is called via command line.

Installation
------------
* Clone this repository via `git clone https://github.com/andreasdemoll/asciiart` or simply download it.
* Install virtual environments via `pip install virtualenv` if not existing.
* Navigate into that folder and create a virutal environment via `virtualenv venv`.
* Activate the environment via `source venv/bin/activate`
* Install required packages via `pip install -r requirements.txt`
* Deactivate environment after use via `deactivate`

Example calls
-------------
* `python3 asciiart.py imag/Emil.jpg` will convert with standard parameters.
* `python3 asciiart.py imag/Emil.jpg --nhor 150` will convert to an image with 150 characters in the horizontal dimension.
* `python3 asciiart.py imag/Emil.jpg --nhor 150 --color 0,255,0` will convert as above but in green.

> Activate virtual environment first via `source venv/bin/activate`, deactivate after use by `deactivate`.

> Call `python3 asciiart.py --help` for all possible options.

Future releases
---------------
* destination file as parameter.
* make it run faster by avoiding loops.
* colored 'asciiart' support.
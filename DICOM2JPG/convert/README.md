# dicom2jpg

dicom2jpg is a Python converter to generate CrypTFlow secure inference-ready X-ray image input directory. Using the DICOM to JPG converter for CrypTFlow secure inference is simple!

## Usage

```
$ python dicom2jpg.py -i <input_directory> -o <output_directory>
```
where ``<input_directory>`` is the path to the input directory of interest. It must contain a sub-directory for each study, and each study directory contains the Chest X-ray images (DICOM format)
corresponding to it.

AND 

``<output_directory>`` is the path of the output directory where the jpg images are stored. This output directory generated matches exactly what is required by the ``client`` as input image directory (see client instructions) to run a secure inference experiment with CrypTFlow. 


## Requirements
Python libraries: numpy, pydicom, png

## Written by
Arjun Soin, [Stanford AIMI](https://aimi.stanford.edu/)

import argparse
import time
import numpy as np
import png, os, pydicom # Note that the package png requires module 'pypng'

def dicom2jpg(source_folder, output_folder):
    # Get list of CXRs in each study
    xray_images = os.listdir(source_folder)
    for xray in xray_images:
        try:
            ds = pydicom.dcmread(os.path.join(source_folder,xray))
            shape = ds.pixel_array.shape

            # Convert to float to avoid overflow or underflow losses.
            image_2d = ds.pixel_array.astype(float)
            
            # depending on the value of the array, X-ray may look inverted - fix that:
            if ds.PhotometricInterpretation == "MONOCHROME1":
                image_2d = np.amax(image_2d) - image_2d 

            # Rescaling grey scale between 0-255
            image_2d_scaled = (np.maximum(image_2d,0) / image_2d.max()) * 255.0

            # Convert to uint
            image_2d_scaled = np.uint8(image_2d_scaled)

            # Write the file
            with open(os.path.join(output_folder, xray.replace(".dcm", "")) + '.jpg' , 'wb') as jpg_file:
                w = png.Writer(shape[1], shape[0], greyscale=True)
                w.write(jpg_file, image_2d_scaled)
        except:
            print('Could not convert: ', xray)


def main():
    for study in os.listdir(source_folder):
        if os.path.isdir(os.path.join(source_folder, study)):
            study_path = os.path.join(source_folder, study)
            # Check if the output directory exists, if not then create it
            isExist = os.path.exists(output_folder)
            if not isExist:
                os.makedirs(output_folder)
            dicom2jpg(study_path, output_folder)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='A DICOM to PNG/JPG converter for CrypTFlow secure inference. Assumes your input \
    directory contains sub-directories for each study, and each study directory then contains the Chest X-ray images corresponding to it. \
    If executed correctly, an output directory that matches the requirements of an input images directory for CrypTFlow secure inference \
    will be created. End-to-end conversion time will also be printed upon successful execution.')

    parser.add_argument("-i", "--input_dir", required=True, help="Input directory path. Input directory should contain study directories, and each study directory should contain X-ray images.")
    parser.add_argument("-o", "--output_dir", required=True, help="Output directory path. Will create a directory in the specified location if it doesn't exist.")

    args = parser.parse_args()
    args_dict = vars(args)

    # Input directory
    source_folder = args_dict["input_dir"] 

    # Output directory, will be created if doesn't exist
    output_folder = args_dict["output_dir"] 

    # Time the conversion end-to-end and print to console
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
import os
import pydicom

def readInputDir(inputDir):
    """This function scans all files in 

    Args:
        inputDir (string): path to input folder, where storing new .dcm files

    Returns:
        structure: data[patient_id][study_id][series_number].append(dcm_file_path)
    """

    # Dictionary to hold the structure
    data = {}

    # Traverse the directory
    for root, dirs, files in os.walk(inputDir):
        for file in files:
            if file.endswith(".dcm"):
                file_path = os.path.join(root, file)
                
                # Read the DICOM file
                dicom = pydicom.dcmread(file_path)
                
                # Extract Patient, Study, and Series information
                patient_id = dicom.PatientID
                study_id = dicom.StudyID
                series_number = dicom.SeriesNumber
                
                # Update the structure dictionary
                if patient_id not in data:
                    data[patient_id] = {}
                if study_id not in data[patient_id]:
                    data[patient_id][study_id] = {}
                if series_number not in data[patient_id][study_id]:
                    data[patient_id][study_id][series_number] = []
                    
                data[patient_id][study_id][series_number].append(file_path)

    return data

# Set the path to the directory containing the .dcm files
inputPath = "/app/store/input" # Keep this if you 

# Read input directory
data = readInputDir(inputPath)

# Function to print the structure
def print_structure(data):
    for patient_id, studies in data.items():
        print(f"Patient: {patient_id}")
        for study_id, series in studies.items():
            print(f"  Study: {study_id}")
            for series_number, images in series.items():
                print(f"    Series: {series_number}")
                for image in images:
                    print(f"      Image: {image}")

# Print the structure
print_structure(data)
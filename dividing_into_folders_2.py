import os
import shutil
import random
import pandas as pd

# Set source folder and Excel file
source_folder = r"C:\final_project\freqs_power_model\freqs_power_abs_ThABG_200ms_L0123\all_jsons\ALL"
excel_file = r"C:\final_project\H1H7 test Yonatan imputated.xlsx"
destination_folder = r"C:\final_project\freqs_power_model\freqs_power_abs_ThABG_200ms_L0123"

# Read Excel file
df = pd.read_excel(excel_file)

# Create subfolders for each treatment
treatment_a_folder = os.path.join(destination_folder, 'treatment_a')
treatment_b_folder = os.path.join(destination_folder, 'treatment_b')
os.makedirs(treatment_a_folder, exist_ok=True)
os.makedirs(treatment_b_folder, exist_ok=True)

# Loop through all patients and copy their files to the appropriate folder
for filename in os.listdir(source_folder):
    if 'sess1' in filename:
        patient_id = filename[0:5]
        patient_row = df.loc[df['Subject'] == patient_id]

        if len(patient_row) == 0:
            print(f"No data found for patient {patient_id}")
            continue

        treatment = patient_row['Coil'].values[0]

        # Copy file to appropriate folder
        if treatment == 'A':
            destination_folder = treatment_a_folder
        elif treatment == 'B':
            destination_folder = treatment_b_folder
        else:
            continue

        shutil.copy(os.path.join(source_folder, filename), os.path.join(destination_folder, filename))
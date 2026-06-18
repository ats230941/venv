import easyocr
import os
import shutil
import pandas as pd
from datetime import datetime

# 1. Define folder paths
input_folder = r"C:\Users\DakotaLink\OneDrive\Adam's Files\01_Unprocessed_Receipts"
processed_folder = r"C:\Users\DakotaLink\OneDrive\Adam's Files\02_Processed_Receipts"
csv_path = os.path.join(input_folder, "receipts_log.csv")

# 2. Initialize the OCR engine
print("Initializing OCR Engine...")
reader = easyocr.Reader(['en'])

# 3. Scan the folder for images (Added .heic just in case your iPhone defaults to it!)
valid_extensions = ('.png', '.jpg', '.jpeg', '.png.png', '.heic')
all_files = os.listdir(input_folder)
image_files = [f for f in all_files if f.lower().endswith(valid_extensions)]

if not image_files:
    print("No receipt images found to process!")
    exit()

print(f"Found {len(image_files)} receipts to process.\n")

# 4. Process each image
for filename in image_files:
    print(f"--- Processing: {filename} ---")
    image_path = os.path.join(input_folder, filename)
    destination_path = os.path.join(processed_folder, filename)
    
    # Run OCR to get a list of every line found
    result = reader.readtext(image_path, detail=0)
    
    # Combine every single line of text found, separated by a clear separator
    full_raw_dump = " | ".join(result)
    print("Logged text snapshot:", result[:3], "...") # Keep terminal output neat

    # 5. Prepare data for spreadsheet (Dumping the entire text block)
    receipt_data = {
        "Date_Processed": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Filename": filename,
        "Full_Raw_Text": full_raw_dump
    }
    
    # 6. Save/Append to CSV Spreadsheet using Pandas
    df = pd.DataFrame([receipt_data])
    if not os.path.exists(csv_path):
        df.to_csv(csv_path, index=False)
    else:
        df.to_csv(csv_path, mode='a', header=False, index=False)
    print(f"Logged {filename} to CSV.")
    
    # 7. Ensure the destination folder exists before moving
    if not os.path.exists(processed_folder):
        os.makedirs(processed_folder)
        print(f"Created missing destination folder: {processed_folder}")
        
    shutil.move(image_path, destination_path)
    print(f"Moved {filename} to 02_Processed_Receipts folder.\n")

print("All receipts processed successfully!")
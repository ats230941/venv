import os

def triage_raw_ocr(input_file="raw_ocr_output.txt"):
    print("=== Starting Layer 1: Data Triage (Case Normalized) ===")
    
    # Check if our raw file from the OCR step exists
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found. Ensure your OCR engine ran successfully.")
        return False

    # Since everything will be converted to lowercase, our filter keywords must be lowercase
    metadata_keywords = [
        "terminal", "txn id", "auth code", "station no", 
        "sequence", "merchant id", "host reg", "batch"
    ]
    
    core_lines = []
    metadata_lines = []
    
    # Read the raw OCR block line by line
    with open(input_file, "r") as f:
        lines = f.readlines()
        
    for line in lines:
        # Crucial step: Strip empty spaces AND normalize completely to lowercase right here
        cleaned_line = line.strip().lower()
        if not cleaned_line:
            continue # Skip empty breaks
            
        # Check if our lowercase line contains any of our lowercase metadata tokens
        is_metadata = any(keyword in cleaned_line for keyword in metadata_keywords)
        
        if is_metadata:
            metadata_lines.append(cleaned_line)
        else:
            core_lines.append(cleaned_line)
            
    # Append isolated metadata logs out to a background tracking file
    with open("metadata_log.txt", "a") as meta_file:
        for line in metadata_lines:
            meta_file.write(line + "\n")
            
    # Write the clean, normalized transaction meat out to our next pipeline step
    with open("core_payload.txt", "w") as core_file:
        for line in core_lines:
            core_file.write(line + "\n")
            
    print(f"✅ Success! Isolated {len(metadata_lines)} metadata lines and saved {len(core_lines)} normalized core text lines.")
    return True

if __name__ == "__main__":
    triage_raw_ocr()
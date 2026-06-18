import csv
import os

def clean_and_parse_summary(raw_summary):
    # Split the text by the pipe symbol
    segments = [seg.strip() for seg in raw_summary.split('|')]
    
    estimated_total = "0.00"
    payment_method = "Unknown"
    
    # Micromanage the Total
    for i, seg in enumerate(segments):
        if seg.upper() in ["TOTAL", "TOTAL SALE"]:
            if i + 1 < len(segments):
                raw_amount = segments[i + 1]
                # Fix European commas (19,54 -> 19.54)
                estimated_total = raw_amount.replace(',', '.')
                break
                
    # Micromanage the Payment Method
    for seg in segments:
        seg_upper = seg.upper()
        if "DEBIT" in seg_upper:
            payment_method = "Debit Card"
            break
        elif "VISA" in seg_upper:
            payment_method = "Visa"
            break
        elif "MASTERCARD" in seg_upper or "MC " in seg_upper:
            payment_method = "Mastercard"
            break
        elif "CASH" in seg_upper:
            payment_method = "Cash"
            break
            
    return estimated_total, payment_method

def process_log_file():
    # Input and Output Paths provided by you
    input_path = r"C:\Users\DakotaLink\OneDrive\Adam's Files\01_Unprocessed_Receipts\receipts_log.csv"
    output_dir = r"C:\Users\DakotaLink\OneDrive\Adam's Files\02_Processed_Archive"
    output_path = os.path.join(output_dir, "clean_parsed_receipts.csv")

    print(f"Reading messy log from: {input_path}")

    # Open the messy file to read, and a new clean file to write
    with open(input_path, mode='r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        
        # Define the exact headers Excel wants to see
        fieldnames = ['Date_Processed', 'Filename', 'Raw_Text_Summary', 'Estimated_Total', 'Payment_Method']
        
        with open(output_path, mode='w', newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader() # Write the top header row

            # Loop through each row in your messy log
            for row in reader:
                raw_text = row['Raw_Text_Summary']
                
                # Run your micromanagement rules!
                total, payment = clean_and_parse_summary(raw_text)
                
                # Update the empty slots with our beautifully extracted data
                row['Estimated_Total'] = total
                row['Payment_Method'] = payment
                
                # Write the clean row to the archive file
                writer.writerow(row)
                print(f"Processed: {row['Filename']} -> Total: ${total}, Pay: {payment}")

    print(f"\nSuccess! Cleaned data saved to: {output_path}")

if __name__ == "__main__":
    process_log_file()
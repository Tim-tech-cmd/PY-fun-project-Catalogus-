import pdfplumber
import pandas as pd
import re

# Path to your PDF file
pdf_path = "Smits Wunsch (Jubilee).pdf"

# Function to extract numbers between 3000 and 15500 from the left side of the page
def extract_numbers_from_left_side(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        extracted_numbers = []
        
        # Loop through each page in the PDF
        for page_num, page in enumerate(pdf.pages, start=1):
            # Define a crop box for the left side of the page (adjust the dimensions as needed)
            left_crop = page.within_bbox((0, 0, page.width / 2, page.height))  # Left half of the page
            
            # Extract text from the cropped left side
            text = left_crop.extract_text()
            
            if text:
                # Use regex to find all numbers in the text
                numbers = re.findall(r'\b\d{4,5}\b', text)  # Match 4 or 5 digit numbers
                
                # Filter numbers between 3000 and 15500
                filtered_numbers = [int(num) for num in numbers if 3000 <= int(num) <= 15500]
                
                # Add filtered numbers to the list
                extracted_numbers.extend(filtered_numbers)
            else:
                print(f"No text found on the left side of page {page_num}")
        
        return extracted_numbers

# Extract numbers
numbers_in_range = extract_numbers_from_left_side(pdf_path)

# Sort the numbers chronologically
numbers_in_range.sort()

# Print the extracted numbers
print("Extracted Numbers from 3000 to 15500 (chronologically):")
print(numbers_in_range)

# Optionally, save to a CSV
pd.DataFrame(numbers_in_range, columns=["Los-Nr"]).to_csv("filtered_los_nr.csv", index=False)

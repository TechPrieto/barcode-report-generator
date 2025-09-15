# Barcode Report Generator

A Python script that reads a text file with comma-separated values and generates a PDF report with Code 128 barcodes.

## Features

- Reads TXT files with comma-separated values
- Generates Code 128 barcodes for each value
- Creates a professional PDF report
- Shows original values below each barcode
- Groups barcodes by row from input file

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/barcode-report-generator.git
cd barcode-report-generator
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Create an `input.txt` file with your data:
```
Value1,Value2,,,value3
test1,test2,test3
```

2. Run the script:
```bash
python barcode_report_generator.py
```

3. The PDF report will be generated as `barcode_report.pdf`

## Input Format

- Each line represents a row
- Values are separated by commas
- Empty values (multiple commas) are ignored
- Example: `value1,value2,,value3` will generate 3 barcodes

## Requirements

- Python 3.6+
- reportlab
- python-barcode
- pillow

## License

MIT License

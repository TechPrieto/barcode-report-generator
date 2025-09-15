import os
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
import tempfile
import barcode
from barcode.writer import ImageWriter
from io import BytesIO

def create_barcode_image(value):
    """Create a barcode image for the given value using python-barcode"""
    try:
        # Create Code128 barcode
        code128 = barcode.get_barcode_class('code128')
        barcode_instance = code128(value, writer=ImageWriter())
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        temp_file.close()
        
        # Save barcode to temporary file
        barcode_instance.save(temp_file.name.replace('.png', ''))
        
        return temp_file.name
    except Exception as e:
        print(f"Error creating barcode for '{value}': {e}")
        return None

def generate_barcode_report(input_file, output_file="barcode_report.pdf"):
    """Generate PDF report with barcodes from input file"""
    
    # Create PDF document
    doc = SimpleDocTemplate(output_file, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()
    temp_files = []  # Keep track of temp files to clean up
    
    # Title
    title = Paragraph("Barcode Report", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 20))
    
    try:
        with open(input_file, 'r') as f:
            row_number = 1
            
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                # Split by comma and filter out empty values
                values = [v.strip() for v in line.split(',') if v.strip()]
                
                if not values:
                    continue
                
                # Row header
                row_header = Paragraph(f"<b>Row {row_number}:</b> {line}", styles['Heading2'])
                story.append(row_header)
                story.append(Spacer(1, 10))
                
                # Create table data for this row
                table_data = []
                
                # Create barcodes for each value
                barcode_row = []
                text_row = []
                
                for value in values:
                    # Create barcode image
                    barcode_file = create_barcode_image(value)
                    if barcode_file and os.path.exists(barcode_file):
                        temp_files.append(barcode_file)
                        barcode_img = Image(barcode_file, width=2.5*inch, height=0.7*inch)
                        barcode_row.append(barcode_img)
                        text_row.append(Paragraph(f"<para align=center><font size=8>{value}</font></para>", styles['Normal']))
                    else:
                        barcode_row.append(Paragraph(f"<para align=center>Error generating barcode</para>", styles['Normal']))
                        text_row.append(Paragraph(f"<para align=center>{value}</para>", styles['Normal']))
                
                # Add rows to table data
                if barcode_row:
                    table_data.append(barcode_row)
                    table_data.append(text_row)
                
                # Create table
                if table_data:
                    table = Table(table_data, colWidths=[2.7*inch] * len(values))
                    table.setStyle(TableStyle([
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('FONTSIZE', (0, 1), (-1, 1), 8),  # Text row font size
                        ('TOPPADDING', (0, 0), (-1, -1), 5),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                        ('LEFTPADDING', (0, 0), (-1, -1), 5),
                        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
                    ]))
                    
                    story.append(table)
                    story.append(Spacer(1, 20))
                
                row_number += 1
    
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        return False
    except Exception as e:
        print(f"Error processing file: {e}")
        return False
    
    # Build PDF
    try:
        doc.build(story)
        print(f"Barcode report generated successfully: {output_file}")
        
        # Clean up temporary files
        for temp_file in temp_files:
            try:
                os.unlink(temp_file)
            except:
                pass
        
        return True
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return False

# Main execution
if __name__ == "__main__":
    # Input file name
    input_filename = "input.txt"
    output_filename = "barcode_report.pdf"
    
    # Check if input file exists
    if not os.path.exists(input_filename):
        print(f"Creating sample input file: {input_filename}")
        with open(input_filename, 'w') as f:
            f.write("b11,46556$2525256002$75,,,20030101120220\n")
            f.write("test1,test2,test3\n")
        print("Sample file created. Edit it with your data and run the script again.")
    else:
        # Generate the report
        generate_barcode_report(input_filename, output_filename)
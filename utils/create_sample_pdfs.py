import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors

def convert_text_to_pdf(text_file, pdf_file):
    """Convert a text file to a PDF file"""
    # Read the text file
    with open(text_file, 'r') as f:
        text_content = f.read()
    
    # Create a PDF document
    doc = SimpleDocTemplate(
        pdf_file,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    # Define styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='Title',
        parent=styles['Heading1'],
        fontSize=16,
        alignment=TA_CENTER,
        spaceAfter=12
    ))
    styles.add(ParagraphStyle(
        name='Normal_Justified',
        parent=styles['Normal'],
        alignment=TA_JUSTIFY
    ))
    
    # Process the text content
    lines = text_content.split('\n')
    story = []
    
    # Assume the first line is the title
    if lines:
        story.append(Paragraph(lines[0], styles['Title']))
        story.append(Spacer(1, 12))
    
    # Process the rest of the content
    current_paragraph = []
    
    for line in lines[1:]:
        # Empty line indicates paragraph break
        if not line.strip():
            if current_paragraph:
                para_text = ' '.join(current_paragraph)
                story.append(Paragraph(para_text, styles['Normal_Justified']))
                story.append(Spacer(1, 6))
                current_paragraph = []
        # Line starting with a special character might be a header
        elif line.strip().startswith(('#', '*', '-')):
            if current_paragraph:
                para_text = ' '.join(current_paragraph)
                story.append(Paragraph(para_text, styles['Normal_Justified']))
                story.append(Spacer(1, 6))
                current_paragraph = []
            story.append(Paragraph(line.strip(), styles['Heading2']))
            story.append(Spacer(1, 6))
        # Line with a colon might be a field
        elif ':' in line and len(line.split(':', 1)[0].split()) <= 3:
            if current_paragraph:
                para_text = ' '.join(current_paragraph)
                story.append(Paragraph(para_text, styles['Normal_Justified']))
                story.append(Spacer(1, 6))
                current_paragraph = []
            key, value = line.split(':', 1)
            story.append(Paragraph(f"<b>{key}:</b>{value}", styles['Normal']))
        # Regular line
        else:
            current_paragraph.append(line.strip())
    
    # Add the last paragraph if any
    if current_paragraph:
        para_text = ' '.join(current_paragraph)
        story.append(Paragraph(para_text, styles['Normal_Justified']))
    
    # Build the PDF
    doc.build(story)
    print(f"Created PDF: {pdf_file}")

def main():
    """Convert sample text files to PDFs"""
    # Get the base directory
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, 'data')
    
    # Convert company info
    company_info_txt = os.path.join(data_dir, 'company_info.txt')
    company_info_pdf = os.path.join(data_dir, 'company_info.pdf')
    if os.path.exists(company_info_txt):
        convert_text_to_pdf(company_info_txt, company_info_pdf)
    
    # Convert insurance offer
    insurance_offer_txt = os.path.join(data_dir, 'insurance_offer.txt')
    insurance_offer_pdf = os.path.join(data_dir, 'insurance_offer.pdf')
    if os.path.exists(insurance_offer_txt):
        convert_text_to_pdf(insurance_offer_txt, insurance_offer_pdf)
    
    print("\nPDF creation complete. You can now use these files in the tutorial.")

if __name__ == "__main__":
    main()
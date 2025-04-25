import os
import sys
from pathlib import Path

# Ensure PDFs are created first
print("Creating sample PDFs...")
from utils.create_sample_pdfs import main as create_pdfs
create_pdfs()

# Import the main workflow
from src.main import main as run_workflow

def test_workflow():
    """Test the entire maritime insurance processing workflow"""
    print("\n" + "="*50)
    print("TESTING MARITIME INSURANCE PROCESSING WORKFLOW")
    print("="*50 + "\n")
    
    # Check if PDF files exist
    data_dir = Path("data")
    company_info_pdf = data_dir / "company_info.pdf"
    insurance_offer_pdf = data_dir / "insurance_offer.pdf"
    broker_email_txt = data_dir / "broker_email.txt"
    
    missing_files = []
    if not company_info_pdf.exists():
        missing_files.append(str(company_info_pdf))
    if not insurance_offer_pdf.exists():
        missing_files.append(str(insurance_offer_pdf))
    if not broker_email_txt.exists():
        missing_files.append(str(broker_email_txt))
    
    if missing_files:
        print("ERROR: The following required files are missing:")
        for file in missing_files:
            print(f"  - {file}")
        print("\nPlease ensure these files exist before running the workflow.")
        return
    
    print("All required files found. Running the workflow...\n")
    
    try:
        # Run the workflow
        db_entry = run_workflow()
        
        # Verify the results
        print("\n" + "="*50)
        print("WORKFLOW TEST RESULTS")
        print("="*50)
        
        # Check if we have company information
        if db_entry.company and db_entry.company.name != "Unknown":
            print("✅ Successfully extracted company information")
        else:
            print("❌ Failed to extract company information")
        
        # Check if we have vessel information
        if db_entry.vessels and len(db_entry.vessels) > 0:
            print("✅ Successfully extracted vessel information")
            print(f"   Found {len(db_entry.vessels)} vessels with IMO numbers")
        else:
            print("❌ Failed to extract vessel information")
        
        # Check if we have insurance information
        if db_entry.insurance and db_entry.insurance.coverage_percentage > 0:
            print("✅ Successfully extracted insurance information")
        else:
            print("❌ Failed to extract insurance information")
        
        # Check if we have a risk assessment
        if db_entry.assessment and db_entry.assessment.risk_score > 0:
            print("✅ Successfully generated risk assessment")
            print(f"   Risk Score: {db_entry.assessment.risk_score}/10")
        else:
            print("❌ Failed to generate risk assessment")
        
        print("\nWorkflow test completed successfully!")
        
    except Exception as e:
        print(f"ERROR: An exception occurred while running the workflow: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_workflow()
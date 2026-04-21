#!/usr/bin/env python3
"""
Generate PDF files from Error Resolution Knowledge Base
Creates both master PDF and individual error PDFs
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from datetime import datetime
import os

# Import knowledge base from main system
import sys
sys.path.insert(0, '.')
from error_resolution_assistant import knowledge_base

# ============================================
# STYLING
# ============================================

def get_styles():
    """Create custom styles for PDF"""
    styles = getSampleStyleSheet()
    
    styles.add(ParagraphStyle(
        name='CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    ))
    
    styles.add(ParagraphStyle(
        name='ErrorName',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#d32f2f'),
        spaceAfter=6,
        fontName='Helvetica-Bold'
    ))
    
    styles.add(ParagraphStyle(
        name='SectionHeader',
        parent=styles['Heading3'],
        fontSize=11,
        textColor=colors.HexColor('#1976d2'),
        spaceAfter=4,
        fontName='Helvetica-Bold'
    ))
    
    styles.add(ParagraphStyle(
        name='Normal',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=6
    ))
    
    return styles

# ============================================
# PDF GENERATION FUNCTIONS
# ============================================

def generate_master_pdf():
    """Generate master PDF with all errors"""
    
    filename = "KB_Master_All_Errors.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter,
                           rightMargin=0.5*inch, leftMargin=0.5*inch,
                           topMargin=0.75*inch, bottomMargin=0.75*inch)
    
    styles = get_styles()
    story = []
    
    # Title
    title = Paragraph("Error Resolution Knowledge Base", styles['CustomTitle'])
    story.append(title)
    
    # Metadata
    metadata = Paragraph(
        f"<b>Generated:</b> {datetime.now().strftime('%B %d, %Y at %H:%M')}<br/>"
        f"<b>Total Errors:</b> {len(knowledge_base)}<br/>"
        f"<b>Version:</b> 1.0",
        styles['Normal']
    )
    story.append(metadata)
    story.append(Spacer(1, 0.3*inch))
    
    # Table of Contents
    story.append(Paragraph("Table of Contents", styles['SectionHeader']))
    story.append(Spacer(1, 0.1*inch))
    
    toc_items = []
    for i, (key, error) in enumerate(knowledge_base.items(), 1):
        toc_items.append(Paragraph(f"{i}. {error['error_name']}", styles['Normal']))
    
    for item in toc_items:
        story.append(item)
    
    story.append(PageBreak())
    
    # Error Details
    for i, (key, error) in enumerate(knowledge_base.items(), 1):
        # Error number and name
        story.append(Paragraph(
            f"#{i} {error['error_name']}", 
            styles['ErrorName']
        ))
        
        # Description
        story.append(Paragraph("<b>Description:</b>", styles['SectionHeader']))
        story.append(Paragraph(error['description'], styles['Normal']))
        
        # Resolution
        story.append(Paragraph("<b>Resolution:</b>", styles['SectionHeader']))
        story.append(Paragraph(error['resolution'], styles['Normal']))
        
        # Commands
        story.append(Paragraph("<b>Debugging Commands:</b>", styles['SectionHeader']))
        
        for cmd in error['commands']:
            story.append(Paragraph(f"<code>{cmd}</code>", styles['Normal']))
        
        story.append(Spacer(1, 0.2*inch))
        
        # Page break between errors (except last)
        if i < len(knowledge_base):
            story.append(PageBreak())
    
    # Build PDF
    try:
        doc.build(story)
        print(f"✅ Master PDF created: {filename}")
        return True
    except Exception as e:
        print(f"❌ Error creating master PDF: {e}")
        return False

# ============================================
# INDIVIDUAL ERROR PDFs
# ============================================

def generate_individual_pdfs():
    """Generate individual PDF for each error"""
    
    styles = get_styles()
    
    for key, error in knowledge_base.items():
        filename = f"KB_Error_{error['error_name'].replace(' ', '_').replace(':', '').replace('(', '').replace(')', '')}.pdf"
        
        doc = SimpleDocTemplate(filename, pagesize=letter,
                               rightMargin=0.5*inch, leftMargin=0.5*inch,
                               topMargin=0.75*inch, bottomMargin=0.75*inch)
        
        story = []
        
        # Header
        story.append(Paragraph(error['error_name'], styles['CustomTitle']))
        story.append(Spacer(1, 0.1*inch))
        
        # Metadata
        meta = Paragraph(
            f"<b>Error Key:</b> {key}<br/>"
            f"<b>Generated:</b> {datetime.now().strftime('%B %d, %Y')}<br/>"
            f"<b>Type:</b> Kubernetes/DevOps Error",
            styles['Normal']
        )
        story.append(meta)
        story.append(Spacer(1, 0.2*inch))
        
        # Description
        story.append(Paragraph("What Does This Error Mean?", styles['SectionHeader']))
        story.append(Paragraph(error['description'], styles['Normal']))
        story.append(Spacer(1, 0.15*inch))
        
        # Resolution
        story.append(Paragraph("How to Fix It?", styles['SectionHeader']))
        story.append(Paragraph(error['resolution'], styles['Normal']))
        story.append(Spacer(1, 0.15*inch))
        
        # Debugging Commands
        story.append(Paragraph("Debugging Commands", styles['SectionHeader']))
        story.append(Spacer(1, 0.05*inch))
        
        for i, cmd in enumerate(error['commands'], 1):
            story.append(Paragraph(f"<b>Step {i}:</b>", styles['SectionHeader']))
            story.append(Paragraph(f"<code>{cmd}</code>", styles['Normal']))
            story.append(Spacer(1, 0.05*inch))
        
        story.append(Spacer(1, 0.2*inch))
        
        # Footer
        footer = Paragraph(
            "<b>Quick Tip:</b> Always check logs first with 'kubectl logs &lt;pod-name&gt;' "
            "to get more context about what went wrong.",
            styles['Normal']
        )
        story.append(footer)
        
        # Build PDF
        try:
            doc.build(story)
            print(f"✅ Individual PDF created: {filename}")
        except Exception as e:
            print(f"❌ Error creating {filename}: {e}")

# ============================================
# CSV EXPORT
# ============================================

def generate_csv():
    """Generate CSV file for spreadsheet import"""
    import csv
    
    filename = "KB_Errors.csv"
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow(['#', 'Error Name', 'Error Key', 'Description', 'Resolution', 'Commands'])
            
            # Data rows
            for i, (key, error) in enumerate(knowledge_base.items(), 1):
                writer.writerow([
                    i,
                    error['error_name'],
                    key,
                    error['description'],
                    error['resolution'],
                    ' | '.join(error['commands'])
                ])
        
        print(f"✅ CSV file created: {filename}")
        return True
    except Exception as e:
        print(f"❌ Error creating CSV: {e}")
        return False

# ============================================
# JSON EXPORT
# ============================================

def generate_json():
    """Export knowledge base as JSON"""
    import json
    
    filename = "KB_Errors.json"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(knowledge_base, f, indent=2)
        
        print(f"✅ JSON file created: {filename}")
        return True
    except Exception as e:
        print(f"❌ Error creating JSON: {e}")
        return False

# ============================================
# MAIN EXECUTION
# ============================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("KNOWLEDGE BASE PDF GENERATOR")
    print("="*70)
    print(f"\nProcessing {len(knowledge_base)} errors from knowledge base...\n")
    
    # Check if reportlab is installed
    try:
        import reportlab
        print(f"✅ reportlab {reportlab.Version} is available\n")
    except ImportError:
        print("❌ reportlab not installed. Install with: pip install reportlab")
        print("Skipping PDF generation...\n")
    
    # Generate files
    print("Generating PDF files...\n")
    generate_master_pdf()
    generate_individual_pdfs()
    
    print("\nGenerating additional export formats...\n")
    generate_csv()
    generate_json()
    
    print("\n" + "="*70)
    print("GENERATION COMPLETE!")
    print("="*70)
    print("\nGenerated Files:")
    print("  1. KB_Master_All_Errors.pdf - Complete knowledge base in one file")
    print("  2. KB_Error_*.pdf - Individual PDF files for each error")
    print("  3. KB_Errors.csv - Spreadsheet compatible format")
    print("  4. KB_Errors.json - JSON format for programmatic access")
    print("\n" + "="*70)

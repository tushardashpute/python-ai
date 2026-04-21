#!/usr/bin/env python3
"""
Simple Knowledge Base to PDF Converter
Creates a single PDF file from the knowledge base
"""

import sys
sys.path.insert(0, '.')
from error_resolution_assistant import knowledge_base
from datetime import datetime

# Try to import fpdf2
try:
    from fpdf import FPDF
    FPDF_AVAILABLE = True
except ImportError:
    FPDF_AVAILABLE = False
    print("⚠️  fpdf2 not available, trying alternative method...")

def create_pdf_with_fpdf2():
    """Create PDF using fpdf2 library with simple, tested layout"""
    if not FPDF_AVAILABLE:
        return False
    
    try:
        pdf = FPDF(format="A4")
        pdf.add_page()
        
        # Use helvetica (safe default font)
        pdf.set_font("helvetica", "B", 16)
        pdf.cell(0, 10, "Error Resolution Knowledge Base", new_x="LMARGIN", new_y="NEXT", align="C")
        
        pdf.set_font("helvetica", "", 9)
        pdf.cell(0, 6, f"Generated: {datetime.now().strftime('%B %d, %Y at %H:%M')}", new_x="LMARGIN", new_y="NEXT", align="C")
        pdf.cell(0, 6, f"Total Errors: {len(knowledge_base)}", new_x="LMARGIN", new_y="NEXT", align="C")
        pdf.ln(5)
        
        # Add each error
        for i, (key, error) in enumerate(knowledge_base.items(), 1):
            # Error number and name
            pdf.set_font("helvetica", "B", 11)
            pdf.cell(0, 7, f"{i}. {error['error_name']}", new_x="LMARGIN", new_y="NEXT")
            
            # Description
            pdf.set_font("helvetica", "", 9)
            pdf.set_x(20)
            pdf.multi_cell(0, 4, f"Description: {error['description']}")
            
            # Resolution
            pdf.set_x(20)
            pdf.multi_cell(0, 4, f"Resolution: {error['resolution']}")
            
            # Commands
            pdf.set_x(20)
            pdf.cell(0, 4, "Commands:", new_x="LMARGIN", new_y="NEXT")
            
            for cmd in error['commands']:
                pdf.set_x(25)
                pdf.multi_cell(0, 4, f"- {cmd}")
            
            pdf.ln(2)
        
        filename = "KB_Errors_Simple.pdf"
        pdf.output(filename)
        
        import os
        file_size = os.path.getsize(filename)
        print(f"✅ PDF created successfully: {filename}")
        print(f"📄 File size: {file_size / 1024:.2f} KB")
        return True
    
    except Exception as e:
        print(f"❌ Error with fpdf2: {type(e).__name__}: {e}")
        return False

def create_pdf_with_reportlab():
    """Create PDF using reportlab library"""
    try:
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
        from reportlab.lib import colors
        
        filename = "KB_Errors_Simple.pdf"
        doc = SimpleDocTemplate(filename, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=1  # Center
        )
        story.append(Paragraph("Error Resolution Knowledge Base", title_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Metadata
        meta_style = ParagraphStyle(
            'Meta',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.grey,
            alignment=1
        )
        story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y at %H:%M')}", meta_style))
        story.append(Paragraph(f"Total Errors: {len(knowledge_base)}", meta_style))
        story.append(Spacer(1, 0.3*inch))
        
        # Errors
        for i, (key, error) in enumerate(knowledge_base.items(), 1):
            error_title = ParagraphStyle(
                'ErrorTitle',
                parent=styles['Heading2'],
                fontSize=14,
                textColor=colors.HexColor('#d32f2f'),
                spaceAfter=10,
                spaceBefore=10
            )
            story.append(Paragraph(f"{i}. {error['error_name']}", error_title))
            
            content_style = styles['Normal']
            story.append(Paragraph(f"<b>Description:</b> {error['description']}", content_style))
            story.append(Spacer(1, 0.1*inch))
            story.append(Paragraph(f"<b>Resolution:</b> {error['resolution']}", content_style))
            story.append(Spacer(1, 0.1*inch))
            
            story.append(Paragraph("<b>Commands:</b>", content_style))
            for cmd in error['commands']:
                story.append(Paragraph(f"• {cmd}", content_style))
            
            story.append(Spacer(1, 0.2*inch))
        
        doc.build(story)
        print(f"✅ PDF created successfully: {filename}")
        return True
    
    except ImportError as e:
        print(f"⚠️  reportlab not available: {e}")
        return False
    except Exception as e:
        print(f"❌ Error with reportlab: {e}")
        return False

def main():
    print('\n' + '='*70)
    print('SIMPLE KNOWLEDGE BASE TO PDF CONVERTER')
    print('='*70)
    print(f'\nConverting {len(knowledge_base)} errors to PDF...\n')
    
    # Try fpdf2 first (simpler)
    if FPDF_AVAILABLE:
        print("Attempting with fpdf2...")
        if create_pdf_with_fpdf2():
            print('\n' + '='*70)
            print('✅ SUCCESS! PDF file created: KB_Errors_Simple.pdf')
            print('='*70)
            return
    
    # Try reportlab as fallback
    print("Attempting with reportlab...")
    if create_pdf_with_reportlab():
        print('\n' + '='*70)
        print('✅ SUCCESS! PDF file created: KB_Errors_Simple.pdf')
        print('='*70)
        return
    
    # If both fail
    print('\n' + '='*70)
    print('❌ Could not create PDF')
    print('='*70)
    print('\nAlternatives:')
    print('1. Use KB_Errors.html and save as PDF via browser:')
    print('   - Open KB_Errors.html in browser')
    print('   - Press Ctrl+P')
    print('   - Select "Save as PDF"')
    print('\n2. Install PDF libraries:')
    print('   pip install fpdf2')
    print('   or')
    print('   pip install reportlab')

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Export Knowledge Base to Multiple Formats
CSV, JSON, Markdown, HTML, and plain text formats
"""

import json
import csv
from datetime import datetime
import sys
sys.path.insert(0, '.')
from error_resolution_assistant import knowledge_base

# ============================================
# CSV EXPORT
# ============================================

def generate_csv():
    """Generate CSV file for spreadsheet import"""
    
    filename = 'KB_Errors.csv'
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow(['#', 'Error Name', 'Error Key', 'Description', 'Resolution', 'Commands'])
            
            # Data rows
            for i, (key, error) in enumerate(knowledge_base.items(), 1):
                cmd_str = ' | '.join(error['commands'])
                writer.writerow([
                    i,
                    error['error_name'],
                    key,
                    error['description'],
                    error['resolution'],
                    cmd_str
                ])
        
        print(f'✅ CSV file created: {filename}')
        return True
    except Exception as e:
        print(f'❌ Error creating CSV: {e}')
        return False

# ============================================
# JSON EXPORT
# ============================================

def generate_json():
    """Export knowledge base as JSON"""
    
    filename = 'KB_Errors.json'
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(knowledge_base, f, indent=2, ensure_ascii=False)
        
        print(f'✅ JSON file created: {filename}')
        return True
    except Exception as e:
        print(f'❌ Error creating JSON: {e}')
        return False

# ============================================
# MARKDOWN EXPORT
# ============================================

def generate_markdown():
    """Export knowledge base as Markdown"""
    
    filename = 'KB_Errors.md'
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('# Error Resolution Knowledge Base\n\n')
            f.write(f'**Generated:** {datetime.now().strftime("%B %d, %Y at %H:%M")}\n')
            f.write(f'**Total Errors:** {len(knowledge_base)}\n\n')
            
            # Table of Contents
            f.write('## Table of Contents\n\n')
            for i, (key, error) in enumerate(knowledge_base.items(), 1):
                link = error["error_name"].lower().replace(" ", "-").replace(":", "").replace("(", "").replace(")", "")
                f.write(f'{i}. [{error["error_name"]}](#{link})\n')
            
            f.write('\n---\n\n')
            
            # Error Details
            for i, (key, error) in enumerate(knowledge_base.items(), 1):
                f.write(f'## #{i} {error["error_name"]}\n\n')
                f.write(f'**Error Key:** `{key}`\n\n')
                
                f.write('### Description\n\n')
                f.write(f'{error["description"]}\n\n')
                
                f.write('### Resolution\n\n')
                f.write(f'{error["resolution"]}\n\n')
                
                f.write('### Debugging Commands\n\n')
                for j, cmd in enumerate(error['commands'], 1):
                    f.write(f'{j}. ```bash\n   {cmd}\n   ```\n\n')
                
                f.write('---\n\n')
        
        print(f'✅ Markdown file created: {filename}')
        return True
    except Exception as e:
        print(f'❌ Error creating Markdown: {e}')
        return False

# ============================================
# HTML EXPORT (Printable as PDF)
# ============================================

def generate_html():
    """Export knowledge base as HTML (can be saved as PDF via browser)"""
    
    filename = 'KB_Errors.html'
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Error Resolution Knowledge Base</title>
    <style>
        * { margin: 0; padding: 0; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
            padding: 30px;
        }
        h1 {
            color: #1a1a1a;
            text-align: center;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        .metadata {
            text-align: center;
            color: #666;
            font-size: 0.9em;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #eee;
        }
        .toc {
            background: #f5f5f5;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 30px;
        }
        .toc h2 { margin-bottom: 15px; }
        .toc ol { margin-left: 20px; }
        .toc li { margin-bottom: 8px; }
        .error-section {
            margin-bottom: 40px;
            page-break-inside: avoid;
        }
        .error-header {
            background: linear-gradient(135deg, #d32f2f 0%, #c62828 100%);
            color: white;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 15px;
        }
        .error-header h2 {
            font-size: 1.5em;
            margin-bottom: 5px;
        }
        .error-key {
            font-size: 0.9em;
            opacity: 0.9;
        }
        .section-title {
            color: #1976d2;
            font-size: 1.1em;
            font-weight: bold;
            margin-top: 15px;
            margin-bottom: 8px;
            border-left: 4px solid #1976d2;
            padding-left: 10px;
        }
        .description, .resolution {
            background: #f9f9f9;
            padding: 12px;
            border-radius: 3px;
            margin-bottom: 12px;
            border-left: 3px solid #1976d2;
        }
        .commands {
            background: #f5f5f5;
            padding: 15px;
            border-radius: 3px;
            margin-bottom: 12px;
        }
        .command-item {
            background: white;
            padding: 10px;
            margin-bottom: 8px;
            border-left: 3px solid #4CAF50;
            font-family: 'Courier New', monospace;
            font-size: 0.95em;
            word-break: break-all;
        }
        .command-num {
            font-weight: bold;
            color: #4CAF50;
            margin-right: 8px;
        }
        footer {
            text-align: center;
            margin-top: 50px;
            padding-top: 20px;
            border-top: 2px solid #eee;
            color: #999;
            font-size: 0.9em;
        }
        @media print {
            body { background: white; padding: 0; }
            .container { box-shadow: none; padding: 0; }
            .error-section { page-break-inside: avoid; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Error Resolution Knowledge Base</h1>
        <div class="metadata">
            <p><strong>Generated:</strong> ''' + datetime.now().strftime("%B %d, %Y at %H:%M") + '''</p>
            <p><strong>Total Errors:</strong> ''' + str(len(knowledge_base)) + '''</p>
            <p><strong>Version:</strong> 1.0</p>
        </div>
        
        <div class="toc">
            <h2>Table of Contents</h2>
            <ol>
''')
            
            for i, (key, error) in enumerate(knowledge_base.items(), 1):
                f.write(f'                <li>{error["error_name"]}</li>\n')
            
            f.write('''            </ol>
        </div>
        
        <div class="errors">
''')
            
            # Error Details
            for i, (key, error) in enumerate(knowledge_base.items(), 1):
                f.write(f'''
        <div class="error-section">
            <div class="error-header">
                <h2>#{i} {error['error_name']}</h2>
                <div class="error-key">Error Key: <code>{key}</code></div>
            </div>
            
            <div class="section-title">Description</div>
            <div class="description">
                {error['description']}
            </div>
            
            <div class="section-title">Resolution</div>
            <div class="resolution">
                {error['resolution']}
            </div>
            
            <div class="section-title">Debugging Commands</div>
            <div class="commands">
''')
                
                for j, cmd in enumerate(error['commands'], 1):
                    f.write(f'                <div class="command-item"><span class="command-num">Step {j}:</span> {cmd}</div>\n')
                
                f.write('''            </div>
        </div>
''')
            
            f.write('''
        </div>
        
        <footer>
            <p>Error Resolution System v1.0 | For internal use</p>
            <p>To save as PDF: Use your browser's Print function (Ctrl+P) and select "Save as PDF"</p>
        </footer>
    </div>
</body>
</html>
''')
        
        print(f'✅ HTML file created: {filename} (can be saved as PDF via browser)')
        return True
    except Exception as e:
        print(f'❌ Error creating HTML: {e}')
        return False

# ============================================
# PLAIN TEXT EXPORT
# ============================================

def generate_text():
    """Export knowledge base as plain text"""
    
    filename = 'KB_Errors.txt'
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('='*80 + '\n')
            f.write('ERROR RESOLUTION KNOWLEDGE BASE\n')
            f.write('='*80 + '\n\n')
            f.write(f'Generated: {datetime.now().strftime("%B %d, %Y at %H:%M")}\n')
            f.write(f'Total Errors: {len(knowledge_base)}\n')
            f.write(f'Version: 1.0\n\n')
            
            # Table of Contents
            f.write('TABLE OF CONTENTS\n')
            f.write('-'*80 + '\n')
            for i, (key, error) in enumerate(knowledge_base.items(), 1):
                f.write(f'{i}. {error["error_name"]}\n')
            
            f.write('\n' + '='*80 + '\n\n')
            
            # Error Details
            for i, (key, error) in enumerate(knowledge_base.items(), 1):
                f.write(f'ERROR #{i}: {error["error_name"]}\n')
                f.write('-'*80 + '\n')
                f.write(f'Error Key: {key}\n\n')
                
                f.write('DESCRIPTION:\n')
                f.write(f'{error["description"]}\n\n')
                
                f.write('RESOLUTION:\n')
                f.write(f'{error["resolution"]}\n\n')
                
                f.write('DEBUGGING COMMANDS:\n')
                for j, cmd in enumerate(error['commands'], 1):
                    f.write(f'  Step {j}: {cmd}\n')
                
                f.write('\n' + '='*80 + '\n\n')
        
        print(f'✅ Text file created: {filename}')
        return True
    except Exception as e:
        print(f'❌ Error creating Text: {e}')
        return False

# ============================================
# MAIN EXECUTION
# ============================================

if __name__ == "__main__":
    print('\n' + '='*70)
    print('KNOWLEDGE BASE EXPORT GENERATOR')
    print('='*70)
    print(f'\nProcessing {len(knowledge_base)} errors from knowledge base...\n')
    
    print('Generating export files...\n')
    generate_csv()
    generate_json()
    generate_markdown()
    generate_html()
    generate_text()
    
    print('\n' + '='*70)
    print('✅ GENERATION COMPLETE!')
    print('='*70)
    print('\nGenerated Files:')
    print('  1. KB_Errors.csv - Spreadsheet compatible format')
    print('  2. KB_Errors.json - JSON format for programmatic access')
    print('  3. KB_Errors.md - Markdown format for documentation')
    print('  4. KB_Errors.html - HTML format (printable/saveable as PDF)')
    print('  5. KB_Errors.txt - Plain text format')
    print('\nNote: To save KB_Errors.html as PDF:')
    print('  1. Open KB_Errors.html in your browser')
    print('  2. Press Ctrl+P (or Cmd+P on Mac)')
    print('  3. Select "Save as PDF" from printer options')
    print('\n' + '='*70)

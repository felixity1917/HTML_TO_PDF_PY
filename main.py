import os
import sys
from tempfile import TemporaryDirectory
from PyPDF2 import PdfMerger
import argparse
from weasyprint import HTML
import requests

def read_urls_from_file(file_path):
    """Read URLs from a text file, one per line."""
    urls = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    urls.append(line)
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    
    if not urls:
        print("Error: No valid URLs found in the input file")
        sys.exit(1)
    
    return urls

def convert_and_merge(urls, output_path):
    """Convert webpages to PDF and merge them."""
    merger = PdfMerger()
    success_count = 0
    
    with TemporaryDirectory() as temp_dir:
        for i, url in enumerate(urls, 1):
            try:
                print(f"Processing URL {i}/{len(urls)}: {url}")
                temp_pdf = os.path.join(temp_dir, f"temp_{i}.pdf")
                
                # Fetch and render the page
                response = requests.get(url)
                response.raise_for_status()
                
                HTML(string=response.text, base_url=url).write_pdf(temp_pdf)
                merger.append(temp_pdf)
                success_count += 1
                print(f"Successfully converted: {url}")
                
            except Exception as e:
                print(f"Failed to convert {url}: {str(e)}")
                continue
        
        if success_count == 0:
            print("Error: No PDFs were successfully created")
            sys.exit(1)
        
        try:
            merger.write(output_path)
            print(f"\nSuccessfully merged {success_count} PDFs to {output_path}")
        except Exception as e:
            print(f"Error merging PDFs: {e}")
            sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Convert webpages from a text file to a merged PDF.')
    parser.add_argument('input_file', help='Text file containing URLs (one per line)')
    parser.add_argument('output_file', help='Output PDF file path')
    args = parser.parse_args()
    
    urls = read_urls_from_file(args.input_file)
    convert_and_merge(urls, args.output_file)

if __name__ == "__main__":
    # Check dependencies
    try:
        import weasyprint
    except ImportError:
        print("Error: weasyprint not installed. Please install with: pip install weasyprint")
        sys.exit(1)
    
    try:
        import PyPDF2
    except ImportError:
        print("Error: PyPDF2 not installed. Please install with: pip install PyPDF2")
        sys.exit(1)
    
    try:
        import requests
    except ImportError:
        print("Error: requests not installed. Please install with: pip install requests")
        sys.exit(1)
    
    main()

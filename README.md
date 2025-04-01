# HTML_TO_PDF_PY

# Usage
Paste list of links, one on each line in urls.txt and then run the following on the console.
```
python main.py urls.txt output.pdf
```

Obviously, make sure to have python installed along with the following dependencies
```
# Core dependencies
weasyprint==58.1
PyPDF2==3.0.1
requests==2.31.0

# Required dependencies
python-dateutil==2.8.2
cairocffi==1.6.1
cffi==1.16.0
Pillow==10.0.1  # For image handling

# Development/build tools
pyinstaller==6.2.0; sys_platform == 'win32'
pywin32==306; sys_platform == 'win32'
```


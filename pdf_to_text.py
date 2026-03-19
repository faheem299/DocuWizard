from PyPDF2 import PdfReader

#PDFs are converted to text data

def pdfToText(files):

    if isinstance(files, str):
        files = [files]

    

    all_text=""
    for path in files:

    
        reader = PdfReader(f"{path}")
        for page in reader.pages:
                t = page.extract_text()
                if t:
                    all_text+=t
        all_text = all_text.replace('\n', ' ').replace('\r', ' ')
        all_text = ' '.join(all_text.split())
        print("converted from pdf to text...")
    return all_text
                    



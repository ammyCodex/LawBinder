from flask import Flask, render_template, request, send_file
from PyPDF2 import PdfMerger
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

app = Flask(__name__)

def create_index(pdf_files):
    index_pdf = BytesIO()
    c = canvas.Canvas(index_pdf, pagesize=letter)
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, 750, "INDEX")
    c.setFont("Helvetica", 10)

    y = 730
    sl_no = 1
    current_page = 1
    
    c.drawString(100, y, "Sl No")
    c.drawString(150, y, "Particulars of Documents")
    c.drawString(350, y, "Page No of Part")
    c.drawString(450, y, "Remarks")
    
    y -= 20
    c.drawString(100, y, "")
    c.drawString(350, y, "Part I")
    c.drawString(400, y, "Part II")
    
    y -= 20
    
    for pdf_file in pdf_files:
        filename = pdf_file.filename
        c.drawString(100, y, str(sl_no))
        c.drawString(150, y, filename)
        c.drawString(350, y, str(current_page))
        c.drawString(400, y, "-")
        c.drawString(450, y, "-")
        
        sl_no += 1
        current_page += 10  # Placeholder increment, adjust as per the actual number of pages
        
        y -= 20
        if y < 50:
            c.showPage()
            y = 750
    
    c.save()
    index_pdf.seek(0)
    return index_pdf

def merge_pdfs(pdf_files, index_pdf):
    merger = PdfMerger()

    if index_pdf:
        merger.append(index_pdf)

    for pdf in pdf_files:
        merger.append(BytesIO(pdf.read()))

    merged_pdf = BytesIO()
    merger.write(merged_pdf)
    merged_pdf.seek(0)
    merger.close()
    return merged_pdf

@app.route('/', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'POST':
        files = request.files.getlist('pdf_files')
        index_pdf = create_index(files)
        merged_pdf = merge_pdfs(files, index_pdf)

        return send_file(merged_pdf, as_attachment=True, download_name="merged_output.pdf", mimetype='application/pdf')
    
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)

import os
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas

CHUNK_SIZE = 1024 * 1024
cur_size = 0
MAX_SIZE = 10 * 1024 * 1024  # 10 mb
cur_idx = 0
cur_pdf = None
FMT = ".%d.pdf"
input_xml_file = '/mnt/datastore/wikipedia/enwiki-20231220-pages-articles-multistream.xml'
output_directory = '/mnt/datastore/wikipedia/wikichunks_pdf'

def create_new_pdf():
    """Create a new PDF file"""
    global cur_pdf, cur_idx
    cur_pdf = canvas.Canvas(os.path.join(output_directory, FMT % cur_idx), pagesize=LETTER)
    cur_pdf.setFont("Helvetica", 10)

def next_file():
    """Close the current PDF file and start a new one"""
    global cur_size, cur_pdf, cur_idx
    if cur_size > MAX_SIZE:
        print("Part %d done" % cur_idx)
        cur_pdf.save()
        cur_size = 0
        cur_idx += 1
        create_new_pdf()

def main():
    try:
        global cur_pdf, cur_idx, cur_size

        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        create_new_pdf()

        text = ""
        with open(input_xml_file, 'rt', encoding='utf-8') as xml_file:
            while True:
                chunk = xml_file.read(CHUNK_SIZE)
                if len(chunk) < CHUNK_SIZE:
                    text += chunk
                    break
                text += chunk
                cur_size += len(chunk)
                next_file()

        # Write remaining text to the last PDF
        if text:
            text_lines = text.split('\n')
            y = 750
            for line in text_lines:
                cur_pdf.drawString(30, y, line)
                y -= 12
                if y < 30:
                    cur_pdf.showPage()
                    cur_pdf.setFont("Helvetica", 10)
                    y = 750
            cur_pdf.save()
        print("Part %d done" % cur_idx)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

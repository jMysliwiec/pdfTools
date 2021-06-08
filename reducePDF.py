import sys

from PyPDF2 import PdfFileReader, PdfFileWriter
import re


def deduplicate_pdf(input_file_path, output_file_path=""):
    if output_file_path == "":
        base, _, file = input_file_path.rpartition('/')
        if base == '':  # take empty base path into account
            base = '.'
        name, _, extensions = file.partition('.')
        output_file_path = f'{base}/{name}_reduced.{extensions}'

    with open(input_file_path, 'rb') as f:
        pdf_reader = PdfFileReader(f)  # original slides
        pdf_writer = PdfFileWriter()

        last_seen = 0
        last_page = pdf_reader.getPage(0)
        for i in range(1, pdf_reader.numPages):
            page = pdf_reader.getPage(i)
            search_slide = re.search(r'(?<=slide)(\d\n)+', page.extractText())
            if search_slide is not None:
                number = int(search_slide.group(0).replace('\n', ''))
                if number != last_seen:
                    pdf_writer.addPage(last_page)
                    last_seen = number
            else:
                pdf_writer.addPage(last_page)
                last_seen = -1
            last_page = page

        pdf_writer.addPage(last_page)  # add last page

        print("done extracting")

        with open(output_file_path, 'wb') as out:
            pdf_writer.write(out)

        print(f"Slide deck of {pdf_reader.numPages} slides reduced to {pdf_writer.getNumPages()} slides")


if __name__ == '__main__':
    deduplicate_pdf(*sys.argv[1:])

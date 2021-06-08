import sys

from PyPDF2 import PdfFileReader, PdfFileWriter


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

        # last_seen = 0
        last_page = pdf_reader.getPage(0)
        text_on_last_page = set(last_page.extractText().split())

        for i in range(1, pdf_reader.numPages):
            page = pdf_reader.getPage(i)
            text_on_page = set(page.extractText().split())
            for part in text_on_last_page:
                if part not in text_on_page:  # is this is a new page
                    pdf_writer.addPage(last_page)
                    break

            text_on_last_page = text_on_page
            last_page = page

        pdf_writer.addPage(last_page)  # add last page

        print("done extracting")

        with open(output_file_path, 'wb') as out:
            pdf_writer.write(out)

        print(f"Slide deck of {pdf_reader.numPages} slides reduced to {pdf_writer.getNumPages()} slides")


if __name__ == '__main__':
    deduplicate_pdf(*sys.argv[1:])

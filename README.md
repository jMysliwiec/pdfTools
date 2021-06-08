# Reduce pdf file

reducePDF.py deletes redundant slides from a slide deck. Often, in decks exported to PDF, multiple pages are dedicated to the same slide, because sentences pop up one after another. This program deletes the uncomplete pages.


## Limitations

This code was written for extracting the last slide with a certain number. It only works when the slide contains the string "slide <number>".

## Usage
### Dependencies

To use the code, you need the following libraries
- PyPDF2

### Run

```
./reducePDF.py "filepath of the initial slide deck" "filepath where you want to save the reduced slide deck"
```
The last argument is optional. If you don't give an output filepath, the new slides will be saved in {filepath}_reduced.pdf.
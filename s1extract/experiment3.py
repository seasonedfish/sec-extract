"""
It just skips over the annotations since they're not links
"""
from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser


def get_overlapping_link(annotations, element):
    for (x0, y0, x1, y1), url in annotations:
        if x0 > element.x1 or element.x0 > x1:
            continue
        if y0 > element.y1 or element.y0 > y1:
            continue
        return url
    else:
        return None


output_string = StringIO
with open("AAOI.pdf", "rb") as in_file:
    parser = PDFParser(in_file)
    doc = PDFDocument(parser)
    resource_manager = PDFResourceManager()
    device = TextConverter(resource_manager, output_string, laparams=LAParams())
    interpreter = PDFPageInterpreter(resource_manager, device)
    pages = PDFPage.create_pages(doc)

    page = pages.__next__()

    annotation_list = []
    if page.annots:
        for annotation in page.annots.resolve():
            annotationDict = annotation.resolve()
            if str(annotationDict["Subtype"]) != "/Link":
                # Skip over any annotations that are not links
                continue
            position = annotationDict["Rect"]
            uriDict = annotationDict["A"].resolve()
            # This has always been true so far.
            assert str(uriDict["S"]) == "/URI"
            # Some of my URI's have spaces.
            uri = uriDict["URI"].replace(" ", "%20")
            annotation_list.append((position, uri))

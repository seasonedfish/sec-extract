from PyPDF2 import PdfFileReader

reader = PdfFileReader("AAOI.pdf")

page1 = reader.pages[0]

if "/Annots" in page1:
    for annot in page1["/Annots"]:
        obj = annot.getObject()

        subtype = obj["/Subtype"]
        if subtype == "/Link":
            print("has link!")
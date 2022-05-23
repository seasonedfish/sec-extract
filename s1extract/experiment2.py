import pikepdf
pdf_file = pikepdf.Pdf.open("AAOI.pdf")
urls = []
for page in pdf_file.pages:
    for annots in page.get("/Annots"):
        url=annots.get("/A").get("/URI")
        if url is not None:
            urls.append(url)
            urls.append(" ; ")
print(urls)

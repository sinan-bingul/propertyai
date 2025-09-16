import pymupdf
from logger import logging 

class TranscribeDocument():
    def __init__(self):
        pass

    def run(self, path: str):
        doc = pymupdf.open(path)
        logging.info(f"Number of pages: {doc.page_count}")
        logging.info(f"First page text: {doc.get_page_text(1)}")
        
if __name__ == "__main__":
    pipeline = TranscribeDocument()
    output = pipeline.run('data/contracts/contract_chelsea.pdf')
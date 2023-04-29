import PyPDF2
import re

class Reader:
    def __init__(self, path):
        self.path = path
    
    def readPdf(self):
        try:
            # open file
            with open(self.path, 'rb') as pdf_file:
                # read file
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                # get number of pages
                num_pages = len(pdf_reader.pages)
                # get page
                page = pdf_reader.pages[0]
                # extract text
                text = page.extract_text()
                # get title
                
                return text

                start = 'ABSTRAK'
                end = 'Kata kunci :'

                result = text[text.find(start)+len(start):text.find(end)].strip()

                return result

                # text_split = text.split('ABSTRAK', 1)[1] # membuang text sebelum "ABSTRAK"
                # text_split = text.split('Kata kunci', 1)[0] # membuang text setelah "Kata kunci"
                # text_split = text.strip() # menghilangkan spasi tambahan di awal atau akhir text
                
                start = 'Kata kunci :'
                end = '1. Pendahuluan'

                result = text[text.find(start)+len(start):text.find(end)].strip()

                return result
        except Exception as e:
            return e
        finally:
            pdf_file.close()

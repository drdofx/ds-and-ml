import PyPDF2
import re

class Reader:
    def __init__(self, path):
        self.path = path
    
    def extractOld(self, text):
        # get title
        regex = r"\d\s+\b[A-Z]+(?:\s+[A-Z()\d]+)*\b"
        title = re.findall(regex, text)[0].lstrip('1234567890 ')

        # find abstract with ignoring case
        start = 'ABSTRAK'
        end = 'Kata kunci'

        abstract = text[text.lower().find(start.lower())+len(start):text.lower().find(end.lower())].strip()
        
        # find keywords with ignoring case
        start2 = 'Kata kunci'
        end2 = '1.'

        keywords = text[text.lower().find(start2.lower())+len(start2):text.lower().find(end2.lower())].strip()
            
        return {
            'title': title,
            'abstract': abstract,
            'keywords': keywords
        }

    def extractNew(self, text):
        # find title
        start = 'https://ojs.unikom.ac.id/index.php/komputika'
        start_pos = text.lower().find(start.lower()) + len(start)

        end_pos = start_pos
        while True:
            end_pos = text.find('\n', end_pos) + 1  # move to next line
            if text[end_pos:end_pos+1].isspace():  # check if the next line is empty
                break

        title = ' '.join(text[start_pos:end_pos].strip().split())

        # find abstract with ignoring case
        start = 'ABSTRAK'
        end = 'Kata kunci'

        abstract = text[text.lower().find(start.lower())+len(start):text.lower().find(end.lower())].strip()
        
        # find keywords with ignoring case
        start = 'Kata Kunci'
        start_pos = text.lower().find(start.lower()) + len(start)

        end_pos = start_pos
        while True:
            end_pos = text.find('\n', end_pos) + 1  # move to next line
            if not text[end_pos:end_pos+1].isspace():  # check if the next line is not empty
                break

        keywords = text[start_pos:end_pos].strip()

        return {
            'title': title,
            'abstract': abstract,
            'keywords': keywords
        }

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

                # extract text from old format if file is 1-313.pdf, else extract text from new format
                if int(self.path.split('/')[-1].split('.')[0]) <= 313:
                    extracted = self.extractOld(text)
                else:
                    extracted = self.extractNew(text)

                # close file
                pdf_file.close()

                return extracted

        except Exception as e:
            return

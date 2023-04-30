import PyPDF2
import re

class Reader:
    def __init__(self, store, articles):
        self.store = store
        self.articles = articles

        if len(self.articles) == 0:
            print("Articles not scraped yet!\n")
            return False

        self.extracted = {}
        self.extracted_count = 0

        # set old_format pdf from Vol 1 No 1 (2012) to Vol 6 No 1 (2017)
        self.old_format = ['Vol 1 No 1 (2012)', 'Vol 1 No 2 (2012)', 'Vol 2 No 1 (2013)', 'Vol 2 No 2 (2013)', 'Vol 3 No 1 (2014)', 'Vol 6 No 1 (2017)']
    
    def extractOld(self, text):
        # get title
        # regex = r"\d\s+\b[A-Z]+(?:\s+[A-Z()\-\d]+)*\b"
        regex = r"\b[A-Z]+(?:\s+[A-Z()\-\d]+)*\b"
        title = re.findall(regex, text)[0].lstrip('1234567890 ').replace('\n', '')

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
        start = 'index.php/komputika'
        start_pos = text.lower().find(start.lower()) + len(start)

        end_pos = start_pos
        while True:
            end_pos = text.find('\n', end_pos) + 1  # move to next line
            if text[end_pos:end_pos+1].isspace():  # check if the next line is empty
                break

        title = ' '.join(text[start_pos:end_pos].strip().split())

        # if title contains 'Copyright' or 'Terakreditasi', just set it to '' (extract title failed)
        if 'Copyright' in title or 'Terakreditasi' in title:
            title = ''

        # find abstract with ignoring case
        start = 'ABSTRAK'
        end = 'Kata kunci'

        abstract = text[text.lower().find(start.lower())+len(start):text.lower().find(end.lower())].replace('\n', '').replace('\u2013', '').strip()
        
        # find keywords with ignoring case
        start = 'Kata Kunci'
        start_pos = text.lower().find(start.lower()) + len(start)

        end_pos = start_pos
        while True:
            end_pos = text.find('\n', end_pos) + 1  # move to next line
            if not text[end_pos:end_pos+1].isspace():  # check if the next line is not empty
                break

        keywords = text[start_pos:end_pos].replace('\u2013', '').strip()

        return {
            'title': title,
            'abstract': abstract,
            'keywords': keywords
        }

    def readPdf(self):
        for issue_name in self.articles:
            if issue_name in self.old_format:
                old_format = True
            else:
                old_format = False

            for article in self.articles[issue_name]:
                # get file_name
                file_path = article['file_path']

                # read article file
                extracted = self.readPdfProcess(file_path, old_format)

                # add extracted text to extracted.json
                file_name = file_path.split('/')[-1]
                self.extracted[file_name] = {
                    'actual_title': article['article_name'],
                    'extracted_title': extracted['title'],
                    'abstract': extracted['abstract'],
                    'keywords': extracted['keywords']
                }

                # add count
                self.extracted_count += 1

            # print progress
            print(f"{self.extracted_count} pdf extracted so far...\n")

            # write to extracted.json after each issue
            store_json = self.store.storeJson(self.extracted, 'output/json/extracted.json')

            print(f"succesfully extracted text from pdf in {issue_name}!\n")

        print(f"Total {self.extracted_count} pdf extracted!\n")

        export_excel = self.store.exportExcel(self.extracted, 'output/excel/extracted.xlsx')
        return export_excel

    def readPdfProcess(self, file_path, old_format):
        try:
            # open file
            with open(file_path, 'rb') as pdf_file:
                # read file
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                # get number of pages
                num_pages = len(pdf_reader.pages)
                # get page
                page = pdf_reader.pages[0]
                # extract text
                text = page.extract_text()

                # extract text from old format if old_format is True
                if old_format:
                    extracted = self.extractOld(text)
                else:
                    extracted = self.extractNew(text)

                # close file
                pdf_file.close()

                return extracted

        except Exception as e:
            print(f"Error while reading file: {e}\n")
            return

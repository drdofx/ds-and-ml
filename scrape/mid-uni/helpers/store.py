import json
import xlsxwriter

class Store:
    def __init__(self):
        pass

    def storeJson(self, data, filename):
        try:
            # save to json file in this directory
            with open(filename, 'w') as outfile:
                json.dump(data, outfile, indent=4)

            return True
        except Exception as e:
            return False
        
    def checkFileExists(self, filename):
        try:
            # open file
            with open(filename, 'r'):
                return True
        except Exception as e:
            return False


    def exportExcel(self, data, filename):
        try:
            workbook = xlsxwriter.Workbook(filename)
            bold = workbook.add_format({'bold': True})
            title = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'font_size': 18, 'bold': True})
            each_data = workbook.add_format({'text_wrap': True, 'align': 'justify', 'valign': 'top'})

            # create worksheet
            worksheet = workbook.add_worksheet('Komputika')
            worksheet.set_column('A:A', 5)
            worksheet.set_column('B:B', 10)
            worksheet.set_column('C:C', 30)
            worksheet.set_column('D:D', 30)
            worksheet.set_column('E:E', 70)
            worksheet.set_column('F:F', 30)
            worksheet.set_row(0, 30)
            worksheet.merge_range(0, 0, 0, 5, 'Komputika: Jurnal Sistem Komputer', title)
            worksheet.write(1, 0, 'No', bold)
            worksheet.write(1, 1, 'Nama File', bold)
            worksheet.write(1, 2, 'Judul Asli', bold)
            worksheet.write(1, 3, 'Judul Hasil Ekstraksi', bold)
            worksheet.write(1, 4, 'Abstrak', bold)
            worksheet.write(1, 5, 'Kata Kunci', bold)

            # loop through data dict
            for index, (key, value) in enumerate(data.items()):
                worksheet.set_row(index + 2, 150)
                worksheet.write(index + 2, 0, index + 1, each_data)
                worksheet.write(index + 2, 1, key, each_data)
                worksheet.write(index + 2, 2, value['actual_title'], each_data)
                worksheet.write(index + 2, 3, value['extracted_title'], each_data)
                worksheet.write(index + 2, 4, value['abstract'], each_data)
                worksheet.write(index + 2, 5, value['keywords'], each_data)

            workbook.close()

            return
        except Exception as e:
            return e
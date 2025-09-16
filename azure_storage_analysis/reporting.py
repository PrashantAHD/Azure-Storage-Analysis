# Reporting and Excel/CSV export logic for Azure Storage Analysis

# ...reporting and export functions will be moved here...

import os
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
import csv

def add_watermark_to_sheet(sheet, watermark_text):
    row = sheet.max_row + 2
    cell = sheet.cell(row=row, column=1)
    cell.value = watermark_text
    cell.font = Font(italic=True, color="888888", size=10)
    cell.alignment = Alignment(horizontal="left", vertical="center")

def save_excel_with_watermark(workbook, output_file, watermark_text):
    for sheet in workbook.worksheets:
        add_watermark_to_sheet(sheet, watermark_text)
    workbook.save(output_file)

def save_csv_with_watermark(rows, output_file, watermark_text):
    with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([watermark_text])
        writer.writerow([])
        for row in rows:
            writer.writerow(row)

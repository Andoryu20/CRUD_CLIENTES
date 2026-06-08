import csv
import openpyxl
import xlwt 

def create_csv_test():
    filename = "test_clients.csv"
    headers = ["name_client", "city", "country_id", "category_id", "is_active"]
    rows = [
        ["Juan Perez", "Bogota", 1, 1, 1],
        ["Maria Gomez", "Medellin", 2, 2, 1],
        ["Carlos 123", "Bogota", 1, 1, 1],
        ["Ana Torroja", "Fusagasuga", 1, 1, 1],
        ["Luis Torres", "Madrid", 99, 1, 1]
    ]
    
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    print(f"✅ Created: {filename}")

def create_xlsx_test():
    filename = "test_clients.xlsx"
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Clients"
    
    headers = ["name_client", "city", "country_id", "category_id", "is_active"]
    ws.append(headers)
    
    rows = [
        ["Pedro Nelson", "Guadalajara", 2, 3, 1],   
        ["Laura Chimpu", "Barcelona", 3, 4, 1],
        ["Sergio Gonzalez", "Madrid", 3, 1, 1],
        ["Karen 45", "Bogota", 1, 2, 1],
        ["Diana Prince", "Gotham", 1, 1, 1]
    ]
    
    for row in rows:
        ws.append(row)
        
    wb.save(filename)
    print(f"✅ Created: {filename}")

def create_xls_test():
    filename = "test_clients.xls"
    wb = xlwt.Workbook()
    ws = wb.add_sheet("Clients")
    
    headers = ["name_client", "city", "country_id", "category_id", "is_active"]
    for col_idx, text in enumerate(headers):
        ws.write(0, col_idx, text)
        
    rows = [
        ["Andres Cubillos", "Buenos Aires", 4, 2, 1],
        ["Alexa Jimenez", "Cordoba", 4, 1, 1],  
        ["Johan C3PO", "Bogota", 1, 1, 1],
    ]
    
    for row_idx, row in enumerate(rows, start=1):
        for col_idx, value in enumerate(row):
            ws.write(row_idx, col_idx, value)
            
    wb.save(filename)
    print(f"✅ Created: {filename}")

if __name__ == "__main__":
    print("Generating test files...")
    create_csv_test()
    create_xlsx_test()
    try:
        create_xls_test()
    except ImportError:
        print("Installing xlwt to generate old .xls format...")
        import os
        os.system("pip install xlwt")
        create_xls_test()
    print("All test files generated successfully!")
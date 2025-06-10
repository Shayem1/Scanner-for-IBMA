import os
import xlsxwriter

WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def process_txt_to_xlsx(filename):
    base_name = os.path.splitext(filename)[0]
    xlsx_filename = base_name + ".xlsx"

    with open(filename, "r") as file:
        lines = file.readlines()

    data = []
    for line in lines:
        parts = line.strip().rsplit(" ", 1)
        if len(parts) == 2:
            code = parts[1].strip()
            if code:
                data.append(code)

    workbook = xlsxwriter.Workbook(xlsx_filename)
    worksheet = workbook.add_worksheet()

    # Header row: (0,0) is blank, (0,1) is "id"
    worksheet.write(0, 1, "id")

    # Write data starting at row 1
    for row_num, code in enumerate(data, start=1):
        worksheet.write(row_num, 0, row_num + 1)  # IDs starting from 2
        worksheet.write(row_num, 1, code)

    workbook.close()
    print(f"✓ Processed: {filename} -> {xlsx_filename}")

def main():
    txt_files = [f for f in os.listdir(".")
                 if f.endswith(".txt") and any(f.startswith(day) for day in WEEKDAYS)]

    if not txt_files:
        print("No weekday-named .txt files found in the current directory.")
        return

    for txt_file in txt_files:
        process_txt_to_xlsx(txt_file)

if __name__ == "__main__":
    main()



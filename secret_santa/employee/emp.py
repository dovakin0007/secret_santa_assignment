from typing import List
import openpyxl


class Employee:
    def __init__(self, name: str, email: str):
        self.emp_name = name
        self.emp_id = email

    def __repr__(self):
        return f"Employee(name={self.emp_name!r}, email={self.emp_id!r})"

    @staticmethod
    def read_employee_data(file_path: str) -> List["Employee"]:
        wb = openpyxl.load_workbook(file_path)
        sheet = wb.active
        headers = [cell.value for cell in sheet[1]]
        name_col = headers.index("Employee_Name")
        email_col = headers.index("Employee_EmailID")
        employees = []
        for row in sheet.iter_rows(min_row=2):
            name = row[name_col].value
            email = row[email_col].value
            employees.append(Employee(name=name, email=email))

        return employees

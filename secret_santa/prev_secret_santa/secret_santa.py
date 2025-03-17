from typing import List
import openpyxl


class PreviousSecretSanta:
    def __init__(self, giver_name: str, giver_email: str, receiver_name: str, receiver_email: str):
        self.giver_name = giver_name
        self.giver_email = giver_email
        self.receiver_name = receiver_name
        self.receiver_email = receiver_email

    def __repr__(self):
        return f"SecretSantaPair({self.giver_name!r} -> {self.receiver_name!r})"

    @staticmethod
    def read_secret_santa_data(file_path: str) -> List["PreviousSecretSanta"]:
        wb = openpyxl.load_workbook(file_path, data_only=True)
        sheet = wb.active
        headers = [cell.value for cell in sheet[1] if cell.value]
        giver_col = headers.index("Employee_Name")
        giver_email_col = headers.index("Employee_EmailID")
        receiver_col = headers.index("Secret_Child_Name")
        receiver_email_col = headers.index("Secret_Child_EmailID")

        pairs = []
        for row in sheet.iter_rows(min_row=2, values_only=True):
            giver_name, giver_email = row[giver_col], row[giver_email_col]
            receiver_name, receiver_email = row[receiver_col], row[receiver_email_col]

            pairs.append(PreviousSecretSanta(
                giver_name, giver_email, receiver_name, receiver_email))

        wb.close()
        return pairs

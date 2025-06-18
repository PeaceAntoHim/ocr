import pandas as pd

class ExcelHandler:
    """Handles Excel to JSON conversion"""

    @staticmethod
    def extract_data_from_excel(excel_path):
        """Read Excel file and convert it to JSON"""
        df = pd.read_excel(excel_path)
        return df.to_dict(orient="records")
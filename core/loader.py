import pandas as pd

class DataAction:

    def load_data(self):
        try:
            file_path = "../data/online_retail_II.xlsx"
            excel_file = pd.ExcelFile(file_path)
            sheet_names = excel_file.sheet_names

            df_list =[]


            # Read Data
            for sheet_no,sheet_name in enumerate(sheet_names):
                df =pd.read_excel(file_path, sheet_name=sheet_name)
                df_list.append(df)

            df = pd.concat([df_list[0], df_list[1]], ignore_index=True)


            # Cleaning and feature engineering
            df = df.dropna(subset=["Customer ID", "Description"])
            df = df[~df['Invoice'].astype(str).str.startswith("C")]
            df = df[df["Quantity"] > 0]
            df = df[df["Price"] > 0] 
            df["Reveue"] = df["Price"] * df["Quantity"]
            df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
            df["Month"] = df["InvoiceDate"].dt.to_period("M").astype(str)
            return df



        except Exception as e:
            print(str(e))


# da_obj = DataAction()
# da_obj.load_data()
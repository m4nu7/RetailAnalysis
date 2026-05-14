from core.standard import AnalysisStd
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import json

import requests
from bs4 import BeautifulSoup
import pandas as pd

class Analysis(AnalysisStd):

    def __init__(self, file_path):
        self.file_path = file_path
        self.url = r"https://archive.ics.uci.edu/dataset/352/online+retail"

        # Document Setup
        self.doc = SimpleDocTemplate(
            file_path,
            pagesize = A4,
            ritghtMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40
        )

        self.styles = getSampleStyleSheet()
        self.story = []


        # Custom Heading style
        self.heading_style = ParagraphStyle("Heading1",
                       parent=self.styles["Heading1"],
                       fontSize=20,
                       spaceAfter=12,
                       spaceBefore=12
        ) 


    def web_scrap(self):
        # Download the webpage
        response = requests.get(self.url)

        # Convert Raw html string to html parser tree
        soup = BeautifulSoup(response.text, "html.parser")

        # Get the dataset details 
        metadata = {}

        # Description
        info_section = soup.find("div", {"class" : "relative flex flex-col gap-4 bg-base-100 p-4 shadow"})
        full_text = info_section.get_text(" ", strip=True)  # " " ensures paragraphs don't get smashed together
        first_sentence = full_text.split(".")[0] + "."
        metadata["description"] = first_sentence


        # Dataset info
        dataset_info = {}
        for info in soup.find_all("div", {"class" : "col-span-4"}):
            key = info.h1.get_text(strip=True)
            value = info.p.get_text(strip=True)
            dataset_info[key] = value
        
        metadata["dataset_info"] = dataset_info


        # Table info using scrapping
        table = soup.find("table")
        header_keys = []
        values = []

        if table:
            for row in table.find_all("tr"):
                cols = row.find_all("th")

                if len(cols) == 6:
                    for i in range(len(cols)):
                        key = cols[i].get_text(strip=True)
                        header_keys.append(key)

            
            for row in table.find_all("tr"):
                cols = row.find_all("td")

                if len(cols) == 6:
                    data = []
                    for i in range(len(cols)):
                        value = cols[i].get_text(strip=True)
                        data.append(value)
                    values.append(data)



            table_data = {(zip(header_keys,row_data)) for row_data in values }

            data = []

            for row in table_data:
                data.append(dict(row))

            df = pd.DataFrame(data)

            metadata["df_table"] = df
    
        return metadata











    #=======================================
    # SECTION BUILDERS
    #=======================================

    def add_title(self):
        pass


    def add_description(self):
        pass


    def add_table(self):
        pass

    def add_plot(self):
        pass

    def build(self):
        pass
    
    def run_analysis(self):
        return super().run_analysis()




   



A_obj = Analysis("retill.pdf")
# A_obj.run_analysis()
data_to_load = A_obj.web_scrap()
data_to_load["df_table"] = data_to_load["df_table"].to_dict(orient = "records")

with open("metadata.json", "w") as j_file:
    json.dump(data_to_load, j_file, indent=4)

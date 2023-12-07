import pandas as pd
import json
import sys

class ProductDetails:
    def __init__(self,csv_path,txt_path):
        dictionary = {"product_details": [{"Product ID": "test","Name": "test","Price": "test","In Stock": "Yes/No"}]}
        json_object = json.dumps(dictionary, indent=4)
        with open("my.json", "w") as outfile:
            outfile.write(json_object)
        self.convert_csv_to_json(csv_path)
        self.convert_text_to_json(txt_path)
    
    def search_product_id_in_existing_json_data(self, product_id):
        with open("my.json", 'r+') as json_file:
            file_data = json.load(json_file)
            list_of_values = []
            for i in range(len(file_data["product_details"])):
                list_of_values.append(str(file_data["product_details"][i]["Product ID"]))
            if product_id in list_of_values:
                return True
            else:
                return  False
            
    def send_data_to_json(self, new_data):
        with open("my.json", 'r+') as json_file:
            file_data = json.load(json_file)
            file_data["product_details"].append(new_data)
            json_file.seek(0)
            json.dump(file_data, json_file, indent=4)

    def convert_csv_to_json(self,csv_path):
        csv_data = pd.read_csv(csv_path)
        try:
            csv_row = csv_data.to_dict(orient="records")[0:]
            for row_csv in range(len(csv_row)):
                csv_dict = csv_data.to_dict(orient="records")[0:][row_csv]
                csv_dict["Product ID"]=str(csv_dict["Product ID"])
                csv_prod_id=csv_dict["Product ID"]
                search_status=self.search_product_id_in_existing_json_data(csv_prod_id)
                if search_status==False:
                    self.send_data_to_json(csv_dict)
        except:
            print("The data is not available in the correct format or the csv file is corrupted")

    def convert_text_to_json(self,txt_path):
        with open(txt_path, "r") as txt_file:
            file_content = txt_file.readlines()
            try:
                txt_dict = {}
                counter = 1
                for row in range(len(file_content)):
                    txt_read_data = file_content[row]
                    ldata = txt_read_data.split(":")
                    txt_dict.update({ldata[0]: ldata[1].replace("\n", "").replace(" ", "")})
                    if counter % 4 == 0:
                        text_prod_id=txt_dict["Product ID"]
                        search_status=self.search_product_id_in_existing_json_data(text_prod_id)
                        if search_status==False:
                            self.send_data_to_json(txt_dict)
                        txt_dict = {}
                    counter = counter + 1
            except:
                print("The data is not available in the correct format or the text file is corrupted")




def get_arg():
    arguments = sys.argv[1:]
    try:
        obj=ProductDetails(csv_path=arguments[0],txt_path=arguments[1])
    except:
        obj=ProductDetails(csv_path="csv_test.csv",txt_path="text_test.txt")
get_arg()
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import os
import pandas as pd
import re
import json

load_dotenv()

#define our azure search settings
service_name = "ai-coffee-search"
index_name = "coffee-data-index"
admin_key = os.environ.get("ADMIN_KEY")
if admin_key is None:
    raise ValueError("Admin key not found in environment variables.")
endpoint = f"https://{service_name}.search.windows.net"
credential = AzureKeyCredential(admin_key)

#load the excel data into the dataframe
df = pd.read_excel("data/Coffee-Data.xlsx")

# Fill NaN values with 0
df = df.fillna("0")

#initialize our search client
client = SearchClient(endpoint=endpoint, index_name=index_name, credential=credential)

#upload our data to the index
data = []

for _, row in df.iterrows():
    data.append({
        "@search.action": "upload",
        "submissionID": str(row["submissionID"]),
        "submittedAt": str(row["submittedAt"]),
        "age": str(row["age"]),
        "zipCode": str(row["zipCode"]),
        "cupsPerDay": str(row["cupsPerDay"]),
        "whereDoYouDrinkCoffee": str(row["whereDoYouDrinkCoffee"]),
        "howDOYouBrewYourCoffee": str(row["howDOYouBrewYourCoffee"])
    })
result = client.upload_documents(data)
print(result)
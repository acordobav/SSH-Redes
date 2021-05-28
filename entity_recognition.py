import sys
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

key = "cadb9f0784e1410ca2eb58015096f78c"
endpoint = "https://soa-nlp-api.cognitiveservices.azure.com/"

def authenticate_client():
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint, 
            credential=ta_credential)
    return text_analytics_client

def entity_recognition(client, documents):

    result = client.recognize_entities(documents = documents)[0]
    f = open("resultado.txt", "w")
    for entity in result.entities:
        if entity.category == "Person":
            f.write(entity.text + "\n")
    f.close()
    print("Success: File analyzed")

def analyze_file(filepath):

    client = authenticate_client()

    with open(filepath) as f:
        content = f.read()
        documents = []
        documents.append(content)
        entity_recognition(client, documents)
    
def main():
    args = sys.argv[1:]
    if len(args) > 0:
        try:
            open(args[0])
            analyze_file(args[0])
        except IOError:
            print("Error: File not accesible")
    else:
        print("Error: Arguments not accesible")

main()

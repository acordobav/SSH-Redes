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
    print ("Named Entities:")
    for entity in result.entities:
        if entity.category == "Person":
            print(entity.text + "\n")

def analyze_file(filepath):

    client = authenticate_client()

    with open(filepath) as f:
        content = f.read()
        documents = []
        documents.append(content)
        entity_recognition(client, documents)

analyze_file("prueba.txt")


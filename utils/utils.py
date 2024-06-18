import random
from faker import Faker
import json
import uuid
from google.cloud import storage, language_v1, bigquery
from datetime import datetime
import time

def today_str():
    return datetime.utcnow().strftime('%Y%m%d')

def gen_uuid():
    return str(uuid.uuid4().hex)[:4]

def extract_reviews():
    num_reviews = random.randint(1,10)
    fake = Faker()
    reviews = []
    for _ in range(num_reviews):
        review = {
            "username": fake.user_name(),
            "comment": fake.sentence(nb_words=random.randint(5, 25)),
            "rating": random.randint(1, 5),
            "datetime": fake.date_time_between(start_date='-1h').strftime('%Y-%m-%d %H:%M:%S') 
        }
        reviews.append(review)
    return json.dumps(reviews, indent=2)

def upload_file_to_gcs(bucket_name, destination_blob_name, content):
    """Sube un archivo a Google Cloud Storage."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(content)
    print(f"Reviews loaded to {destination_blob_name} bucket {bucket_name}.")


def download_file_from_gcs(bucket_name, source_blob_name):
    """Descarga un archivo desde Google Cloud Storage y devuelve su contenido."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    content = blob.download_as_string().decode("utf-8")
    print(f"Archivo {source_blob_name} descargado desde el bucket {bucket_name}.")
    return content

def analyze_sentiment(text):
    """Analiza el sentimiento de un texto utilizando la API de Google Cloud Natural Language."""
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(document=document)
    sentiment = response.document_sentiment
    print(f"Sentimiento: {sentiment.score}, Magnitud: {sentiment.magnitude}")
    return sentiment.score, sentiment.magnitude

def parse_json(text):
    return json.loads(text)

def format_reviews(reviews):
    rows_to_insert = []
    for review in reviews:
        print(review["comment"])
        sentiment_score, sentiment_magnitude = analyze_sentiment(review["comment"])
        row = {
            "username": review["username"],
            "comment": review["comment"],
            "rating": review["rating"],
            "sentiment_score": sentiment_score,
            "sentiment_magnitude": sentiment_magnitude,
            "review_datetime": review["datetime"],
            "process_datetime": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        rows_to_insert.append(row)
        time.sleep(2)

    return rows_to_insert

def upload_results_to_bigquery(dataset_id, table_id, rows_to_insert):
    """Sube los resultados del análisis de sentimiento a BigQuery."""
    client = bigquery.Client()
    table_ref = client.dataset(dataset_id).table(table_id)
    table = client.get_table(table_ref)

    errors = client.insert_rows_json(table, rows_to_insert)
    if errors == []:
        print("Datos insertados exitosamente en BigQuery.")
    else:
        print(f"Errores al insertar los datos: {errors}")
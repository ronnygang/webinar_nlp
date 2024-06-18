import utils.utils as fx
from utils import config

def analyze():
    PROCESS_DATE = fx.today_str()
    SOURCE_BLOB_NAME = f'{config.__RAW_FOLDER__}/{PROCESS_DATE}/reviews.json'
    BUCKET_NAME = config.__BUCKET_NAME__
    dataset_id = config.__DATASET_ID__
    table_id = config.__TABLE_ID__
    downloaded_reviews  = fx.download_file_from_gcs(BUCKET_NAME, SOURCE_BLOB_NAME)
    reviews = fx.parse_json(downloaded_reviews)
    reviews_analyzed = fx.format_reviews(reviews)
    fx.upload_results_to_bigquery(dataset_id, table_id, reviews_analyzed)
    return f'Analyzed succesfully PROCESS_DATE: {PROCESS_DATE}'

def main():
    return analyze()

"""
if __name__ == '__main__':
    response = main()
    print(response)
"""    
import utils.utils as fx
from utils import config

def extract():
    PROCESS_DATE = fx.today_str()
    DESTINATION_BLOB_NAME = f'{config.__RAW_FOLDER__}/{PROCESS_DATE}/reviews.json' 
    BUCKET_NAME = config.__BUCKET_NAME__
    reviews = fx.extract_reviews()
    fx.upload_file_to_gcs(BUCKET_NAME, DESTINATION_BLOB_NAME, reviews)
    return f'Extract succesfully PROCESS_DATE: {PROCESS_DATE}'

def main():
    return extract()

"""
if __name__ == '__main__':
    response = main()
    print(response)
"""    
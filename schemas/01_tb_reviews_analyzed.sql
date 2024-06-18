CREATE TABLE `raw_layer.tb_reviews_analyzed` (
    username STRING,
    comment STRING,
    rating INT64,
    sentiment_score FLOAT64,
    sentiment_magnitude FLOAT64,
    review_datetime STRING,
    process_datetime STRING
);

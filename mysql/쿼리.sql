USE testdb;

CREATE TABLE product_quality(
product_id INT PRIMARY KEY,
temperature FLOAT NOT NULL,
pressure FLOAT NOT NULL,
humidity FLOAT NOT NULL,
process_time FLOAT NOT NULL,
defect_rate FLOAT NOT NULL,
quality_grade TINYINT NOT NULL
);

DESC product_quality;


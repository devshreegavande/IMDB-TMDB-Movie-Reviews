import os
import csv


reviews_list_files = "2_reviews_per_movie_raw"
count = 0
review_count_empty = 0
for file_name in os.listdir(reviews_list_files):
    file_path = reviews_list_files+"/"+file_name
    with open(file_path, 'r', newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            count += 1
            if len(row['title']) == 0:
                review_count_empty += 1

print(f"reviews count: {count}")
print(f"reviews count empty: {review_count_empty}")
import os
import requests
import json


def write_to_file_with(filename, content):
    with open(filename, 'w') as file:
        file.write(content)


search_imdb_id_string = "title/tt"
movies_list_files = "dataset/1_movies_per_genre"
imdb_id_list = []
for file_name in os.listdir(movies_list_files):
    file_path = movies_list_files+"/"+file_name
    with open(file_path, 'r') as file:
        for line in file:
            if search_imdb_id_string in line:
                index = line.find(search_imdb_id_string)
                imdb_id_index = index+len(search_imdb_id_string) - 2
                imdb_id_end_index = line.find("/", imdb_id_index)
                imdb_id = line[imdb_id_index:imdb_id_end_index]
                if imdb_id not in imdb_id_list:
                    imdb_id_list.append(imdb_id)
print(f"imdb ids count: {len(imdb_id_list)}")


def tmdb_api_call(url:str):
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3NTc2NmM1Y2U3MDFjZjM0Mzc0NmYyZTVhZWMzZTZiYiIsIm5iZiI6MTcyNzM5MjUxNi44NDg3NTIsInN1YiI6IjY2ZDViNWIyMjM0MTMzOTE5NzE4MjVmNSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.BjN9MP_Md4XG2cm9eiCu56VRZ61pIr_U77GDiO41ywo"
    }    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        if len(response.json()) == 0: # if no data
            return None
        # Convert the response to JSON
        json_data = response.json()
        return json_data
    else:
        print(f"Request failed with status code: {response.status_code} for url {url}")


tmdb_url_part1 = "https://api.themoviedb.org/3/find/"
tmdb_url_part2 = "?external_source=imdb_id"
language_part = "language=en-US"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3NTc2NmM1Y2U3MDFjZjM0Mzc0NmYyZTVhZWMzZTZiYiIsIm5iZiI6MTcyNzM5MjUxNi44NDg3NTIsInN1YiI6IjY2ZDViNWIyMjM0MTMzOTE5NzE4MjVmNSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.BjN9MP_Md4XG2cm9eiCu56VRZ61pIr_U77GDiO41ywo"
}

tmdb_movie_details_list = []
cnt = 1
for id in imdb_id_list:
    tmdb_url = tmdb_url_part1+id+tmdb_url_part2+"&"+language_part
    json_data = tmdb_api_call(tmdb_url)
    if json_data is not None or len(json_data['movie_results']) != 0:
        movie_id = json_data['movie_results'][0]['id']
        tmdb_movie_details_url = f"https://api.themoviedb.org/3/movie/{movie_id}?"+language_part
        details_json = tmdb_api_call(tmdb_movie_details_url)
        print(f"adding data for movie: {movie_id}...{cnt}")
        tmdb_movie_details_list.append(details_json)
        cnt += 1        
    

write_to_file_with("dataset/tmdb_movie_details.json", json.dumps(tmdb_movie_details_list))



#  ------------------------------
# reviews_per_movie_path = "dataset/2_reviews_per_movie_raw"

# movie_names_year = []

# for f in os.listdir(reviews_per_movie_path):
#     filename_no_extension = f[:-4]
#     movie_dict = {}
#     movie_dict["movie_name"] = f[:-9]
#     movie_dict["year"] = f[-8:-4]
#     movie_names_year.append(movie_dict)

#print(f"list: {movie_names_year}")
# movie_name = "Black%20Hawk%20Down"
# year = "2001"
# tmdb_url = f"https://api.themoviedb.org/3/search/movie?query={movie_name}&include_adult=false&language=en-US&page=1&year={year}"

# headers = {
#     "accept": "application/json",
#     "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3NTc2NmM1Y2U3MDFjZjM0Mzc0NmYyZTVhZWMzZTZiYiIsIm5iZiI6MTcyNzM5MjUxNi44NDg3NTIsInN1YiI6IjY2ZDViNWIyMjM0MTMzOTE5NzE4MjVmNSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.BjN9MP_Md4XG2cm9eiCu56VRZ61pIr_U77GDiO41ywo"
# }

# response = requests.get(tmdb_url, headers=headers)
# if response.status_code == 200:
#     if len(response.json()) == 0: # if no data
#         print("No Data")
#     # Convert the response to JSON
#     json_data = response.json()
#     print(json_data)
#     print(f"original_title: {json_data['results'][0]['original_title']}")
#     print(f"original_title: {json_data['results'][0]['original_title']}")
# else:
#     print(f"Request failed with status code: {response.status_code} for url {tmdb_url}")

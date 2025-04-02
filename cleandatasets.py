import pandas as pd
import numpy as np
import gpxpy
import os
from tqdm import tqdm

# gpx files user : cMartin 18 avril 2022
GPX_FILES_PATH = "datasets/gpx/"
CSV_FILES_PATH = "datasets/csv/"

def clean_csv(files):
    df = pd.DataFrame(columns=['trajet_id','latitude','longitude'])
    for file in tqdm(files, desc="Processing .csv files", unit="file"):
        data = pd.read_csv(file)

        filtered_data = data[['vehicle_id', 'latitude', 'longitude']]
        filtered_data.rename(columns={"vehicle_id": "trajet_id"}, inplace=True)

        df = pd.concat([df, filtered_data], ignore_index=True)

    df.to_csv('datasets/outputs/cleaned_csv.csv', index=False)


def clean_gpx(files):
    data = []
    for file in tqdm(files, desc="Processing .gpx files", unit="file"):
        with open(file) as f:
            gpx = gpxpy.parse(f)

        trajet_id = file.removeprefix(GPX_FILES_PATH).removesuffix(".gpx")

        for segment in gpx.tracks[0].segments:
            for point in segment.points:
                data.append([trajet_id, point.latitude, point.longitude])

    df = pd.DataFrame(data, columns=['trajet_id','latitude', 'longitude'])
    df.to_csv('datasets/outputs/cleaned_gpx.csv', index=False)


gpx_files = [GPX_FILES_PATH+entry.name for entry in os.scandir(GPX_FILES_PATH) if entry.is_file()]
csv_files = [CSV_FILES_PATH+entry.name for entry in os.scandir(CSV_FILES_PATH) if entry.is_file()]

def csv_chosen(selected_files):
    clean_csv(selected_files)
    
def gpx_chosen(selected_files):
    clean_gpx(selected_files)

#clean_gpx(["datasets/test/"+entry.name for entry in os.scandir("datasets/test/") if entry.is_file()])
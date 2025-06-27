
import os
import csv
import uuid
import supabase
from supabase import create_client, Client

# Replace with your Supabase keys
SUPABASE_URL = "https://zlkefvmjdlqewcreqhko.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inpsa2Vmdm1qZGxxZXdjcmVxaGtvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDk5MTI2ODcsImV4cCI6MjA2NTQ4ODY4N30.MJe_4Gvtpj2x1J5TcLorVXzyNFrMxjLvh0mBLXdhNT8"
BUCKET_NAME = "species-images"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

SEED_DATA_PATH = "../metadata/seed_data.csv"
DATASET_ROOT = "../dataset"

def upload_image(file_path, storage_path):
    with open(file_path, 'rb') as f:
        response = supabase.storage().from_(BUCKET_NAME).upload(storage_path, f, {"content-type": "image/jpeg"})
        return response

def main():
    with open(SEED_DATA_PATH, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            species = row['species']
            strain = row['strain']
            grade = row['grade_label']
            filename = row['image_filename']
            source = row.get('source', 'unknown')
            license_type = row.get('license', 'unknown')
            contributor = row.get('contributor', 'unknown')

            local_image_path = os.path.join(DATASET_ROOT, species, strain, grade, filename)
            storage_path = f"{species}/{strain}/{grade}/{filename}"

            print(f"Uploading {local_image_path} to {storage_path}...")
            upload_image(local_image_path, storage_path)

            image_url = f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET_NAME}/{storage_path}"

            supabase.table("images").insert({
                "image_url": image_url,
                "source": source,
                "license": license_type,
                "contributor": contributor
            }).execute()

if __name__ == "__main__":
    print("Script started...")
    main()
    print("Script finished.")

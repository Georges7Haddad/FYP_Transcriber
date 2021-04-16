FROM python:3.7.3-slim

WORKDIR /app
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y wget unzip build-essential ffmpeg sox libsndfile1 libasound2-dev libjack-dev portaudio19-dev

# Download trained piano model
RUN wget https://storage.googleapis.com/magentadata/models/onsets_frames_transcription/maestro_checkpoint.zip
RUN unzip maestro_checkpoint.zip
RUN rm maestro_checkpoint.zip
# Download trained drums model
RUN wget https://storage.googleapis.com/magentadata/models/onsets_frames_transcription/e-gmd_checkpoint.zip
RUN unzip -d ./e-gmd_checkpoint e-gmd_checkpoint.zip
RUN rm e-gmd_checkpoint.zip

# Upgrade pip
RUN pip install --upgrade pip

# Install requirements
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

RUN rm -rf /var/lib/apt/lists/*

COPY . /app/

EXPOSE 8000

ENTRYPOINT python3 manage.py runserver 0.0.0.0:8000
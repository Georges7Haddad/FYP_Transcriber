import subprocess
import os
from random import randrange
from threading import Timer

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from wsgiref.util import FileWrapper


def delete_files(rand, type):
    os.remove(f"Transcriber/{type}_track{rand}.wav")
    os.remove(f"Transcriber/{type}_track{rand}.wav.midi")


class PianoMidi(APIView):
    parser_classes = (MultiPartParser,)

    @csrf_exempt
    def post(self, request):
        rand = randrange(1000)
        with open(f"Transcriber/piano_track{rand}.wav", "wb") as new_file:
            new_file.write(request.FILES['file'].read())
        subprocess.run(["onsets_frames_transcription_transcribe", "--model_dir=./train",
                        f"Transcriber/piano_track{rand}.wav"])
        t = Timer(20.0, delete_files, args=[rand, "piano"])
        t.start()
        midi = open(f"Transcriber/piano_track{rand}.wav.midi", "rb")
        midi_response = HttpResponse(FileWrapper(midi), content_type="audio/midi", status=status.HTTP_200_OK)
        midi_response['Content-Disposition'] = 'attachment; filename="piano.midi"'
        return midi_response


class DrumsMidi(APIView):
    parser_classes = (MultiPartParser,)

    @csrf_exempt
    def post(self, request):
        rand = randrange(1000)
        with open(f"Transcriber/drums_track{rand}.wav", "wb") as new_file:
            new_file.write(request.FILES['file'].read())
        subprocess.run(["onsets_frames_transcription_transcribe", "--model_dir=./e-gmd_checkpoint",
                        "--config=drums", f"Transcriber/drums_track{rand}.wav"])
        t = Timer(20.0, delete_files, args=[rand, "drums"])
        t.start()
        midi = open(f"Transcriber/drums_track{rand}.wav.midi", "rb")
        midi_response = HttpResponse(FileWrapper(midi), content_type="audio/midi", status=status.HTTP_200_OK)
        midi_response['Content-Disposition'] = 'attachment; filename="drums.midi"'
        return midi_response


class BassMidi(APIView):
    parser_classes = (MultiPartParser,)

    @csrf_exempt
    def post(self, request):
        rand = randrange(1000)
        with open(f"Transcriber/bass_track{rand}.wav", "wb") as new_file:
            new_file.write(request.FILES['file'].read())
        subprocess.run(["onsets_frames_transcription_transcribe", "--model_dir=./train",
                        f"Transcriber/bass_track{rand}.wav"])
        t = Timer(20.0, delete_files, args=[rand, "bass"])
        t.start()
        midi = open(f"Transcriber/bass_track{rand}.wav.midi", "rb")
        midi_response = HttpResponse(FileWrapper(midi), content_type="audio/midi", status=status.HTTP_200_OK)
        midi_response['Content-Disposition'] = 'attachment; filename="bass.midi"'
        return midi_response

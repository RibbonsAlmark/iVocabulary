import os
import time
from pydub import AudioSegment
import simpleaudio as sa


def trans_mp3_to_wav(mp3_fp, wav_fp):
    if not os.path.exists(mp3_fp):raise Exception('mp3 not found')

    sound = AudioSegment.from_mp3(mp3_fp)
    sound.export(wav_fp, format="wav")

    return


def play_wav_audio(wav_fp, repeat_times = 1, repeat_interval = 1):
    if not os.path.exists(wav_fp):raise Exception('wav not found')

    wave_obj = sa.WaveObject.from_wave_file(wav_fp)

    for i in range(repeat_times):
        play_obj = wave_obj.play()
        play_obj.wait_done()
        if repeat_times > 1:time.sleep(repeat_interval)

    return
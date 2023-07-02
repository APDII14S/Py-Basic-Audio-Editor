from pydub import AudioSegment
import simpleaudio as sa    # importing the simpleaudio module(s)
import os
from pathlib import Path

while_loop_check = True

def intro1():
    global mp3_to_input
    global mp3_to_edit
    global preview_prompt

    mp3_to_input = input("Where is your MP3 destination?: ")


    while os.path.exists(mp3_to_input) == False and Path(mp3_to_input).suffix != ".mp3":
        print("File doesn't exist, or isn't an MP3")
        print("Try specifying the full file path")
        print("Remember to specify the '.mp3' file extension suffix")
        mp3_to_input = input('Where is your MP3 destination?: ')

    mp3_to_edit = AudioSegment.from_mp3(mp3_to_input)
    intro2(mp3_to_edit)

def intro2(mp3_to_edit):
    global preview_prompt
    global while_loop_check
    global audio_crop_time



    audio_preview = input(
        "Your MP3 is ready to be modified. What edit do you wish to make?\n"
        "Options: Reverse (r), Crop (c), Volume Adjust (a)\n")
    if audio_preview.lower() == 'r':
        preview_prompt = input('Before editing your mp3, would you like to hear a 10s preview?\nY | N\n')
        if preview_prompt.lower() == 'y':
            preview(audio_preview, mp3_to_edit)
            edit_or_nah(audio_preview, mp3_to_edit)

        elif preview_prompt.lower() == 'n':
            edit_or_nah(audio_preview, mp3_to_edit)

    elif audio_preview.lower() == 'c':
        edit_or_nah(audio_preview, mp3_to_edit)



    elif audio_preview.lower() == 'a':
        preview_prompt = input('Before editing your mp3, would you like to hear a 10s preview?\nY | N')

def edit_or_nah(audio_preview, mp3_to_edit):
    global while_loop_check
    global audio_crop_time
    global audio_time
    global mp3_duration

    mp3_duration = mp3_to_edit.duration_seconds

    while while_loop_check:
        if audio_preview.lower() == 'r':
            audio_crop_time = input('Wanna reverse your mp3, or leave it?\nR | L\n')
            if audio_crop_time.lower() == 'r':
                mp3_to_edit = mp3_to_edit.reverse()
                mp3_to_edit.export(mp3_to_input, format='mp3')
                print('Reversed ' + mp3_to_input + ' successfully')
                break
            elif audio_crop_time.lower() == 'l':
                refresh_variables()
                intro1()
                break
            else:
                print('Pick a valid option')
                continue
        elif audio_preview.lower() == 'c':
            while while_loop_check:
                audio_crop_time = int(input('What timeframe will the crop be?\n'
                                      "Enter a natural #: \n"))


                if audio_crop_time > mp3_duration:
                    print("End/start times can't exceed the actual end time of your mp3 file")
                elif audio_crop_time == 0:
                    print('Why not just delete your mp3?')
                elif type(audio_crop_time) is int:
                    print('Test passed')
                    while_loop_check = False
                    crop_audio(mp3_to_edit, audio_crop_time, audio_preview)
                    break
                else:
                    print('Input valid data types')

def preview(audio_preview, mp3_to_edit):
    global limited_preview

    if audio_preview.lower() == 'r':
        preview = mp3_to_edit.reverse()
    else:
        preview = mp3_to_edit

    if len(preview) <= 10000: # len(preview) refers to the duration of the preview variable, which would
                              # equal mp3_to_edit, which would equal the mp3 file one wishes to edit

        preview.export('C:\\Users\\client\\PycharmProjects\\basic_MP3_Editor\\mp3_to_edit_preview.wav', format='wav')
        preview_instance = sa.WaveObject.from_wave_file('mp3_to_edit_preview.wav')
        play_instance = preview_instance.play()
        play_instance.wait_done()
        os.remove('mp3_to_edit_preview.wav')
    elif len(preview) > 10000:
        limited_preview = preview[:10000]
        limited_preview.export('C:\\Users\\client\\PycharmProjects\\basic_MP3_Editor\\limited_preview.wav',
                               format='wav')
        preview_instance = sa.WaveObject.from_wave_file('limited_preview.wav')
        play_instance = preview_instance.play()
        play_instance.wait_done()
        os.remove('limited_preview.wav')

def crop_audio(mp3_to_edit, audio_crop_time, audio_preview):

    print('test passed again')
    mp3_to_edit = mp3_to_edit[:audio_crop_time]
    preview_prompt = input('Before editing your mp3, would you like to hear a 10s preview?\nY | N\n')
    if preview_prompt.lower() == 'y':
        print('test passed for preview_prompt equals yes')
        preview(audio_preview, mp3_to_edit)
        edit_or_nah(audio_preview, mp3_to_edit)

    elif preview_prompt.lower() == 'n':
        print('test passed for preview_prompt equals no')
        edit_or_nah(audio_preview, mp3_to_edit)



#   meant to reset every variable, to being a blank slate
def refresh_variables():
    global mp3_to_input
    global mp3_to_edit
    global audio_preview
    global preview_prompt
    global limited_preview
    global output_filename

    mp3_to_input = None
    mp3_to_edit = None
    audio_preview = None
    preview_prompt = None
    limited_preview = None
    output_filename = None



intro1()




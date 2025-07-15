from utils.file_utils import get_all_files_in_directory, delete_file
from utils.audio_utils import get_noise_snippet, get_audio_wav_and_sample_rate, get_duration, export_audio
from utils.rttm_utils import concat_rttm_entries_if_small_gap, export_rttm_file
import numpy as np
import random
import yaml
import os

with open("config.yml", encoding="utf-8") as f:
    config = yaml.safe_load(f)

############################################################
PATH_TO_SPEAKERS_FOLDER = config["paths"]["path_to_speakers_folder"]
PATH_TO_NOISE_FILE = config["paths"]["path_to_noise_file"]
PATH_TO_OUTPUT_FOLDER = config["paths"]["path_to_output_folder"]

random.seed(config["params"]["random_seed"])
CHOSEN_SPEAKERS = config["params"]["chosen_speakers"]
NAME_OF_OUTPUT_FILE= f"{len(CHOSEN_SPEAKERS)}_speakers_001"

SAMPLE_RATE = int(config["params"]["sample_rate"])

DESIRED_DURATION_SEC = int(config["params"]["desired_duration_sec"])
MIN_DURATION_TO_CONSIDER_AUDIO_SEC = int(config["params"]["min_duration_to_consider_audio_sec"])

SPEAKER_MAX_REPEAT = int(config["params"]["speaker_max_repeat"])
SPEAKER_MIN_REPEAT = int(config["params"]["speaker_min_repeat"])

MIN_SILENCE_DURATION_DIFF_SPEAKERS_SEC = float(config["params"]["min_silence_duration_diff_speakers_sec"])
MAX_SILENCE_DURATION_DIFF_SPEAKERS_SEC = float(config["params"]["max_silence_duration_diff_speakers_sec"])

MIN_SILENCE_DURATION_SAME_SPEAKERS_SEC = float(config["params"]["min_silence_duration_same_speakers_sec"])
MAX_SILENCE_DURATION_SAME_SPEAKERS_SEC = float(config["params"]["max_silence_duration_same_speakers_sec"])

MAX_GAP_TO_MERGE_SAME_SPEAKER_SEC = float(config["params"]["max_gap_to_merge_same_speaker_sec"])
################################################################
def get_filenames_for_speakers(
    chosen_speakers:list,
    path_to_speakers_folder:str
    )->dict:
    '''
    Get a dict with names of speakers as keys and their filenames of each audio as a list as the values
    '''
    audio_filepath_dict = {}
    for speaker in chosen_speakers:
        
        path_to_audio = os.path.join(path_to_speakers_folder, speaker)
        audio_filepath_dict[speaker] = []
        
        audio_filenames = get_all_files_in_directory(path_to_audio)
        
        for audio_filename in audio_filenames:
            
            audio_filepath = os.path.join(path_to_audio, audio_filename)
            audio_filepath_dict[speaker].append(audio_filepath)
            
    return audio_filepath_dict

def generate_diar_dataset(
    audio_filepath_dict:dict
    )->tuple[np.ndarray, list]:
    '''
    Logic to generate the diar dataset
    
    steps:
    
    1. Checks if desired duration has been reached
    2. Determine which speaker to grab audio from first and how many times to repeat for this speaker
    3. Check if audio chosen is within min duration specified, if not pick another and try again
    4. Add to the rttm values
    5. Determine how long of silence should be used and put that duration into get_noise_snippet function
    6. Concat the silence to the wav and repeat
    '''
    final_wav = np.ndarray([0])
    past_speaker = ''
    speaker = ''
    current_audio_start_time = 0
    current_audio_length = 0
    number_to_run = 0
    rttm_values = []
    noise_wav, sr = get_audio_wav_and_sample_rate(PATH_TO_NOISE_FILE, SAMPLE_RATE)
        
    while current_audio_length<DESIRED_DURATION_SEC:
        
        if number_to_run == 0:
            # Make sure the previous speaker not same as current speaker
            while speaker == past_speaker:
                speaker = CHOSEN_SPEAKERS[random.randint(0, len(CHOSEN_SPEAKERS)-1)]
            number_to_run = random.randint(SPEAKER_MIN_REPEAT, SPEAKER_MAX_REPEAT-1)
            past_speaker = speaker
            
        else:
            number_to_run -= 1
        
        choose_random_audio = audio_filepath_dict[speaker][random.randint(0, len(audio_filepath_dict[speaker])-1)]
        
        if not get_duration(choose_random_audio) < MIN_DURATION_TO_CONSIDER_AUDIO_SEC:
            duration_of_audio = get_duration(choose_random_audio)
            
            # Dealing with adding the audio in         
            y, sr = get_audio_wav_and_sample_rate(choose_random_audio, SAMPLE_RATE)
            final_wav = np.concatenate((final_wav, y))
            rttm_value = [round(current_audio_start_time, 2), round(current_audio_start_time + duration_of_audio,2), speaker]
            
            rttm_values.append(rttm_value)
            
            # Adding in noise audio with preset time inbetween speakers
            # Inbetween same speakers
            if number_to_run != 0:
                duration_silence = random.randint((MIN_SILENCE_DURATION_SAME_SPEAKERS_SEC * 10), (MAX_SILENCE_DURATION_SAME_SPEAKERS_SEC * 10)-1 )/10
            # Inbetween diff speakers
            else:
                duration_silence = random.randint((MIN_SILENCE_DURATION_DIFF_SPEAKERS_SEC * 10), (MAX_SILENCE_DURATION_DIFF_SPEAKERS_SEC * 10)-1 )/10
            silence_array = get_noise_snippet(
                noise_wav=noise_wav,
                sample_rate=SAMPLE_RATE,
                desired_duration=duration_silence,
                chunk_duration=0.1
                )
            final_wav = np.concatenate((final_wav, silence_array))
            
            # Next audio start time
            current_audio_start_time+= (duration_of_audio+duration_silence)
            current_audio_length += (duration_of_audio+duration_silence)
        
        else: 
            number_to_run+=1
            print('we skippy')
    
    return final_wav, rttm_values
    

def main():
    
    audio_filepath_dict = get_filenames_for_speakers(
        chosen_speakers=CHOSEN_SPEAKERS,
        path_to_speakers_folder=PATH_TO_SPEAKERS_FOLDER
    )
    
    final_wav, rttm_values = generate_diar_dataset(
        audio_filepath_dict=audio_filepath_dict
    )
    
    new_rttm = concat_rttm_entries_if_small_gap(rttm_values, MAX_GAP_TO_MERGE_SAME_SPEAKER_SEC)
    
    # Export generated audio and rttm
    delete_file(os.path.join(PATH_TO_OUTPUT_FOLDER, NAME_OF_OUTPUT_FILE+'.rttm'))
    export_audio(final_wav, SAMPLE_RATE, os.path.join(PATH_TO_OUTPUT_FOLDER, NAME_OF_OUTPUT_FILE+'.wav'))
    export_rttm_file(new_rttm, 'NSC_DIAR_DH', os.path.join(PATH_TO_OUTPUT_FOLDER, NAME_OF_OUTPUT_FILE+'.rttm'))
        
if __name__ == "__main__":
    
    main()
import librosa
import soundfile as sf
import numpy as np
def get_duration(audio_filepath):
    ''' Get the duration of an audio file in seconds '''
    
    return librosa.get_duration(path=audio_filepath)

def get_segment_of_audio(audio_filepath, start_time, end_time, sr = 16000):
    ''' Get a segment of an audio file '''
    
    y, sr = librosa.load(audio_filepath, sr=sr, offset=start_time, duration=end_time - start_time)
    
    return y, sr

def get_audio_wav_and_sample_rate(audio_filepath, sr=16000):
    ''' Get the sample rate of an audio file '''
    
    y, sr = librosa.load(audio_filepath, sr=sr)
    
    return y, sr

def export_audio(y, sr, output_filepath):
    ''' Export audio to a file '''
    
    sf.write(output_filepath, y, sr)
    

def get_noise_snippet(noise_wav, 
                      sample_rate = 16000, 
                      desired_duration = 0.4,
                      chunk_duration = 0.1):
    '''
    Sample noise from wav and returns the specified duration of sitched together noise
    '''
    
    if not desired_duration == 0:
    
        chunk_size = int(chunk_duration * sample_rate)
        total_chunks = int(np.ceil(desired_duration / chunk_duration))

        max_start = len(noise_wav) - chunk_size
        if max_start <= 0:
            raise ValueError("Noise wav is too short to sample 0.1s chunks.")

        chunks = []
        for _ in range(total_chunks):
            start = np.random.randint(0, max_start)
            chunk = noise_wav[start:start + chunk_size]
            chunks.append(chunk)
            
        return np.concatenate(chunks)

    else:
        
        return np.zeros(1)
    
# Generating Audio Diarisation
This repo is for generating a custom diarisation audio and rttm file with utterances from different speakers

## Setup
### Virtual Environment

1. Set up a virtual Environment
```bash
python3 -m venv venv
```
2. Activate the virtual environment
```bash
source venv/bin/activate
```

3. Download the packages needed
```bash
pip install -r requirements.txt
```
Virtual Environment has been set up!

### Config file

The config file should look something like:

```yaml
paths:
  path_to_speakers_folder: "<Direct path to speakers dataset>"
  path_to_noise_file: "<Direct path to noise wav file>"
  path_to_output_folder: "<Direct path to output folder>"

params:
  random_seed: <integar seed value>
  chosen_speakers: <chosen speakers with respect to your speaker dataset folder> 
    e.g.
    [
      "SPEAKER0970",
      "SPEAKER1015",
    ] 
  sample_rate: 16000
  desired_duration_sec: 60 # Total duration of diarisation audio
  min_duration_to_consider_audio_sec: 3 # minimum duration of speaker utterance audio to combine
  speaker_max_repeat: 5 # Max number of repetitions of same speaker before swapping
  speaker_min_repeat: 2 # Min number of repetitions of same speaker before swapping
  min_silence_duration_diff_speakers_sec: 0 # Min seconds of silence between 2 different speakers
  max_silence_duration_diff_speakers_sec: 0.8 # Max seconds of silence between 2 different speakers
  min_silence_duration_same_speakers_sec: 0 # Min seconds of silence between 2 same speaker segments
  max_silence_duration_same_speakers_sec: 0.2 # Max seconds of silence between 2 same speaker segments
  max_gap_to_merge_same_speaker_sec: 0.5 # Anything less than this Max seconds of silence between 2 same speaker segment are combined in the .rttm file
```
A template is provided in config.yml

### Speaker dataset
Your speaker dataset should look something like this
```
.
└── speakers_folder/
    ├── SPEAKER001/
    │   ├── audio1.wav
    │   ├── audio2.wav
    │   └── ...
    ├── SPEAKER002/
    │   ├── audio1.wav
    │   ├── audio2.wav
    │   └── ...
    └── SPEAKER003/
        ├── audio1.wav
        ├── audio2.wav
        └── ...
```

### Noise

This can be any noise you want to add inbetween any 2 segments of speech


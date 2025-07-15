def concat_rttm_entries_if_small_gap(rttm_values, max_gap = 0.5):
    ''' 
    Combine rttm entries if the gap in between same speaker segments are less than max_gap
    '''
    
    last_end_time = 0
    last_start_time = 0
    last_speaker = ''
    new_rttm_values = []
    
    for rttm_value in rttm_values:
        
        start_time = rttm_value[0]
        end_time = rttm_value[1]
        speaker = rttm_value[2]
        
        # Starting
        if last_speaker == '':
            
            last_speaker = speaker
            last_end_time = end_time
            last_start_time = start_time
        
        # If previous speaker same as current
        elif last_speaker == speaker:
            
            if start_time - last_end_time <= max_gap:
                #MERGE
                last_end_time = end_time
            
            else:
                #NO MERGE
                entry = [last_start_time, last_end_time, last_speaker]
                new_rttm_values.append(entry)
                last_speaker = speaker
                last_end_time = end_time
                last_start_time = start_time
            
        # If speaker not the same    
        else:
            
            entry = [last_start_time, last_end_time, last_speaker]
            new_rttm_values.append(entry)
            last_speaker = speaker
            last_end_time = end_time
            last_start_time = start_time
            
    entry = [last_start_time, last_end_time, last_speaker]
    new_rttm_values.append(entry)
    return new_rttm_values

def export_rttm_file(list_rttm_entries, file_id, output_path = 'test.rttm'):
    ''' 
    Generate rttm file from list [[start, end, speaker]]
    '''
    for entry in list_rttm_entries:

        duration = entry[1] - entry[0]

        with open(output_path, 'a') as f:
            line = f"SPEAKER {file_id} 1 {entry[0]:.3f} {duration:.3f} <NA> <NA> {entry[2]} <NA>\n"
            f.write(line)
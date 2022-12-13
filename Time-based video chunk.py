total_frames = 6504
frequency_in_seconds = 10

start_frame = 0
for i in range(0, int(total_frames / 60), frequency_in_seconds):
    if not i + frequency_in_seconds >= int(total_frames / 60):
        end_frame = start_frame + (frequency_in_seconds * 60)
    else:
        end_frame = (total_frames - start_frame) + start_frame
    print(f'Cutting from stamp {start_frame / 60} to {end_frame / 60}')
    start_frame = end_frame + 1

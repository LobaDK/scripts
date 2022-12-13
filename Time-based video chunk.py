total_time = 108.400000
frequency = 4
last_total_time = round(total_time - int(total_time), 6)
total_time_without_last = int(total_time - last_total_time)

for i in range(0, int(total_time), frequency):
    if not i + frequency + last_total_time == total_time:
        print(f'Cutting from stamp {i} to {(((i + frequency) * 60) - 1) / 60}') # Calculate timestamp to frame, then subtract 1 frame count, and convert back to timestamp
    else:
        print(f'Cutting from stamp {total_time_without_last} to {total_time}')
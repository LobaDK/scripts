total_time = 108.400000
frequency = 4
last_total_time = round(total_time - int(total_time - frequency), 6)
total_time_without_last = int(total_time - last_total_time)

for i in range(0, total_time_without_last, frequency):
    print(f'Cutting from stamp {i} to {i + frequency}')
print(f'Cutting from stamp {total_time_without_last} to {total_time}')
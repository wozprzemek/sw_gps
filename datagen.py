import csv
import time

x_value = 0
total_1 = 1000
total_2 = 1000
longitude_data = [16.9638768, 16.96298, 16.96261, 16.96233, 16.9623278, 16.96233, 16.96232, 16.96231, 16.9623, 16.96225,
                  16.96224, 16.96221, 16.96219, 16.96219, 16.96219, 16.96221, 16.96222, 16.96222, 16.9623, 16.96243,
                  16.96247, 16.96248, 16.9625, 16.96253, 16.96255, 16.96263, 16.96263, 16.96296, 16.96326, 16.96346,
                  16.96362, 16.96378, 16.964, 16.96419, 16.9641902]
latitude_data = [52.3994823, 52.3993, 52.39922, 52.39918, 52.3991805, 52.39945, 52.39951, 52.39988, 52.39995, 52.40028,
                 52.4003, 52.40049, 52.40059, 52.40066, 52.40075, 52.40076, 52.40077, 52.40078, 52.40087, 52.40101,
                 52.40106,
                 52.40108, 52.40114, 52.40119, 52.40126, 52.40143, 52.401426, 52.40136, 52.40128, 52.4012, 52.40111,
                 52.40099, 52.4008, 52.40064, 52.4006378]

print(max(longitude_data), min(longitude_data), max(latitude_data), min(latitude_data))

fieldnames = ["longitude", "latitude"]

with open('data.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

i = 0

while i <= len(longitude_data):
    with open('data.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        info = {
            "longitude": longitude_data[i],
            "latitude": latitude_data[i]
        }

        csv_writer.writerow(info)
        print(longitude_data[i], latitude_data[i])

    i = i + 1
    time.sleep(1)

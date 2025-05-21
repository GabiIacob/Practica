import csv

with open("persoane.csv", "r") as file: 
    reader=csv.reader(file)
    for row in reader:
        print (row)

with open("persoane.csv","a", newline="") as file:
    writer=csv.writer(file)
    
    writer.writerow(["Gheorghe", "1989-12-25"])
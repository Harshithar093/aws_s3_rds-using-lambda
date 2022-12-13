import csv
outputlist=[]
with open('emp_dict.csv','r',newline='') as csvreader:
    reader=csv.DictReader(csvreader)
    for row in reader:
        print(row['empid'],row['empname'],row['empaddress'])
        outputlist.append(row.values())
        outputlist.append(row)


    print(outputlist)
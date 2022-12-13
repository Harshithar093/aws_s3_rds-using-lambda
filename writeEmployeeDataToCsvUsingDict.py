import csv

#field names of csv
fields=['empid','empname','empaddress']

#data for rows in csv
rows=[{
  "empid": "100",
  "empname": "vamsi",
  "empaddress": "ap"
},
    {
        "empid": "200",
        "empname": "harshita",
        "empaddress": "Banglre"
    }
]

with open('emp_dict.csv', 'w',newline='') as dictcsvfile:
    #creating a csv dict writer object
    writer=csv.DictWriter(dictcsvfile,fieldnames=fields)
    #writing headers (fieldnames)
    writer.writeheader()
    #writing data rows
    writer.writerows(rows)



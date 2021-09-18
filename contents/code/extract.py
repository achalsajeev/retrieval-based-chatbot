import csv
with open('BankFAQs.csv', encoding="utf8", errors='ignore') as file:
    reader = csv.reader(file)

    for row in reader:
        f = open("file.txt", "a")
        f.write("{ \n")
        f.write('    "message": "'+row[0]+'"\n')
        f.write('   ,"response":"'+row[1]+'"')
        f.write("\n}, \n")
        f.close()
       
    
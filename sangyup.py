f=open("2018.txt","r",encoding = 'utf-16' )

while True:
    line = f.readline()
    if line == '' :
        break
    print(line, end='')

f.close()
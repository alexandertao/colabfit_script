import sys
def reformat(file_name):
    do=True
    a = file_address.split('.')
    #print(a)
    b = a[0] + '.' + a[1] + '_reformat.' + a[2]
    nf=open(b,'w')
    #nf=open(str(file_address+'_reformat'),'w')
    with open(file_address,'r') as f:
        while do:
                try:
                    n=int(f.readline())
                    #print(n)
                    data=f.readline().split(' ')
                    print(data)
                    atoms=""
                    for i in range(n):
                        atoms+=f.readline()

                    #cell=[]
                    #for j in range (3):
                    #    cell.append(f.readline().replace('\n','')[0:]) #changed
                    #print(cell)
                    #f.readline()
                    nf.write('%s\n' %n)
                    nf.write('CCSD(T)/CBS=%s CCSD(T)/haTZ=%s Properties=species:S:1:pos:R:3\n' %(data[16],data[18]))
                    nf.write(atoms)
                    #nf.write('\n')
                    #print (n)
                    #print(data)
                    #print (cell)
                except:
                    do=False

import os
current_address = os.path.dirname(os.path.abspath(__file__))
file_list = os.listdir(current_address)
for file_address in file_list:
    #a = file_address.split['.']
    #print (a)
import sys
def reformat(file_name):
    do=True
    nf=open('141_Cl-pyridine_A_z_-30_1.10_reformat.xyz','w')
    with open('141_Cl-pyridine_A_z_-30_1.10.xyz','r') as f:
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
    reformat(file_list)



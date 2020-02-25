import os
import sys
import pickle

version='11.4.5.14.893'
usage='''tel written by QwQ\n
Version {}\n
Usage:\n
-l Print your telephone book.\n
-a [name] [tel] Add a new record.Also edit existed records.\n
-rn [name] -rt [tel] Remove a record.\n
-sn [name] -st [tel] Search corresponding name or telephone number.\n
'''.format(version)
i=1
cnta=0
cntc=0
cntr=0

def getArg():
    global i
    i+=1
    return sys.argv[i-1]

def validArg(arg):
    l=set(['-a','-l','-rn','-rt','-sn','-st'])
    return arg in l

def load():
    f=open('tel.dat','rb')
    dir1=pickle.load(f)
    dir2=pickle.load(f)
    f.close()
    return (dir1,dir2)

def write(t):
    f=open('tel.dat','wb')
    pickle.dump(t[0],f)
    pickle.dump(t[1],f)
    f.close()

if len(sys.argv)==1:
    exit(usage)
else:
    if not os.path.exists('tel.dat'):
        f=open('tel.dat','wb')
        pickle.dump({},f)
        pickle.dump({},f)
        f.close()
    while i<len(sys.argv):
        arg=getArg()
        if not validArg(arg):
            exit('Error:Invalid argument.Run this program without arguments to see the usage.\n')
        if arg=='-l':
            f=open('tel.dat','rb')
            dir1=pickle.load(f)
            f.close()
            for name,tel in dir1.items():
                print('{}\t\t{}\n'.format(name,tel))
        elif arg=='-a':
            if not i+1<=len(sys.argv):
                exit('Error:Too few arguments.Run this program without arguments to see the usage.\n')
            name=getArg()
            tel=getArg()
            if not tel.isdigit():
                exit('Error:Invalid telephone number.\n')
            t=load()
            if not name in t[0].keys() and not tel in t[1].keys():
                cnta+=1
                t[0][name]=tel
                t[1][tel]=name
                write(t)
            elif name in t[0].keys() and not tel in t[1].keys():
                cntc+=1
                tel2=t[0][name]
                del t[1][tel2]
                t[0][name]=tel
                t[1][tel]=name
                write(t)
            elif not name in t[0].keys() and tel in t[1].keys():
                cntc+=1
                name2=t[1][tel]
                del t[0][name2]
                t[1][tel]=name
                t[0][name]=tel
                write(t)
            else:
                print('Warning:Invalid edit.\n')

        elif arg=='-rn':
            if not i<=len(sys.argv):
                exit('Error:Too few arguments.Run this program without arguments to see the usage.\n')
            name=getArg()
            t=load()
            if not name in t[0].keys():
                print('Warning:Name {} is not in the telephone book.No record removed.\n'.format(arg))
            else:
                tel=t[0][name]
                del t[0][name]
                del t[1][tel]
                write(t)
                cntr+=1
        elif arg=='-rt':
            if not i<=len(sys.argv):
                exit('Error:Too few arguments.Run this program without arguments to see the usage.\n')
            tel=getArg()
            t=load()
            if not tel in t[1].keys():
                print('Warning:Name {} is not in the telephone book.No record removed.\n'.format(arg))
            else:
                name=t[1][tel]
                del t[0][name]
                del t[1][tel]
                write(t)
                cntr+=1
        elif arg=='-sn':
            if not i<=len(sys.argv):
                exit('Error:Too few arguments.Run this program without arguments to see the usage.\n')
            name=getArg()
            t=load()
            if not name in t[0].keys():
                print('Name {} is not in the telephone book\n'.format(name))
            else:
                print('{}\t\t{}\n'.format(name,t[0][name]))
        elif arg=='-st':
            if not i<=len(sys.argv):
                exit('Error:Too few arguments.Run this program without arguments to see the usage.\n')
            tel=getArg()
            t=load()
            if not tel in t[1].keys():
                print('Telephone {} is not in the telephone book\n'.format(tel))
            else:
                print('{}\t\t{}\n'.format(t[1][tel],tel))

print('Work Complete.{} records added.{} records changed.{} records removed.\n'.format(cnta,cntc,cntr))
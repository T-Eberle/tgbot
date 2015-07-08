from multiprocessing import Process
import os

def f(name):
    info('function f')
    print ('hello'+ name)

def info(title):
    print (title)
    print ('module name:'+ __name__)
    if hasattr(os, 'getppid'):  # only available on Unix
        print ('parent process:'+ os.getppid().__str__())
    print ('process id:'+ os.getpid().__str__())



if __name__ == '__main__':
    p = Process(target=f, args=('bob',))
    p.start()
    p.join()
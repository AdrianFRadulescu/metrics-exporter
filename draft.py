import subprocess
import time
import sys

if __name__ == "__main__":

    proc = subprocess.Popen(['netstat', '-w 5'], stdout=subprocess.PIPE)

    line = 'input'
    while 'input' in line or 'bytes' in line:
        line = proc.stdout.readline()
        print line
        time.sleep(5)

    print line

    proc.terminate()
    del proc


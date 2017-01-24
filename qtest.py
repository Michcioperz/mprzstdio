#!/usr/bin/env python3
import subprocess, os, argparse, re, shutil

parser = argparse.ArgumentParser()
parser.add_argument("directory", type=str, choices=[d for d in os.listdir('.') if os.path.isdir(d)])
parser.add_argument("-s", "--special", type=str, action='append')
parser.add_argument("-v", "--verbose", action="store_true")
parser.add_argument('-p', '--profiling', action="store_true")
parser.add_argument('--pin', choices=['on', 'if_found', 'off'], default='off')
args = parser.parse_args()

if args.pin == "if_found":
    args.pin = "on" if shutil.which('pin') is not None else "off"

args.pin = True if args.pin == "on" else False

if args.pin:
    pin_root = os.path.dirname(shutil.which('pin'))
    subprocess.check_call(['make', '-f', 'makefile.pintool', 'pin-inscount.so', 'PIN_ROOT={}'.format(pin_root)])

cxx_args = ["g++",'-W','-Wall','-Wshadow','-g','-std=c++11','-o','./.qtest.out',os.path.join(args.directory,args.directory+".cpp")]
if args.profiling:
    cxx_args.append('-pg')
subprocess.check_call(cxx_args)

results = {}
def count(x):
    results[x] = results.get(x, 0) + 1
    return x

for i in sorted([x for x in os.listdir(args.directory) if x.endswith(".in")], key=lambda x: ("ocen" not in x, int(re.findall(r"\d+",x)[0]))):
    with open(os.path.join(args.directory, i)) as f, open(os.path.join(args.directory, i[:-2]+"out")) as g:
        if args.verbose or args.special and i in args.special: print("Now we'll debug %s" % i)
        print(i+" "+str(count(subprocess.check_output(['pin', '-t', 'pin-inscount.so', '--', './.qtest.out'] if args.pin else ["./.qtest.out"], universal_newlines=True, stderr=(None if args.verbose or args.special and i in args.special else subprocess.DEVNULL), input=f.read()).strip() == g.read().strip())))
        if args.pin:
            subprocess.call(['cat', '.pintester.log'])

print(results)

if args.profiling:
    subprocess.check_call(['gprof', './.qtest.out', 'gmon.out'])

#!/usr/bin/env python3
import subprocess, os, argparse, re

parser = argparse.ArgumentParser()
parser.add_argument("directory", type=str)
parser.add_argument("-s", "--special", type=str, action='append')
args = parser.parse_args()

subprocess.check_call(["g++",'-o','./.qtest.out',os.path.join(args.directory,args.directory+".cpp")])

results = {}
def count(x):
    results[x] = results.get(x, 0) + 1
    return x

for i in sorted([x for x in os.listdir(args.directory) if x.endswith(".in")], key=lambda x: int(re.findall(r"\d+",x)[0])):
    with open(os.path.join(args.directory, i)) as f, open(os.path.join(args.directory, i[:-2]+"out")) as g:
        if args.special and i in args.special: print("Now we'll debug %s" % i)
        print(i+" "+str(count(subprocess.check_output(["./.qtest.out"], universal_newlines=True, stderr=(None if args.special and i in args.special else subprocess.DEVNULL), input=f.read()).strip() == g.read().strip())))

print(results)

#!/usr/bin/env python3
import subprocess, os, argparse

parser = argparse.ArgumentParser()
parser.add_argument("directory", type=str)
args = parser.parse_args()

subprocess.check_call(["g++",'-o','./qtest.out',os.path.join(args.directory,args.directory+".cpp")])

for i in sorted([x for x in os.listdir(args.directory) if x.endswith(".in")]):
    with open(os.path.join(args.directory, i)) as f, open(os.path.join(args.directory, i[:-2]+"out")) as g:
        print(i+" "+str(subprocess.check_output(["./qtest.out"], universal_newlines=True, input=f.read()).strip() == g.read().strip()))

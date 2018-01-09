import subprocess
import sys


def parse(outputFile, filename):
	with open(outputFile) as f:
		content = f.readlines()

	content = [x.strip() for x in content if ('label="' + filename + '\\n') in x]

	counts = {}
	for x in content:
		functionname = x.split("[")[0].strip().split("'")[0]
		if '"' in functionname:
			functionname = functionname.split('"')[1]
		if functionname not in counts:
			counts[functionname] = 0
		counts[functionname] += int(x.split("label=")[1].split("\\n")[4].split('"')[0][0:-2])

	return counts


if __name__ == '__main__':
	# filename = sys.argv[1]
	# callgrindOutput = "profile"
	# gprof2dotOutput = "profile.dot"
	# subprocess.call(("valgrind -q --tool=callgrind --callgrind-out-file=" + callgrindOutput + " ./" + filename + " > /dev/null").split(" "))
	# subprocess.call(("./gprof2dot.py -n0 -e0 --format=callgrind --output=" + gprof2dotOutput + " " + callgrindOutput).split(" "))

	counts = parse("profile.dot", "a.out")
	print counts
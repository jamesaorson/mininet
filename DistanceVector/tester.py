from pathlib import Path

import subprocess

HERE = Path(__file__).parent.resolve()
EXPECTED = HERE / 'expected'

display_bool = lambda b: 'SUCCESS' if b else 'FAIL'

def parse_output(log_file):
	""" 
	Parse log file, return list of lines 
	Handles both cases of
		1. Expected output (no excess or round/dividers)
		2. Run output (has multi-round output with dividers, grab last)
	"""

	with open(log_file) as rfile:
		lines = [line.strip() for line in rfile.readlines()]

	divider_lines = [ind for ind,line in enumerate(lines) if line.startswith('-')]
	if len(divider_lines):
		# Grab the block between last two dividers
		left, right = divider_lines[-2], divider_lines[-1]
		lines = lines[left+1:right]

	# Trim empty lines
	lines = [line for line in lines if len(line)]
	return lines

def parse_line(line):
	""" Parse out a single line"""
	node, links = line.split(':')
	pairs = [pair for pair in links.strip().split(' ')]

	return node, pairs

def outputs_equal(left_lines, right_lines):
	""" Checks expected (left) lines against output (right) lines"""

	if len(left_lines) != len(right_lines):
		return False, 'Mismatched output length'

	for i in range(len(left_lines)):
		left, right = left_lines[i], right_lines[i]
		(left_node, left_pairs), (right_node, right_pairs) = parse_line(left), parse_line(right)
		if left_node != right_node:
			return False, f'Misaligned lines: {left=} \t {right=}'


		for left_pair in left_pairs:
			if left_pair not in right_pairs: 
				return False, f' {left_node}: Expected {left_pair} but not matched to {right_pairs=}'

		for right_pair in right_pairs:
			if right_pair not in left_pairs:
				return False, f' {left_node}: Produced {right_pair} but not found in {left_pairs=}'


	return True, ''

def main():
	# Iterate over log files in the ./expected/ folder
	for expected_file in EXPECTED.glob('*.log'):
		topo = expected_file.stem

		# Run the file (assumes the {topo.txt} file exists)
		subprocess.run(f"{HERE}/run.sh {topo}", shell=True, stdout=subprocess.DEVNULL)

		# Grab the output file
		output_file = HERE / expected_file.name
		if not output_file.exists():
			raise ValueError(f"No file exists at {output_file=}")

		# Parse out the two logs
		expected_lines = parse_output(expected_file)
		output_lines = parse_output(output_file)

		# Compare
		match, explanation = outputs_equal(expected_lines, output_lines)
		print(f"({display_bool(match)}) {topo} {explanation}")



if __name__ == '__main__':
	main()

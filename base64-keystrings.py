#!/usr/bin/env python3

# Generate key base64 strings of a given input. 
# The generated key strings can then be used for searching within base64-encoded data 
# for the presence of the given search target.

import sys, argparse, base64

def validate_target(target):
	# It is impossible to generate key strings for an input fewer than five characters.
	# Additionally, the strings generated for inputs of fewer than eight characters are not particularly useful.

	if len(target) < 5:
		sys.exit("It is not possible to generate key strings for phrases shorter than 5 characters.")
	elif len(target) < 8:
		print("Warning: Inputs of fewer than eight characters generate questionably useful key strings. Beware of false positives when using these.")

def generate_padding(target_string):
	# Create three triad lists based on our target. One each of:
	# - Zero Padding
	# - One Padded Character
	# - Two Padded Characters
	# Note that the use of underscores is arbitrary.
	padding_char = "_"
	padded_strings = [target_string, padding_char + target_string, padding_char * 2 + target_string]
	return padded_strings

def generate_triads(input_strings):
	# If input_strings is a single string, normalize it to a single-element list. 
	if type(input_strings) == str:
		input_strings = [input_strings]		
	
	# Break listed strings into lists of three-character triads.
	output_triads = [] 
	for input_string in input_strings:
		triads = [input_string[i:i + 3] for i in range(0, len(input_string), 3)]
		output_triads.append(triads)

	# Clean up triad sets, removing character triads that won't be predictable in encoded text
	output_triads = cleanup_triad_sets(output_triads)
	return output_triads

def cleanup_triad_sets(input_triad_sets):	
	# Clean up a set of three triad lists.

	# Confirm we're only cleaning up three sets of character triads at a time
	if len(input_triad_sets) != 3:
		sys.exit("This function requires exactly three input triad sets.")

	# input_triad_sets[0] can keep its first block, because all three characters in it are valid.
	# input_triad_sets[1] and input_triad_sets[2] will need to have the first block dropped.
	# Additionally, if the last triad in a given list is not three characters long, 
	# it will need to be dropped. This includes input_triad_sets[0].

	# Initialize output triads list
	output_triad_sets = []

	for i in range(0, len(input_triad_sets)):
		# Loop through all three lists to clean them up.
		if args.debug is True:
			print(f"Cleaning up input_triad_sets[{i}]")
		if i != 0:
			# Not including input_triad_sets[0], drop the first item from the list
			if args.debug is True:
				print(f"Dropping first triad of input_triad_sets[{i}]: '{input_triad_sets[i][0]}'")
			del input_triad_sets[i][0]
		if len(input_triad_sets[i][-1]) != 3:
			# If the final triad in a set is not 3 characters long, drop it.
			if args.debug is True:
				print(f"Dropping incomplete final triad from input_triad_sets[{i}]: {repr(input_triad_sets[i][-1])}")
			del input_triad_sets[i][-1]
		# Finally, collapse the internal lists to strings
		input_triad_sets[i] = ''.join(input_triad_sets[i])
		if args.debug is True:
			print(f"Resulting ASCII keystring for input_triad_sets[{i}]: {repr(input_triad_sets[i])}")
		output_triad_sets.append(input_triad_sets[i])

	return output_triad_sets

def generate_key_strings(triad_sets):
	# Take a list of triad sets and convert each one to a searchable key string
	key_strings = []

	for triad_set in triad_sets: 
		target_string = "".join(triad_set)
		key_string = to_base64(target_string)
		key_strings.append(key_string)

	return key_strings

def to_base64(string):
	# Helper function to handle simple ascii string to base64 string encoding
	string_bytes = string.encode("ascii")
	base64_bytes = base64.b64encode(string_bytes)
	base64_string = base64_bytes.decode("ascii")
	return base64_string

def main():
	# Begin handling arguments.
	parser = argparse.ArgumentParser(description="Generate key base64 strings based on a given input. Returns three strings.", epilog="For complete details, please visit: http://s7n.co/b64strings")
	parser.add_argument("input", nargs='?', default=None, help="Target string to generate key base64 strings of. (Only necessary if not using --stdin or --file)")
	parser.add_argument("-f", "--file", type=argparse.FileType('r'), default=None, help="File containing target string.")
	parser.add_argument("-s", "--stdin", action="store_true", default=None, help="Use data received from stdin" )
	parser.add_argument("-d", "--debug", action="store_true", help="Enable debug messages.")
	global args
	args = parser.parse_args()

	if args.input is not None:
		# If we're given a positional input string, use that first.
		if args.debug is True:
			print("Using positional input")
		target = args.input
	elif args.file is not None:
		# If we were given a file, use that instead.
		if args.debug is True:
			print("Using file %s") % (args.file.name)
		target = args.file.read()
	elif args.stdin is True and not sys.stdin.isatty():
		# Try using stdin
		if args.debug is True:
			print("Using stdin")
		target = sys.stdin.read()
	else:
		print("No input identified. Use [-h] or [--help] for more information.")
		exit()
    
	# Confirm target string is an appropriate length
	validate_target(target)

	# Now that we've landed on our target string, we generate two additional
	# versions with one and two prepended characters of padding 
	padded_strings = generate_padding(target)

	# Then, break each version of the target string into character triads 
	triad_sets = generate_triads(padded_strings)

	if args.debug is True:
		# Print generated character triads 
		for triad_set in triad_sets:
			print(f"[DEBUG] Generated triad set: {triad_set}")

	# Convert cleaned up triad sets into base64-encoded key strings 
	key_strings = generate_key_strings(triad_sets)		

	# Print key strings
	for key_string in key_strings:
		print(key_string)


if __name__ == "__main__":
	main()
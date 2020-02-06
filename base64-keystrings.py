#!/usr/bin/env python3
""" Generate key base64 strings of a given input. 
The generated key strings can then be used for searching within base64-encoded data 
for the presence of the given search target.
"""
import sys, argparse, base64

# Begin handling arguments.
parser = argparse.ArgumentParser(description="Generate key base64 strings based on a given input. Returns three strings.", epilog="For complete details, please visit: http://s7n.co/b64strings")
parser.add_argument("input", nargs='?', default=None, help="Target string to generate key base64 strings of. (Only necessary if not using --stdin or --file)")
parser.add_argument("-f", "--file", type=argparse.FileType('r'), default=None, help="File containing target string.")
parser.add_argument("-s", "--stdin", action="store_true", default=None, help="Use data received from stdin" )
parser.add_argument("-d", "--debug", action="store_true", help="Enable debug messages.")
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

# It is impossible to generate key strings for an input fewer than five characters.
# Additionally, the strings generated for inputs of fewer than eight characters are not particularly useful.

if len(target) < 5:
	print("It is not possible to generate key strings for phrases shorter than 5 characters.")
	exit()
elif len(target) < 8:
	print("Warning: Inputs of fewer than eight characters generate questionably useful key strings. Beware of false positives when using these.")



# Now that we've landed on our target string, we break it into character triads
def triads(string):
	""" Break a given string into a list of three-character triads."""
	return [string[i:i + 3] for i in range(0, len(string), 3)]


'''

 Create three triad lists based on our target. One each of:
 - Zero Padding
 - One Padded Character
 - Two Padded Characters
 Note that the use of underscores is arbitrary.

'''
padding = [triads(target), triads("_" + target), triads("__" + target)]

if args.debug is True:
	padded = 0
	for i in padding:
		print("Triads for padding %d: %s" ) % (padded, i)
		padded += 1

'''
Clean up our triad lists.

padding[0] can keep its first block, because all three characters in it are valid.
padding[1] and padding[2] will need to have the first block dropped.
Additionally, if the last triad in a given list is not three characters long, 
it will need to be dropped. This includes padding[0].
'''
# Initialize keystrings list
keystrings = []
for i in range(0, len(padding)):
	# Loop through all three lists to clean them up.
	if args.debug is True:
		print("Cleaning up padding[%d]") % (i)
	if i is not 0:
		# Not including padding[0], drop the first item from the list
		if args.debug is True:
			print("Dropping first triad of padding[%d]: '%s'") % (i, padding[i][0])
		del padding[i][0]
	if len(padding[i][-1]) is not 3:
		# If the final triad in a set is not 3 characters long, drop it.
		if args.debug is True:
			print("Dropping incomplete final triad from padding[%d]: %s") % (i, repr(padding[i][-1]))
		del padding[i][-1]
	# Finally, collapse the internal lists to strings
	padding[i] = ''.join(padding[i])
	if args.debug is True:
		print("Resulting ASCII keystring for padding[%d]: %s") % (i, repr(padding[i]))
	keystrings.append(padding[i])
	

for i in range(0, len(keystrings)):
	keystrings[i] = base64.b64encode(bytes(keystrings[i], 'utf-8'))
	print(str(keystrings[i], "utf-8"))

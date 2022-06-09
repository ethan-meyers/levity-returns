import sys
import textwrap
import os

to_stringify = None
to_return = None
to_write = None

if len(sys.argv) == 3:
	to_stringify = sys.argv[1]
	to_return = sys.argv[2]
if len(sys.argv) == 4:
	to_stringify = sys.argv[1]
	to_return = sys.argv[2]
	to_write = sys.argv[3]
# deal with no command line argument

while not to_stringify:
	print('SQL files in the current directory: \n')
	for x in os.listdir('.'):
		if x[-4:] == ".sql":
			print(x)
	to = input("You have not specified a sql script to stringify. Please enter one now: ")
	if to:
		to_stringify = to

while not to_return:
	to = input('Your string variable needs a name! Please specify one now: ')
	to_return = to

with open(to_stringify, 'r') as text:

	if not to_write:
		with open('sql_commands.py', 'a') as output:

			lines = text.read()
			lines = lines.split('\n')
			lines = [textwrap.dedent(line) for line in lines]
			lines = [line.replace('"', '\\"') for line in lines]
			lines = [line.replace('%', '%%') for line in lines]

			# Add first quotation mark. First line requires no space.
			return_string = '\n' + to_return + ' = "' + lines[0]

			# Subsequent lines require space.
			for line in lines[1:]:
				return_string += " " + line

			# Add final quotation.
			return_string += '"\n'

			output.write(return_string)

			print(f'SINGLE-STRINGIFY is finished. {to_stringify} is now in sql_commands.py as {to_return}')
	else:
		with open(to_write, 'a') as output:

			lines = text.read()
			lines = lines.split('\n')
			lines = [textwrap.dedent(line) for line in lines]
			lines = [line.replace('"', '\\"') for line in lines]
			lines = [line.replace('%', '%%') for line in lines]
			lines = ["" if line[:2] == "--" else line for line in lines]

			# Add first quotation mark. First line requires no space.
			return_string = '\n' + to_return + ' = "' + lines[0]

			# Subsequent lines require space.
			for line in lines[1:]:
				return_string += " " + line

			# Add final quotation.
			return_string += '"\n'

			output.write(return_string)

			print(f'SINGLE-STRINGIFY is finished. {to_stringify} is now in {to_write} as {to_return}')
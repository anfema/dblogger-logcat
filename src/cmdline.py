import argparse
import itertools

from dateutil.parser import parse


# date parser
class ParseDate(argparse.Action):
	def __init__(self, option_strings, dest, nargs=None, **kwargs):
		super().__init__(option_strings, dest, **kwargs)

	def __call__(self, parser, namespace, values, option_string=None):
		setattr(namespace, self.dest, parse(values))

def parse_cmdline():
	# argument parser setup
	parser = argparse.ArgumentParser(description='Show a dblogger logfile.')
	parser.add_argument(
		'-t', '--tag',
		type=str,
		action='append',
		nargs=1,
		help='only show log lines with this tag (boolean AND)'
	)
	parser.add_argument(
		'--from',
		type=str,
		action=ParseDate,
		nargs=1,
		dest='from_date',
		help='earliest date to show'
	)
	parser.add_argument(
		'--to',
		type=str,
		action=ParseDate,
		nargs=1,
		dest='to_date',
		help='latest date to show'
	)
	parser.add_argument(
		'-l', '--level',
		type=int,
		nargs=1,
		dest='level',
		help='minimum log level to display (10: trace, 20: debug, 30: info, 40: warn, 50: error, 60: fatal)'
	)
	parser.add_argument(
		'-n', '--lines',
		type=int,
		nargs=1,
		dest='lines',
		help='maximum number of lines to output'
	)
	# parser.add_argument(
	# 	'--file',
	# 	type=str,
	# 	nargs=1,
	# 	action='append',
	# 	dest='file_filter',
	# 	help='only show log entries from that file, may be partial from right side'
	# )
	parser.add_argument(
		'-f', '--follow',
		action='store_true',
		dest='follow',
		help='follow the log output while the file is written to (like tail -f)'
	)
	parser.add_argument(
		'file',
		nargs='*',
		type=str,
		help='file to process'
	)

	args = parser.parse_args()
	if args.tag:  # flatmap tag list
		args.tag = list(itertools.chain(*args.tag))
	# if args.file_filter:  # flatmap file filter list
	# 	args.file_filter = list(itertools.chain(*args.file_filter))
	if args.level:
		args.level = args.level[-1]
	if args.lines:
		args.lines = args.lines[-1]

	return args

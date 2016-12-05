import datetime
from time import sleep

from src.cmdline import parse_cmdline
args = parse_cmdline()

from src.db import create_engines
engines = create_engines(args.file)

from src.model import Tag, Func, Source, Log

int_to_level = {
	10: 'TRACE',
	20: 'DEBUG',
	30: 'INFO ',
	40: 'WARN ',
	50: 'ERROR',
	60: 'FATAL'
}

def build_query(session):
	q = session.query(Log)

	if args.tag:
		q = q.filter(Log.tags.any(Tag.name.in_(args.tag)))

	if args.from_date:
		q = q.filter(Log.time >= datetime.datetime.fromtimestamp(args.from_date / 1000.0))

	if args.to_date:
		q = q.filter(Log.time <= datetime.datetime.fromtimestamp(args.to / 1000.0))

	if args.level:
		q = q.filter(Log.level >= args.level)

	q = q.order_by(Log.time)

	return q


def output_log(q, limit=None):
	if limit:
		count = q.count()
		q = q.offset(count - limit).limit(limit)

	maxTime = 0
	for log in q:
		tags = []
		for tag in log.tags:
			tags.append(tag.name)
		maxTime = log.time
		prefix = '{time:%Y-%m-%dT%H:%M:%S} [{level}]{tags}: '.format(
			time=datetime.datetime.fromtimestamp(log.time),
			level=int_to_level[log.level],
			tags=(' ' + (', '.join(tags))) if len(tags) > 0 else ''
		) 
		print('{prefix}{msg}'.format(
			prefix=prefix,
			msg=log.message.replace('\n', '\n' + len(prefix) * ' ')
		))

	return maxTime

if args.follow:
	limit = 10
	if args.lines:
		limit = args.lines
	maxTimes = {}
	while(42):
		for engine in engines:
			session = engine()
			q = build_query(session)
			if engine in maxTimes:
				q = q.filter(Log.time > maxTimes[engine])
			if q.count() > 0:
				sleep(0.5)
				if len(args.file) > 1:
					print(engine.file + ':')
					print((len(engine.file) + 1) * '=')
				maxTimes[engine] = output_log(q, limit=limit if engine not in maxTimes else None)
				if len(args.file) > 1:
					print()
		sleep(1)
else:
	for engine in engines:
		if len(args.file) > 1:
			print(engine.file + ':')
			print((len(engine.file) + 1) * '=')
		session = engine()
		output_log(build_query(session), limit=args.lines)
		if len(args.file) > 1:
			print()

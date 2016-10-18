# dblogger log cat for command line use

[dblogger](https://github.com/anfema/dblogger) logs to databases or SQLite files so the logfiles are binary blobs that can not be viewed easily on the command line. To make that possible again use this logcat script.

## Building

You'll need to have `SQLAlchemy>=1.1.2` and `dateutils>=0.6.6` either installed globally or in a virtualenv.

I'll describe the virtualenv variant here:

- Create a virtualenv:

```bash
cd
mkdir .logcat
pyvenv .logcat
. .logcat/bin/activate
```

- Install requirements

```bash
pip install -r Requirements.txt
```

- Build `logcat`:

```bash
git clone https://github.com/anfema/dblogger-logcat.git
cd dblogger-logcat
./build.sh
```

- Move the `logcat` script to your path

```bash
mv logcat ~/bin
```

The script automatically uses the right python from your virtualenv so just call `logcat log.db` to convert to text.

## Usage

```plain
usage: logcat [-h] [-t TAG] [--from FROM_DATE] [--to TO_DATE] [-l LEVEL]
              [-n LINES] [-f]
              [file [file ...]]

Show a dblogger logfile.

positional arguments:
  file                  file to process

optional arguments:
  -h, --help            show this help message and exit
  -t TAG, --tag TAG     only show log lines with this tag (boolean AND)
  --from FROM_DATE      earliest date to show
  --to TO_DATE          latest date to show
  -l LEVEL, --level LEVEL
                        minimum log level to display (10: trace, 20: debug,
                        30: info, 40: warn, 50: error, 60: fatal)
  -n LINES, --lines LINES
                        maximum number of lines to output
  -f, --follow          follow the log output while the file is written to
                        (like tail -f)
```

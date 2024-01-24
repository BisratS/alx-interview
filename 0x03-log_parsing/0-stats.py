import sys
import signal
import re

# Initialize counters
total_size = 0
status_codes = {200: 0, 301: 0, 400: 0, 401: 0, 403: 0, 404: 0, 405: 0, 500: 0}
line_count = 0

# Define the log line pattern
pattern = re.compile(r'^\S+ - \[\S+\] "GET /projects/260 HTTP/1.1" (\d+) (\d+)$')

def print_stats():
    print(f"Total file size: {total_size}")
    for code in sorted(status_codes.keys()):
        if status_codes[code] > 0:
            print(f"{code}: {status_codes[code]}")

def handle_sigint(sig, frame):
    print_stats()
    sys.exit(0)

# Register the signal handler
signal.signal(signal.SIGINT, handle_sigint)

try:
    for line in sys.stdin:
        match = pattern.match(line)
        if match:
            status_code, file_size = map(int, match.groups())
            if status_code in status_codes:
                status_codes[status_code] += 1
                total_size += file_size
        line_count += 1
        if line_count % 10 == 0:
            print_stats()
except KeyboardInterrupt:
    pass

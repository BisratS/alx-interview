import sys
import signal
import re

# Initialize variables
total_size = 0
status_codes = {200: 0, 301: 0, 400: 0, 401: 0, 403: 0, 404: 0, 405: 0, 500: 0}
line_count = 0

# Define the pattern for the log line
pattern = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - \[(.*?)\] "GET /projects/260 HTTP/1.1" (\d{3}) (\d+)'

def print_stats():
    global total_size, status_codes
    print(f"Total file size: {total_size}")
    for code in sorted(status_codes.keys()):
        if status_codes[code] > 0:
            print(f"{code}: {status_codes[code]}")

def handle_sigint(sig, frame):
    print("\n--- Interrupted ---")
    print_stats()
    sys.exit(0)

# Register the signal handler
signal.signal(signal.SIGINT, handle_sigint)

try:
    for line in sys.stdin:
        match = re.search(pattern, line)
        if match:
            total_size += int(match.group(4))
            status_codes[int(match.group(3))] += 1
        line_count += 1
        if line_count % 10 == 0:
            print_stats()
except KeyboardInterrupt:
    pass

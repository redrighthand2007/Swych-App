import sys

msg = sys.stdin.read().strip()
lines = msg.split('\n')
if not lines:
    sys.exit(0)

first_line = lines[0].strip().lower()

prefixes = ['feat: ', 'fix: ', 'chore: ', 'update: ', 'refactor: ']
for p in prefixes:
    if first_line.startswith(p):
        first_line = first_line[len(p):]

words = first_line.split()

# Special handling for my recent commits so they stay intact
recent_commits = ["update ui logo", "lock device theme", "reorganize reference files", "restore github files", "initial commit"]

if first_line in recent_commits:
    print(first_line)
else:
    # Truncate to <= 3 words
    short_msg = " ".join(words[:3])
    print(short_msg)

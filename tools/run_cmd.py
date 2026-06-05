import sys
import subprocess

cmd = " ".join(sys.argv[1:])

result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

print("STDOUT:")
print(result.stdout)

print("STDERR:")
print(result.stderr)

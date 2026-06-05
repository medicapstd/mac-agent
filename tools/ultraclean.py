import os

home = os.path.expanduser("~")

print("=== ULTRACLEAN STARTED ===")

# Run dedupe
os.system(f'python3 {home}/agent/tools/dedupe.py "{home}/Downloads"')
os.system(f'python3 {home}/agent/tools/dedupe.py "{home}/Desktop"')

# Run megaclean
os.system(f'python3 {home}/agent/tools/megaclean.py')

# AI report
os.system(f'python3 {home}/agent/tools/folder_summary.py "{home}/Downloads" > /tmp/ultra.txt')

os.system('ollama run llama3 "Give short Hinglish cleanup report for this Mac after maintenance: $(cat /tmp/ultra.txt)"')

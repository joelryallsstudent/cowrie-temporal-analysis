import json
import pandas as pd
import glob
 
records = []
for filepath in sorted(glob.glob("cowrie.json.2026-*")):
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except:
                continue
 
df = pd.DataFrame(records)
cmds = df[df['eventid'] == 'cowrie.command.input']
 
print("Top 5 commands:")
print()
for i, (cmd, count) in enumerate(cmds['input'].value_counts().head(5).items()):
    print(f"Rank {i+1}: {count} occurrences")
    print(f"  {cmd[:150]}")
    print()

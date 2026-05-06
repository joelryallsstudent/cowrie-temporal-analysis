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
logins = df[df['eventid'].isin(['cowrie.login.success', 'cowrie.login.failed'])]
 
print("345gs5662d34 as username:", logins[logins['username'] == '345gs5662d34'].shape[0])
print("345gs5662d34 as password:", logins[logins['password'] == '345gs5662d34'].shape[0])
print("3245gs5662d34 as username:", logins[logins['username'] == '3245gs5662d34'].shape[0])
print("3245gs5662d34 as password:", logins[logins['password'] == '3245gs5662d34'].shape[0])

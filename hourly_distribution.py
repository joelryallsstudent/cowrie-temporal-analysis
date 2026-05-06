import json
import pandas as pd
import matplotlib.pyplot as plt
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
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['hour'] = df['timestamp'].dt.hour

connections = df[df['eventid'] == 'cowrie.session.connect']

hourly = connections.groupby('hour').size()

fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(hourly.index, hourly.values, color='#2196F3', width=0.8)
ax.set_xlabel('Hour of Day (UTC)')
ax.set_ylabel('Total Connections')
ax.set_title('Connection Volume by Hour of Day (All 20 Days)')
ax.set_xticks(range(0, 24))
ax.set_xticklabels([f'{h:02d}:00' for h in range(24)], rotation=45, ha='right')
plt.tight_layout()
plt.savefig("hourly_distribution.png")
plt.close()
print("saved.")

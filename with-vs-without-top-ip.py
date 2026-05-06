import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
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
df['date'] = df['timestamp'].dt.date

connections = df[df['eventid'] == 'cowrie.session.connect']

top_ip = connections['src_ip'].value_counts().index[0]
top_ip_count = connections['src_ip'].value_counts().values[0]
print(f"Most active IP: {top_ip} ({top_ip_count} connections)")

daily_all = connections.groupby('date').size()
daily_excluded = connections[connections['src_ip'] != top_ip].groupby('date').size()

fig, ax = plt.subplots(figsize=(13, 6))
x = np.arange(len(daily_all))
width = 0.35
ax.bar(x - width/2, daily_all.values, width, label='All Traffic', color='#2196F3')
ax.bar(x + width/2, daily_excluded.reindex(daily_all.index, fill_value=0).values, width, label=f'Excluding {top_ip}', color='#4CAF50')
ax.set_xlabel('Date')
ax.set_ylabel('Number of Connections')
ax.set_title('Daily Connections: With vs Without Top Attacker IP')
ax.set_xticks(x)
ax.set_xticklabels([d.strftime('%d %b') for d in daily_all.index], rotation=45, ha='right')
ax.legend()
plt.tight_layout()
plt.savefig("with_vs_without_top_ip.png")
plt.close()
print("saved.")

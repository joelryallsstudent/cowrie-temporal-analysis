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
df['date'] = df['timestamp'].dt.date

connections = df[df['eventid'] == 'cowrie.session.connect']

daily = connections.groupby(['date', 'protocol']).size().unstack(fill_value=0)

fig, ax = plt.subplots(figsize=(13, 6))
daily.plot(kind='bar', stacked=True, ax=ax, color=['#2196F3', '#FF9800'], width=0.8)
ax.set_xlabel('Date')
ax.set_ylabel('Number of Connections')
ax.set_title('Daily Connection Volume by Protocol')
ax.legend(title='Protocol')
labels = [d.strftime('%d %b') for d in daily.index]
ax.set_xticklabels(labels, rotation=45, ha='right')
plt.tight_layout()
plt.savefig("daily-connection-volume.png")
plt.close()
print("saved.")

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

daily_pct = daily.div(daily.sum(axis=1), axis=0) * 100

fig, ax = plt.subplots(figsize=(13, 6))
ax.stackplot(range(len(daily_pct)), daily_pct['ssh'], daily_pct['telnet'],
             labels=['SSH', 'Telnet'], colors=['#2196F3', '#FF9800'], alpha=0.85)
ax.set_xlabel('Date')
ax.set_ylabel('Percentage (%)')
ax.set_title('Daily Protocol Distribution (% SSH vs % Telnet)')
ax.set_xticks(range(len(daily_pct)))
ax.set_xticklabels([d.strftime('%d %b') for d in daily_pct.index], rotation=45, ha='right')
ax.legend(loc='center right')
ax.set_ylim(0, 100)
plt.tight_layout()
plt.savefig("protocol_distribution.png")
plt.close()
print("saved.")

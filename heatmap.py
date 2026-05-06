import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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
df['day_of_week'] = df['timestamp'].dt.dayofweek

connections = df[df['eventid'] == 'cowrie.session.connect']

heatmap_data = connections.groupby(['day_of_week', 'hour']).size().unstack(fill_value=0)

day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
heatmap_data.index = [day_order[i] for i in heatmap_data.index]

fig, ax = plt.subplots(figsize=(14, 6))
sns.heatmap(heatmap_data, cmap='YlOrRd', ax=ax, linewidths=0.5,
            xticklabels=[f'{h:02d}' for h in range(24)])
ax.set_xlabel('Hour of Day (UTC)')
ax.set_ylabel('Day of the Week')
ax.set_title('Connection Heatmap: Day of Week vs Hour of Day')
plt.tight_layout()
plt.savefig("heatmap.png")
plt.close()
print("saved.")

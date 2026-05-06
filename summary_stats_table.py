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
df['hour'] = df['timestamp'].dt.hour
df['day_name'] = df['timestamp'].dt.day_name()
df['day_of_week'] = df['timestamp'].dt.dayofweek

connections = df[df['eventid'] == 'cowrie.session.connect']
logins = df[df['eventid'].isin(['cowrie.login.success', 'cowrie.login.failed'])]

total_events = len(df)
total_connections = len(connections)
ssh_count = len(connections[connections['protocol'] == 'ssh'])
telnet_count = len(connections[connections['protocol'] == 'telnet'])
ssh_pct = f"{ssh_count / total_connections * 100:.1f}%"
telnet_pct = f"{telnet_count / total_connections * 100:.1f}%"
unique_ips = connections['src_ip'].nunique()
date_range = f"{connections['date'].min()} to {connections['date'].max()}"
avg_daily = f"{connections.groupby('date').size().mean():.0f}"
peak_day = connections.groupby('date').size().idxmax()
peak_day_count = connections.groupby('date').size().max()
quietest_day = connections.groupby('date').size().idxmin()
quietest_day_count = connections.groupby('date').size().min()
hourly = connections.groupby('hour').size()
peak_hour = f"{hourly.idxmax():02d}:00 UTC"
peak_hour_count = hourly.max()
quietest_hour = f"{hourly.idxmin():02d}:00 UTC"
quietest_hour_count = hourly.min()
success_count = len(logins[logins['eventid'] == 'cowrie.login.success'])
failed_count = len(logins[logins['eventid'] == 'cowrie.login.failed'])
success_pct = f"{success_count / len(logins) * 100:.1f}%"
failed_pct = f"{failed_count / len(logins) * 100:.1f}%"
weekday_avg = f"{connections[connections['day_of_week'] < 5].groupby('date').size().mean():.0f}"
weekend_avg = f"{connections[connections['day_of_week'] >= 5].groupby('date').size().mean():.0f}"

table_data = [
    ["Observation Period", date_range],
    ["Total Events", f"{total_events:,}"],
    ["Total Connections", f"{total_connections:,}"],
    ["SSH Connections", f"{ssh_count:,} ({ssh_pct})"],
    ["Telnet Connections", f"{telnet_count:,} ({telnet_pct})"],
    ["Unique Source IPs", f"{unique_ips:,}"],
    ["Average Daily Connections", avg_daily],
    ["Weekday Average", weekday_avg],
    ["Weekend Average", weekend_avg],
    ["Peak Day", f"{peak_day} ({peak_day_count:,})"],
    ["Quietest Day", f"{quietest_day} ({quietest_day_count:,})"],
    ["Peak Hour", f"{peak_hour} ({peak_hour_count:,})"],
    ["Quietest Hour", f"{quietest_hour} ({quietest_hour_count:,})"],
    ["Successful Logins", f"{success_count:,} ({success_pct})"],
    ["Failed Logins", f"{failed_count:,} ({failed_pct})"],
]

fig, ax = plt.subplots(figsize=(10, 8))
ax.axis('off')
table = ax.table(
    cellText=table_data,
    colLabels=['Metric', 'Value'],
    cellLoc='left',
    loc='center',
    colWidths=[0.45, 0.45]
)
table.auto_set_font_size(False)
table.set_fontsize(11)
table.scale(1, 1.6)

for j in range(2):
    table[0, j].set_facecolor('#2196F3')
    table[0, j].set_text_props(color='white', fontweight='bold')

for i in range(1, len(table_data) + 1):
    for j in range(2):
        if i % 2 == 0:
            table[i, j].set_facecolor('#f5f5f5')
        else:
            table[i, j].set_facecolor('#ffffff')

ax.set_title('Summary Statistics', fontsize=14, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig("summary_stats_table.png", bbox_inches='tight', dpi=150)
plt.close()
print("saved.")

print("\nSummary Statistics:")
for row in table_data:
    print(f"  {row[0]}: {row[1]}")

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

logins = df[df['eventid'].isin(['cowrie.login.success', 'cowrie.login.failed'])]

usernames = logins['username'].value_counts().head(15)

fig, ax = plt.subplots(figsize=(10, 7))
usernames.plot(kind='barh', ax=ax, color='#2196F3')
ax.set_xlabel('Number of Attempts')
ax.set_ylabel('Username')
ax.set_title('Top 15 Attempted Usernames')
ax.invert_yaxis()
plt.tight_layout()
plt.savefig("top_15_usernames.png")
plt.close()
print("saved.")

import pandas as pd

peer = pd.read_excel("data/source_files/peer_groups.xlsx")

print(peer.columns.tolist())
print(peer.head())
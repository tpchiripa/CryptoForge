from cryptoforge.discovery.inspector import DatasetInspector

inspector = DatasetInspector()

dataset = inspector.inspect()

print(dataset)

df = inspector.load_sample()

print(df.head())

print(df.shape)
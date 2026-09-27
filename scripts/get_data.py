from beir import util
from beir.datasets.data_loader import GenericDataLoader

url = "https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/scifact.zip"
data_path = util.download_and_unzip(url, "data")
corpus, queries, qrels = GenericDataLoader(data_folder=data_path).load(split="test")

print(f"Docs: {len(corpus)}, Queries: {len(queries)}")
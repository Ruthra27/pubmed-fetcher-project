import pandas as pd

def save_to_csv(papers: list, file: str):
    df = pd.DataFrame(papers)
    df.to_csv(file, index=False)
import pandas as pd

class Preprocess:
    def __init__(self, df):
        self.df = df.copy()
    def transform(self):
        self.df[['Team 1 Score', 'Team 2 Score']] = self.df['Score'].str.split('-', expand=True).astype(int)
        self.df['Winner'] = (self.df['Winner'] == self.df['Team 2']).astype(int)
        self.df.drop(columns=['Score'], inplace=True)
        return self.df
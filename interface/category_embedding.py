import pandas as pd
import re
from sentence_transformers import SentenceTransformer
import numpy as np

#loading data (from macthed Codex and Ex to Ei) to embed and
# not need to do it each time for matching
df1=pd.read_excel('outputs/merged_approach_manual.xlsx')
categories=df1['Codex Merged Input'].tolist()

#creating model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

#mebedding the categories
embeddings = model.encode(categories, convert_to_tensor=True)

#saving the embeddings into a file
np.save('outputs/ref_db.npy', embeddings.numpy())

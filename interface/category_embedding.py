import pandas as pd
import re
from sentence_transformers import SentenceTransformer
import numpy as np

def create_reference_db(filename, columnname, outputfile, sentence_transformers_model):
    #loading data (from macthed Codex and Ex to Ei) to embed and
    # not need to do it each time for matching
    df1=pd.read_excel(filename)
    categories=df1[columnname].tolist()

    #creating model
    model = SentenceTransformer(sentence_transformers_model)

    #mebedding the categories
    embeddings = model.encode(categories, convert_to_tensor=True)

    #saving the embeddings into a file
    np.save(outputfile, embeddings.numpy())

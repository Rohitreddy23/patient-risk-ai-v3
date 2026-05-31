import pandas as pd
import numpy as np
import faiss

from sentence_transformers import SentenceTransformer

df = pd.read_csv("realtime_patient_data.csv")

documents = (
    df["Medical_Condition"].astype(str)
    + " | Medication: "
    + df["Medication"].astype(str)
    + " | Test Result: "
    + df["Test_Results"].astype(str)
)

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

embeddings = embedding_model.encode(
    documents.tolist()
)

index = faiss.IndexFlatL2(
    embeddings.shape[1]
)

index.add(
    np.array(embeddings).astype("float32")
)


def retrieve_context(query):

    query_embedding = embedding_model.encode(
        [query]
    )

    distances, indices = index.search(
        np.array(query_embedding).astype("float32"),
        3
    )

    context = "\n".join(
        documents.iloc[
            indices[0]
        ].tolist()
    )

    return context
import streamlit as st
import pandas as pd
import numpy as np
import faiss

from sentence_transformers import SentenceTransformer


@st.cache_resource
def load_rag():

    df = pd.read_csv(
        "realtime_patient_data.csv"
    ).head(1000)

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
        documents.tolist(),
        show_progress_bar=False
    )

    index = faiss.IndexFlatL2(
        embeddings.shape[1]
    )

    index.add(
        np.array(
            embeddings
        ).astype("float32")
    )

    return (
        embedding_model,
        index,
        documents
    )


def retrieve_context(query):

    model, index, documents = load_rag()

    query_embedding = model.encode(
        [query]
    )

    distances, indices = index.search(
        np.array(
            query_embedding
        ).astype("float32"),
        3
    )

    context = "\n".join(
        documents.iloc[
            indices[0]
        ].tolist()
    )

    return context
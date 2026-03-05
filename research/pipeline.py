from research.pubmed_client import search_pubmed, fetch_abstracts
from research.processor import parse_pubmed_records
from research.llm_extractor import extract_interactions
import pandas as pd
import os


ABSTRACTS_FILE = "data/abstracts.csv"
INTERACTIONS_FILE = "data/interactions.csv"


def run():

    query = (
        '("lung cancer" OR "lung carcinoma" OR "lung neoplasm") '
        'AND (gene OR genetic OR mutation OR "gene expression") '
        'AND (hasabstract[text]) AND (english[lang])'
    )

    print("Searching PubMed...")
    pmids = search_pubmed(query, retmax=500)
    pmids = [str(p) for p in pmids]
    print(f"Retrieved {len(pmids)} PMIDs")

    # ----------------------------
    # ABSTRACT HANDLING
    # ----------------------------

    if os.path.exists(ABSTRACTS_FILE):
        existing_abs_df = pd.read_csv(ABSTRACTS_FILE)
        existing_abs_pmids = set(existing_abs_df["PMID"].astype(str))
        print(f"{len(existing_abs_pmids)} abstracts already stored.")
    else:
        existing_abs_df = pd.DataFrame()
        existing_abs_pmids = set()

    new_pmids = [p for p in pmids if p not in existing_abs_pmids]

    print(f"{len(new_pmids)} new abstracts to fetch.")

    if new_pmids:
        records = fetch_abstracts(new_pmids)
        new_abs_df = parse_pubmed_records(records)

        if os.path.exists(ABSTRACTS_FILE):
            new_abs_df.to_csv(ABSTRACTS_FILE, mode="a", header=False, index=False)
        else:
            new_abs_df.to_csv(ABSTRACTS_FILE, index=False)

        abstracts_df = pd.concat([existing_abs_df, new_abs_df], ignore_index=True)
    else:
        abstracts_df = existing_abs_df

    # ----------------------------
    # INTERACTION HANDLING
    # ----------------------------

    if os.path.exists(INTERACTIONS_FILE):
        existing_int_df = pd.read_csv(INTERACTIONS_FILE)
        processed_pmids = set(existing_int_df["PMID"].astype(str))
        print(f"{len(processed_pmids)} PMIDs already processed for interactions.")
    else:
        processed_pmids = set()

    abstracts_df["PMID"] = abstracts_df["PMID"].astype(str)

    to_process_df = abstracts_df[~abstracts_df["PMID"].isin(processed_pmids)]

    print(f"{len(to_process_df)} abstracts to process with LLM.")

    new_interactions = []

    for idx, row in to_process_df.iterrows():
        pmid = row["PMID"]
        print(f"Processing PMID: {pmid}")

        interactions = extract_interactions(row["Abstract"])

        for interaction in interactions:
            interaction["PMID"] = pmid
            new_interactions.append(interaction)

    if new_interactions:
        new_int_df = pd.DataFrame(new_interactions)

        if os.path.exists(INTERACTIONS_FILE):
            new_int_df.to_csv(INTERACTIONS_FILE, mode="a", header=False, index=False)
        else:
            new_int_df.to_csv(INTERACTIONS_FILE, index=False)

        print(f"Saved {len(new_int_df)} new interactions.")
    else:
        print("No new interactions extracted.")

    print("Pipeline complete.")


if __name__ == "__main__":
    run()
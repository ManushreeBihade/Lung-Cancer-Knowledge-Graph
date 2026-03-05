import pandas as pd


def parse_pubmed_records(records):
    """
    Parse raw PubMed XML records into a structured DataFrame.
    """
    data = []

    if not records:
        return pd.DataFrame()

    for article in records.get("PubmedArticle", []):
        try:
            medline = article["MedlineCitation"]
            pmid = str(medline["PMID"])
            article_data = medline["Article"]

            title = article_data.get("ArticleTitle", "")

            # Abstract can be multiple sections
            abstract_sections = article_data.get("Abstract", {}).get("AbstractText", [])
            abstract_text = " ".join(str(section) for section in abstract_sections)

            data.append({
                "PMID": pmid,
                "Title": title,
                "Abstract": abstract_text
            })

        except Exception:
            continue

    return pd.DataFrame(data)


def save_to_csv(df, filepath="data/abstracts.csv"):
    """
    Save DataFrame to CSV file.
    """
    df.to_csv(filepath, index=False)
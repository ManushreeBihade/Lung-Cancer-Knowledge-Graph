import os
from Bio import Entrez
from dotenv import load_dotenv
import ssl
import certifi

ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())

# Load environment variables
load_dotenv()

Entrez.email = os.getenv("ENTREZ_EMAIL") #Your email

def search_pubmed(query: str, retmax: int = 20) -> list:
    handle = Entrez.esearch(
        db="pubmed",
        term=query,
        retmax=retmax
    )
    record = Entrez.read(handle)
    handle.close()

    return record["IdList"]


def fetch_abstracts(pmids: list):
    if not pmids:
        return None

    handle = Entrez.efetch(
        db="pubmed",
        id=",".join(pmids),
        rettype="abstract",
        retmode="xml"
    )
    records = Entrez.read(handle)
    handle.close()

    return records
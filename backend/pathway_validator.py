import truststore
truststore.inject_into_ssl()
from Bio import Entrez
import os

class PathwayValidator:

    def __init__(self):
        Entrez.email = os.getenv("ENTREZ_EMAIL") #Your email

    def validate_path(self, path):
        """
        Validate whether a pathway exists in PubMed.

        Example input:
        "MAPK1 → EGFR → SMARCA4"
        """

        # Extract genes
        genes = path.split(" → ")

        # Build PubMed query
        query = " AND ".join(genes)

        try:
            handle = Entrez.esearch(
                db="pubmed",
                term=query,
                retmax=5
            )

            record = Entrez.read(handle)

            count = int(record["Count"])
            pmids = record["IdList"]

            if count > 0:
                return {
                    "path": path,
                    "status": "literature_supported",
                    "count": count,
                    "pmids": pmids
                }

            return {
                "path": path,
                "status": "potentially_novel",
                "count": 0,
                "pmids": []
            }

        except Exception as e:

            return {
                "path": path,
                "status": "error",
                "message": str(e)
            }
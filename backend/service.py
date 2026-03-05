from .kg_lookup import KGLookup
from .llm_explainer import generate_explanation
from .graph_builder import build_edges
from .pathway_validator import PathwayValidator
import pandas as pd


class InteractionService:

    def __init__(self):
        self.kg = KGLookup()
        self.validator = PathwayValidator()

        # build list of genes in KG
        self.all_genes = set(self.kg.direct_df["gene_1"]).union(
            set(self.kg.direct_df["gene_2"])
        )

    # -----------------------------
    # Reconstruct 2-hop paths
    # -----------------------------
    def reconstruct_2hop_paths(self, gene1, gene2, two_hop_df):

        paths = []

        for _, row in two_hop_df.iterrows():

            intermediates = row["intermediates"]

            mediators = (
                intermediates
                .strip("[]")
                .replace(" ", "")
                .split(",")
            )

            for m in mediators:
                if m != "":
                    paths.append(f"{gene1} → {m} → {gene2}")

        return paths


    # -----------------------------
    # Reconstruct 3-hop paths
    # -----------------------------
    def reconstruct_3hop_paths(self, three_hop_df):

        paths = []

        for _, row in three_hop_df.iterrows():

            i1 = row["intermediates__001"]
            i2 = row["intermediates__002"]

            if pd.notna(i1) and pd.notna(i2):

                path = (
                    f"{row['source']} → "
                    f"{i1} → "
                    f"{i2} → "
                    f"{row['target']}"
                )

                paths.append(path)

        return paths


    # -----------------------------
    # Validate pathways
    # -----------------------------
    def validate_paths(self, paths):

        results = []

        for path in paths:
            validation = self.validator.validate_path(path)
            results.append(validation)
           
        return results


    # -----------------------------
    # Main analysis
    # -----------------------------
    def analyze(self, gene1, gene2):

        gene1 = gene1.upper()
        gene2 = gene2.upper()

        # Check gene presence
        if gene1 not in self.all_genes:
            return f"{gene1} is not present in the knowledge graph."

        if gene2 not in self.all_genes:
            return f"{gene2} is not present in the knowledge graph."

        # Lookup
        direct, two_hop, three_hop = self.kg.lookup(gene1, gene2)

        # Build paths
        two_hop_paths = self.reconstruct_2hop_paths(gene1, gene2, two_hop)
        three_hop_paths = self.reconstruct_3hop_paths(three_hop)

        # No connection case
        if direct.empty and not two_hop_paths and not three_hop_paths:
            return (
                f"{gene1} and {gene2} exist in the knowledge graph "
                "but no connection was found within 3 hops."
            )

        # -----------------------------
        # Validate pathways (Stage 3)
        # -----------------------------

        two_hop_validation = self.validate_paths(two_hop_paths)
        three_hop_validation = self.validate_paths(three_hop_paths)

        # -----------------------------
        # Build graph edges
        # -----------------------------

        edges = build_edges(
            direct,
            two_hop_paths,
            three_hop_paths
        )

        # -----------------------------
        # Generate explanation
        # -----------------------------

        explanation = generate_explanation(
            gene1,
            gene2,
            direct,
            two_hop_paths,
            three_hop_paths
        )

        return {
            "explanation": explanation,
            "edges": edges,
            "two_hop_validation": two_hop_validation,
            "three_hop_validation": three_hop_validation
        }
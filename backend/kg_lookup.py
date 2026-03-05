import pandas as pd
import os


class KGLookup:
    def __init__(self):

        base_path = os.path.join(os.path.dirname(__file__), "..", "data")

        self.direct_df = pd.read_csv(
            os.path.join(base_path, "interactions_cleaned.csv")
        )

        self.two_hop_df = pd.read_csv(
            os.path.join(base_path, "neo4j_2hop.csv")
        )

        self.three_hop_df = pd.read_csv(
            os.path.join(base_path, "neo4j_3hop.csv")
        )

        # -----------------------------
        # Fix Neo4j export structure
        # -----------------------------
        self.three_hop_df[['source', 'target']] = (
            self.three_hop_df[['source', 'target']].ffill()
        )

        if "hop_length" in self.three_hop_df.columns and "path_count" in self.three_hop_df.columns:
            self.three_hop_df[['hop_length', 'path_count']] = (
                self.three_hop_df[['hop_length', 'path_count']].ffill()
            )

        # -----------------------------
        # Normalize gene names
        # -----------------------------
        self.direct_df["gene_1"] = self.direct_df["gene_1"].str.upper()
        self.direct_df["gene_2"] = self.direct_df["gene_2"].str.upper()

        self.two_hop_df["source"] = self.two_hop_df["source"].str.upper()
        self.two_hop_df["target"] = self.two_hop_df["target"].str.upper()

        self.three_hop_df["source"] = self.three_hop_df["source"].str.upper()
        self.three_hop_df["target"] = self.three_hop_df["target"].str.upper()

    def lookup(self, g1, g2):

        g1, g2 = g1.upper(), g2.upper()

        direct = self.direct_df[
            ((self.direct_df["gene_1"] == g1) &
             (self.direct_df["gene_2"] == g2)) |
            ((self.direct_df["gene_1"] == g2) &
             (self.direct_df["gene_2"] == g1))
        ]

        two_hop = self.two_hop_df[
            ((self.two_hop_df["source"] == g1) &
             (self.two_hop_df["target"] == g2)) |
            ((self.two_hop_df["source"] == g2) &
             (self.two_hop_df["target"] == g1))
        ]

        three_hop = self.three_hop_df[
            ((self.three_hop_df["source"] == g1) &
             (self.three_hop_df["target"] == g2)) |
            ((self.three_hop_df["source"] == g2) &
             (self.three_hop_df["target"] == g1))
        ]

        return direct, two_hop, three_hop
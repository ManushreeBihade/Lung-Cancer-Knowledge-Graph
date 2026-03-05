def build_edges(direct_df, two_hop_paths, three_hop_paths):

    edges = set()

    # ------------------
    # Direct interactions
    # ------------------
    for _, row in direct_df.iterrows():
        edges.add((row["gene_1"], row["gene_2"]))

    # ------------------
    # 2-hop paths
    # ------------------
    for path in two_hop_paths:

        parts = path.split(" → ")

        if len(parts) == 3:
            edges.add((parts[0], parts[1]))
            edges.add((parts[1], parts[2]))

    # ------------------
    # 3-hop paths
    # ------------------
    for path in three_hop_paths:

        parts = path.split(" → ")

        if len(parts) == 4:
            edges.add((parts[0], parts[1]))
            edges.add((parts[1], parts[2]))
            edges.add((parts[2], parts[3]))

    return list(edges)
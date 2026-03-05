from pyvis.network import Network


def render_graph(edges, gene1, gene2):

    net = Network(
        height="600px",
        width="100%",
        directed=True
    )

    nodes_added = set()

    for src, tgt in edges:

        # Add source node
        if src not in nodes_added:

            if src == gene1 or src == gene2:
                net.add_node(
                    src,
                    label=src,
                    shape="circle",
                    color="#1f4e79",
                    size=55,   # larger query nodes
                    font={
                        "color": "white",
                        "size": 16,
                        "face": "arial"
                    }
                )
            else:
                net.add_node(
                    src,
                    label=src,
                    shape="circle",
                    color="#7ed957",
                    size=30,   # smaller mediator nodes
                    font={
                        "color": "black",
                        "size": 14,
                        "face": "arial"
                    }
                )

            nodes_added.add(src)

        # Add target node
        if tgt not in nodes_added:

            if tgt == gene1 or tgt == gene2:
                net.add_node(
                    tgt,
                    label=tgt,
                    shape="circle",
                    color="#1f4e79",
                    size=55,
                    font={
                        "color": "white",
                        "size": 16,
                        "face": "arial"
                    }
                )
            else:
                net.add_node(
                    tgt,
                    label=tgt,
                    shape="circle",
                    color="#7ed957",
                    size=30,
                    font={
                        "color": "black",
                        "size": 14,
                        "face": "arial"
                    }
                )

            nodes_added.add(tgt)

        # Add edge
        net.add_edge(src, tgt)

    output_file = "subgraph.html"

    net.save_graph(output_file)

    return output_file
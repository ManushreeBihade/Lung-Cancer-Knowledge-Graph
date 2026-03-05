import streamlit as st
import sys
import os
import streamlit.components.v1 as components

# Allow import from backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.service import InteractionService
from visualizations.graph_visualizer import render_graph

service = InteractionService()

st.set_page_config(page_title="Lung Cancer KG Explorer")

st.title("🫁 Lung Cancer Gene Interaction Explorer")

st.markdown(
    "Enter two gene symbols to explore their structural "
    "relationship within the lung cancer knowledge graph."
)

gene1 = st.text_input("Gene 1", placeholder="e.g., STK11")
gene2 = st.text_input("Gene 2", placeholder="e.g., SMARCA4")

if st.button("Analyze Interaction"):

    if not gene1 or not gene2:
        st.warning("Please enter both gene names.")

    else:

        with st.spinner("Analyzing structural relationships..."):

            result = service.analyze(
                gene1.strip().upper(),
                gene2.strip().upper()
            )

        st.markdown("---")
        st.subheader("🧠 Interaction Analysis")

        # Handle case where backend returns text instead of dictionary
        if isinstance(result, str):
            st.write(result)

        else:

            # -------------------------
            # Explanation
            # -------------------------

            st.write(result["explanation"])

            # -------------------------
            # Graph Visualization
            # -------------------------

            edges = result["edges"]

            if edges:

                st.subheader("Graph Legend")

                st.markdown("""
🔵 **Dark blue nodes** – Query genes  
🟢 **Light green nodes** – Mediator genes connecting the pathway   

Edges represent **literature-derived gene relationships** from PubMed.
""")

                html_file = render_graph(
                    edges,
                    gene1.upper(),
                    gene2.upper()
                )

                with open(html_file, "r", encoding="utf-8") as f:
                    graph_html = f.read()

                st.subheader("🕸 Knowledge Graph Subnetwork")

                components.html(graph_html, height=650)

            # -------------------------
            # Stage 3: Pathway Validation
            # -------------------------

            st.markdown("---")
            st.subheader("📚 Pathway Validation")

            # 2-hop validation
            if result["two_hop_validation"]:

                st.markdown("### 2-hop Pathways")

                for item in result["two_hop_validation"]:

                    st.markdown(f"**{item['path']}**")

                    if item["status"] == "literature_supported":

                        st.success(
                            f"Literature-supported pathway | Publications: {item['count']}"
                        )

                        if item["pmids"]:
                            st.write("Example PMIDs:", ", ".join(item["pmids"]))

                    elif item["status"] == "potentially_novel":

                        st.warning("Potentially novel pathway")

                    st.markdown("---")

            # 3-hop validation
            if result["three_hop_validation"]:

                st.markdown("### 3-hop Pathways")

                for item in result["three_hop_validation"]:

                    st.markdown(f"**{item['path']}**")

                    if item["status"] == "literature_supported":

                        st.success(
                            f"Literature-supported pathway | Publications: {item['count']}"
                        )

                        if item["pmids"]:
                            st.write("Example PMIDs:", ", ".join(item["pmids"]))

                    elif item["status"] == "potentially_novel":

                        st.warning("Potentially novel pathway")

                    st.markdown("---")
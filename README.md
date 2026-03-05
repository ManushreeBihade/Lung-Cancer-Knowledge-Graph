# 🫁 Lung Cancer Knowledge Graph Explorer

A **literature-derived biomedical knowledge graph system** that extracts gene interactions from **PubMed abstracts**, constructs a **gene interaction network**, discovers **multi-hop pathways**, and validates them using **scientific literature evidence**.

The project demonstrates how **LLMs + Knowledge Graphs + Biomedical Literature Mining** can be combined to explore structural relationships between genes involved in **lung cancer**.

---

# 🚀 Key Features

### 📚 Literature-Driven Gene Interaction Extraction

Gene–gene relationships are extracted from **PubMed abstracts** using an LLM-based extraction pipeline.

---

### 🧠 Knowledge Graph Construction

Extracted interactions are used to build a **gene interaction knowledge graph**.

Nodes represent:

```
Gene
```

Edges represent:

```
GeneA → GeneB interaction
```

---

### 🔗 Multi-Hop Pathway Discovery

The system identifies indirect gene relationships such as:

```
GeneA → GeneB → GeneC
GeneA → GeneB → GeneC → GeneD
```

Example:

```
STK11 → TP53 → SMARCA4
```

---

### 📊 Graph Visualization

Interactive network visualization using **PyVis**, highlighting:

* 🔵 Query genes
* 🟢 Mediator genes

Edges represent literature-derived interactions.

---

### 📖 Literature Validation

Each discovered pathway is validated against **PubMed**.

Results are classified as:

```
literature_supported
```

or

```
potentially_novel
```

Example result:

```
STK11 → TP53 → SMARCA4
Publications: 36
```

---

### 🤖 LLM-Generated Biological Explanation

An LLM interprets the graph structure and generates a **structured explanation** describing the relationship between the queried genes.

---

# 🧬 System Pipeline

```
PubMed Abstracts
        ↓
LLM Interaction Extraction
        ↓
Gene Interaction Dataset
        ↓
Knowledge Graph Construction
        ↓
Neo4j Graph Database
        ↓
Multi-Hop Path Discovery
        ↓
Gephi Network Analysis
        ↓
Pathway Reconstruction
        ↓
LLM Explanation
        ↓
Graph Visualization (PyVis)
        ↓
PubMed Pathway Validation
```

---

# ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/ManushreeBihade/Lung-Cancer-Knowledge-Graph.git
cd Lung-Cancer-Knowledge-Graph
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate environment:

**Windows**

```
venv\Scripts\activate
```

**Mac/Linux**

```
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file in the root directory.

```
GROQ_API_KEY=your_api_key
ENTREZ_EMAIL=your_email
```

Used for:

* LLM explanation generation
* PubMed API access

---

# ▶️ Running the Application

Launch the Streamlit interface:

```bash
streamlit run frontend/app.py
```

Then open:

```
http://localhost:8501
```

Enter two gene symbols to explore their relationship.

Example:

```
Gene 1: STK11
Gene 2: SMARCA4
```


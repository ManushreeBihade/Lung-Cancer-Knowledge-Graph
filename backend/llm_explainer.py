import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.1-8b-instant"


def generate_explanation(gene1, gene2, direct_df, two_hop_paths, three_hop_paths):

    direct_text = (
        direct_df.to_string(index=False)
        if not direct_df.empty
        else "None"
    )

    two_hop_text = (
        f"{len(two_hop_paths)} paths:\n" + "\n".join(two_hop_paths)
        if two_hop_paths else "None"
    )

    three_hop_text = (
        f"{len(three_hop_paths)} paths:\n" + "\n".join(three_hop_paths)
        if three_hop_paths else "None"
    )

    context = f"""
Gene 1: {gene1}
Gene 2: {gene2}

Direct interactions:
{direct_text}

2-hop structural connections:
{two_hop_text}

3-hop cascade connections:
{three_hop_text}
"""

    prompt = f"""
You are a biomedical knowledge graph reasoning assistant.

Using ONLY the structured data below, explain the relationship
between the two genes.

Rules:
- Do NOT hallucinate.
- Do NOT invent biological facts.
- Clearly separate:
  • Direct evidence
  • 2-hop structural connections
  • 3-hop cascade connections
- Mention the number of paths when describing connections.
- If no interaction exists, clearly state that.

Structured Data:
{context}
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content
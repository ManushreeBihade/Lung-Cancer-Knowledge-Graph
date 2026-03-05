import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL_NAME = "gpt-4o-mini"   # fast + cheaper model


def build_prompt(abstract_text: str) -> str:
    prompt = f"""
You are a biomedical information extraction system.

Your task:
Extract explicitly stated gene–gene interactions related to Lung Cancer from the abstract below.

Rules:
- Extract ONLY relationships clearly stated in the text.
- Do NOT infer or add background knowledge.
- Do NOT hallucinate.
- Both gene_1 and gene_2 must be gene names or gene symbols.
- Exclude:
    • drugs or chemical compounds
    • therapies
    • cell types
    • immune cells
    • signaling pathways
    • mutation labels (e.g., L858R)
    • gene amplification or expression events
- The relation must represent a meaningful biological relationship
  (e.g., activates, inhibits, suppresses, regulates, stabilizes,
   binds, interacts with, correlates with, associated with).
- Use the EXACT wording of the relationship as written in the abstract.
- Do NOT paraphrase.
- Do NOT convert wording (e.g., do NOT change "negative effect" to "inhibits").
- Do NOT change correlation into inhibition or activation.
- Do NOT extract genes merely listed together.
- Do NOT extract fusion notation (e.g., "::").
- If no valid gene–gene interaction exists, return [].

Output MUST be valid JSON.
Output MUST be a list of objects with:
    - gene_1
    - relation
    - gene_2
    - disease

The disease must always be:
"Lung Cancer"

Abstract:
\"\"\"{abstract_text}\"\"\"

Return ONLY JSON.
"""
    return prompt


def extract_interactions(abstract_text: str):
    """
    Send abstract to OpenAI and return parsed JSON interactions.
    """

    prompt = build_prompt(abstract_text)

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You output strict JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        raw_text = response.choices[0].message.content.strip()

        try:
            return json.loads(raw_text)
        except json.JSONDecodeError:
            # Try extracting JSON block if extra text exists
            start = raw_text.find("[")
            end = raw_text.rfind("]") + 1
            if start != -1 and end != -1:
                json_block = raw_text[start:end]
                return json.loads(json_block)
            return []

    except Exception as e:
        print("OpenAI Error:", e)
        return []
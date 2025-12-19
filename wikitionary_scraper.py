
"""
Enrich an Italian A1 vocabulary CSV with part of speech and gender
using Wiktionary.

- Preserves existing annotations
- Gender only applied to nouns
- Multiple POS are joined with '; '
- Ambiguous entries are noted, not guessed
"""

import pandas as pd
import requests

WIKTIONARY_API = "https://en.wiktionary.org/w/api.php"


def query_wiktionary(word: str) -> dict:
    """
    Query Wiktionary for an Italian word.

    Returns a dictionary with:
    - pos: set[str]
    - gender: set[str]
    """
    params = {
        "action": "query",
        "format": "json",
        "titles": word,
        "prop": "revisions",
        "rvprop": "content",
        "rvslots": "main",
    }

    response = requests.get(WIKTIONARY_API, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    pages = data["query"]["pages"]
    page = next(iter(pages.values()))

    result = {"pos": set(), "gender": set()}

    if "revisions" not in page:
        return result

    text = page["revisions"][0]["slots"]["main"]["*"]

    in_italian = False
    for line in text.splitlines():
        if line.startswith("==Italian=="):
            in_italian = True
            continue
        if in_italian and line.startswith("=="):
            break

        if in_italian:
            if line.startswith("===Noun==="):
                result["pos"].add("noun")
            elif line.startswith("===Verb==="):
                result["pos"].add("verb")
            elif line.startswith("===Adjective==="):
                result["pos"].add("adjective")
            elif line.startswith("===Adverb==="):
                result["pos"].add("adverb")
            elif line.startswith("===Article==="):
                result["pos"].add("article")

            if "{{it-noun" in line:
                if "|m" in line:
                    result["gender"].add("masculine")
                if "|f" in line:
                    result["gender"].add("feminine")

    return result


def enrich_csv(
    input_path: str,
    output_path: str,
) -> None:
    """
    Enrich a CSV with POS and gender using Wiktionary.
    """
    df = pd.read_csv(input_path)

    italian_col, english_col, pos_col, gender_col = df.columns[:4]

    if "notes" not in df.columns:
        df["notes"] = ""

    for idx, row in df.iterrows():
        if pd.notna(row[pos_col]) or pd.notna(row[gender_col]):
            continue

        word = str(row[italian_col]).strip()
        if not word:
            continue

        info = query_wiktionary(word)

        if info["pos"]:
            df.at[idx, pos_col] = "; ".join(sorted(info["pos"]))

        if "noun" in info["pos"] and info["gender"]:
            df.at[idx, gender_col] = "; ".join(sorted(info["gender"]))

        if len(info["pos"]) > 1:
            df.at[idx, "notes"] = "multiple parts of speech"

    df.to_csv(output_path, index=False)


if __name__ == "__main__":
    enrich_csv(
        input_path="A1_Vocab.csv",
        output_path="A1_Vocab_wiktionary_enriched.csv",
    )

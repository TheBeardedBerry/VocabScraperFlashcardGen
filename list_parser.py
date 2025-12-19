from typing import List


def read_lines(path: str) -> List[str]:
    """
    Read all lines from a text file.

    :param path: Path to the input text file.
    :return: List of lines without trailing newlines.
    """
    with open(path, "r", encoding="utf-8") as file:
        return [line.rstrip("\n") for line in file]


def compute_column_widths(rows: List[List[str]]) -> List[int]:
    """
    Compute the maximum width of each word column.

    :param rows: A list of word lists (one list per line).
    :return: List of maximum column widths.
    """
    max_columns = max(len(row) for row in rows)

    widths = [0] * max_columns
    for row in rows:
        for index, word in enumerate(row):
            widths[index] = max(widths[index], len(word))

    return widths


def align_rows(rows: List[List[str]], widths: List[int]) -> List[str]:
    """
    Align rows of words into evenly spaced columns.

    :param rows: A list of word lists.
    :param widths: Column widths to align against.
    :return: List of aligned strings.
    """
    aligned_lines = []

    for row in rows:
        padded_words = []
        for index, width in enumerate(widths):
            word = row[index] if index < len(row) else ""
            padded_words.append(word.ljust(width))
        aligned_lines.append(" ".join(padded_words).rstrip())

    return aligned_lines


def align_text_file(input_path: str, output_path: str) -> None:
    """
    Align words in a text file so each word column lines up vertically.

    :param input_path: Path to the input text file.
    :param output_path: Path to write the aligned output.
    """
    lines = read_lines(input_path)
    rows = [line.split() for line in lines]

    if not rows:
        return

    widths = compute_column_widths(rows)
    aligned_lines = align_rows(rows, widths)

    with open(output_path, "w", encoding="utf-8") as file:
        for line in aligned_lines:
            file.write(line + "\n")


if __name__ == "__main__":
    align_text_file("A1_vocab.txt", "A1_Vocab.csv")
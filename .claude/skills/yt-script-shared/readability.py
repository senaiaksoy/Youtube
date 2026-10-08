"""Rough readability check for a spoken-script body (FR/EN/TR).

Usage: python readability.py <body.txt>

Reports words per sentence, syllables per word, Kandel-Moles (French Flesch),
an English Flesch-Kincaid grade (rough proxy for other languages), the share of
sentences over 20 words, and the longest sentences. It does not measure how
hard medical terms are; check jargon separately.
"""
import re
import sys

VOWELS = r"[aeiouyàâäéèêëîïôöùûüœıİ]+"


def syllables(word: str) -> int:
    w = word.lower()
    if len(w) > 3:
        w = re.sub(r"(e|es|ent)$", "", w)
    return max(1, len(re.findall(VOWELS, w)))


def main(path: str) -> None:
    text = open(path, encoding="utf-8").read()
    sentences = [s for s in re.split(r"(?<=[.!?…])\s+|\n+", text) if re.search(r"\w", s)]
    words = re.findall(r"[A-Za-zÀ-ÿœŒğüşöçıİĞÜŞÖÇ0-9]+(?:[-'’][A-Za-zÀ-ÿ]+)*", text)
    if not sentences or not words:
        print("empty text")
        return
    asl = len(words) / len(sentences)
    asw = sum(syllables(w) for w in words) / len(words)
    kandel_moles = 207 - 1.015 * asl - 73.6 * asw
    fk_grade = 0.39 * asl + 11.8 * asw - 15.59
    long_share = sum(len(s.split()) > 20 for s in sentences) / len(sentences)
    print(f"sentences {len(sentences)} | words {len(words)} | words/sentence {asl:.1f} | syllables/word {asw:.2f}")
    print(f"Kandel-Moles (FR) {kandel_moles:.0f} (target >= 80) | FK grade (rough) {fk_grade:.1f} | sentences >20 words {long_share:.0%} (target <= 15%)")
    print("Longest sentences:")
    for s in sorted(sentences, key=lambda s: -len(s.split()))[:6]:
        print(f"  {len(s.split()):>3}  {s[:140]}")


if __name__ == "__main__":
    main(sys.argv[1])

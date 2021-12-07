import re
from typing import Optional

from pymorphy2 import MorphAnalyzer
from pymorphy2.analyzer import Parse

vowels = "аеёиоуыэюя"
consonants = "бвгджзйклмнпрстфхцчшщ"

rhymes = {
    "а": "хуя",
    "е": "хуе",
    "ё": "хуё",
    "и": "хуи",
    "о": "хуё",
    "у": "хую",
    "ы": "хуи",
    "э": "хуе",
    "ю": "хую",
    "я": "хуя",
}


def get_syllable_rhyme(syllable: str) -> str:
    if not syllable or not is_vowel(syllable[-1]):
        return syllable
    return rhymes[syllable[-1]]


def get_first_syllable(word: str) -> str:
    result = []

    read_vowel = False

    for letter in word:
        is_letter_vowel = is_vowel(letter)
        if read_vowel and not is_letter_vowel:
            break
        if is_letter_vowel:
            read_vowel = True
        result.append(letter)

    return "".join(result)


def is_vowel(character: str) -> bool:
    return character in vowels


def is_consonant(character: str) -> bool:
    return character in consonants


def is_noun(tag: Parse) -> bool:
    return "NOUN" in tag.tag


def is_adjective(tag: Parse) -> bool:
    return "ADJF" in tag.tag or "ADJS" in tag.tag


def is_rhymable(word: str) -> bool:
    """Возвращает True, если слово подходит под критерий рифмовки,
    т.е. является существительным или прилагательным"""
    analyzer = MorphAnalyzer()
    morphs = analyzer.parse(word)

    tags = [tag for tag in morphs if is_noun(tag) or is_adjective(tag)]

    if not tags:
        return False

    return True


def get_rhyme(word: str) -> str:
    """Подбирает рифму для слова, если это существительное или прилагательное"""
    if not is_rhymable(word):
        return word

    syllable = get_first_syllable(word)

    if not syllable or syllable == word:
        return word

    return get_syllable_rhyme(syllable) + word.removeprefix(syllable)


def split_words(text: str) -> list[str]:
    word_boundary = re.compile(r"\b")

    return word_boundary.split(text)


def get_rhymes(text: str) -> Optional[str]:
    input_text = text.lower()
    words = split_words(input_text)
    rhymed_text = "".join([get_rhyme(word) for word in words])
    if rhymed_text == input_text:
        return None
    return rhymed_text


__all__ = ['get_rhymes']

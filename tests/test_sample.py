from hassil import parse_sentence
from hassil.intents import RangeFractionType, RangeSlotList, TextSlotList
from hassil.sample import sample_sentence


def test_text_chunk():
    assert set(sample_sentence(parse_sentence("this is a test"))) == {"this is a test"}


def test_group():
    assert set(sample_sentence(parse_sentence("this (is a) test"))) == {
        "this is a test"
    }


def test_optional():
    assert set(sample_sentence(parse_sentence("turn on [the] light[s]"))) == {
        "turn on light",
        "turn on lights",
        "turn on the light",
        "turn on the lights",
    }


def test_double_optional():
    assert set(sample_sentence(parse_sentence("turn [on] [the] light[s]"))) == {
        "turn light",
        "turn lights",
        "turn on light",
        "turn on lights",
        "turn the light",
        "turn the lights",
        "turn on the light",
        "turn on the lights",
    }


def test_alternative():
    assert set(sample_sentence(parse_sentence("this is (the | a) test"))) == {
        "this is a test",
        "this is the test",
    }


def test_list():
    sentence = parse_sentence("turn off {area}")
    areas = TextSlotList.from_strings(["kitchen", "living room"])
    assert set(sample_sentence(sentence, slot_lists={"area": areas})) == {
        "turn off kitchen",
        "turn off living room",
    }


def test_list_range():
    sentence = parse_sentence("run test {num}")
    num_list = RangeSlotList(name=None, start=1, stop=3)
    assert set(sample_sentence(sentence, slot_lists={"num": num_list})) == {
        "run test 1",
        "run test 2",
        "run test 3",
    }


def test_list_range_missing_language():
    sentence = parse_sentence("run test {num}")
    num_list = RangeSlotList(name=None, start=1, stop=3, words=True)

    # Range slot digits cannot be converted to words without a language available.
    assert set(sample_sentence(sentence, slot_lists={"num": num_list})) == {
        "run test 1",
        "run test 2",
        "run test 3",
    }


def test_list_range_words():
    sentence = parse_sentence("run test {num}")
    num_list = RangeSlotList(name=None, start=1, stop=3, words=True)
    assert set(
        sample_sentence(sentence, slot_lists={"num": num_list}, language="en")
    ) == {
        "run test 1",
        "run test one",
        "run test 2",
        "run test two",
        "run test 3",
        "run test three",
    }


def test_list_range_halves_words():
    sentence = parse_sentence("run test {num}")
    num_list = RangeSlotList(
        name=None, start=1, stop=1, fraction_type=RangeFractionType.HALVES, words=True
    )
    assert set(
        sample_sentence(sentence, slot_lists={"num": num_list}, language="en")
    ) == {
        "run test 1",
        "run test one",
        "run test 1.5",
        "run test one point five",
    }


def test_list_range_tenths_words():
    sentence = parse_sentence("run test {num}")
    num_list = RangeSlotList(
        name=None, start=1, stop=1, fraction_type=RangeFractionType.TENTHS, words=True
    )
    assert set(
        sample_sentence(sentence, slot_lists={"num": num_list}, language="en")
    ) == {
        "run test 1",
        "run test one",
        "run test 1.1",
        "run test one point one",
        "run test 1.2",
        "run test one point two",
        "run test 1.3",
        "run test one point three",
        "run test 1.4",
        "run test one point four",
        "run test 1.5",
        "run test one point five",
        "run test 1.6",
        "run test one point six",
        "run test 1.7",
        "run test one point seven",
        "run test 1.8",
        "run test one point eight",
        "run test 1.9",
        "run test one point nine",
    }


def test_rule():
    sentence = parse_sentence("turn off <area>")
    assert set(
        sample_sentence(
            sentence,
            expansion_rules={"area": parse_sentence("[the] kitchen")},
        )
    ) == {"turn off kitchen", "turn off the kitchen"}


def test_permutation():
    assert set(sample_sentence(parse_sentence("a;b;[c] d"))) == {
        "a b d",
        "a b c d",
        "a c d b",
        "a d b",
        "b a d",
        "b a c d",
        "b c d a",
        "b d a",
        "c d a b",
        "c d b a",
        "d a b",
        "d b a",
    }


def test_skip_optionals() -> None:
    assert set(sample_sentence(parse_sentence("a [b] c [d]"), skip_optionals=True)) == {
        "a c "
    }

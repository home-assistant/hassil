from hassil import parse_sentence
from hassil.intents import RangeSlotList, TextSlotList
from hassil.sample import sample_expression


def test_text_chunk():
    assert set(sample_expression(parse_sentence("this is a test"))) == {
        "this is a test"
    }


def test_group():
    assert set(sample_expression(parse_sentence("this (is a) test"))) == {
        "this is a test"
    }


def test_optional():
    assert set(sample_expression(parse_sentence("turn on [the] light[s]"))) == {
        "turn on light",
        "turn on lights",
        "turn on the light",
        "turn on the lights",
    }


def test_double_optional():
    assert set(sample_expression(parse_sentence("turn [on] [the] light[s]"))) == {
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
    assert set(sample_expression(parse_sentence("this is (the | a) test"))) == {
        "this is a test",
        "this is the test",
    }


def test_list():
    sentence = parse_sentence("turn off {area}")
    areas = TextSlotList.from_strings(["kitchen", "living room"])
    assert set(sample_expression(sentence, slot_lists={"area": areas})) == {
        "turn off kitchen",
        "turn off living room",
    }


def test_list_range():
    sentence = parse_sentence("run test {num}")
    num_list = RangeSlotList(name=None, start=1, stop=3)
    assert set(sample_expression(sentence, slot_lists={"num": num_list})) == {
        "run test 1",
        "run test 2",
        "run test 3",
    }


def test_list_range_missing_language():
    sentence = parse_sentence("run test {num}")
    num_list = RangeSlotList(name=None, start=1, stop=3, words=True)

    # Range slot digits cannot be converted to words without a language available.
    assert set(sample_expression(sentence, slot_lists={"num": num_list})) == {
        "run test 1",
        "run test 2",
        "run test 3",
    }


def test_list_range_words():
    sentence = parse_sentence("run test {num}")
    num_list = RangeSlotList(name=None, start=1, stop=3, words=True)
    assert set(
        sample_expression(sentence, slot_lists={"num": num_list}, language="en")
    ) == {
        "run test 1",
        "run test one",
        "run test 2",
        "run test two",
        "run test 3",
        "run test three",
    }


def test_rule():
    sentence = parse_sentence("turn off <area>")
    assert set(
        sample_expression(
            sentence,
            expansion_rules={"area": parse_sentence("[the] kitchen")},
        )
    ) == {"turn off kitchen", "turn off the kitchen"}

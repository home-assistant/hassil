from hassil.expression import (
    ListReference,
    RuleReference,
    Sentence,
    Sequence,
    SequenceType,
    TextChunk,
)
from hassil.parse_expression import parse_expression, parse_sentence
from hassil.parser import next_chunk

# -----------------------------------------------------------------------------


def test_word():
    assert parse_expression(next_chunk("test")) == t(text="test")


def test_group_in_group():
    assert parse_expression(next_chunk("((test test2))")) == group(
        items=[group(items=[t(text="test "), t(text="test2")])],
    )


def test_optional():
    assert parse_expression(next_chunk("[test test2]")) == alt(
        items=[
            group(
                items=[t(text="test "), t(text="test2")],
            ),
            TextChunk.empty(),
        ],
    )


def test_group_alternative():
    assert parse_expression(next_chunk("(test | test2)")) == alt(
        items=[group(items=[t(text="test ")]), group(items=[t(text=" test2")])],
    )


def test_group_permutation():
    assert parse_expression(next_chunk("(test; test2)")) == alt(
        items=[
            group(
                items=[
                    t(text=" "),
                    group(items=[t(text="test")]),
                    t(text=" "),
                    group(items=[t(text=" test2")]),
                    t(text=" "),
                ]
            ),
            group(
                items=[
                    t(text=" "),
                    group(items=[t(text=" test2")]),
                    t(text=" "),
                    group(items=[t(text="test")]),
                    t(text=" "),
                ]
            ),
        ],
    )


def test_slot_reference():
    assert parse_expression(next_chunk("{test}")) == ListReference(list_name="test")


def test_rule_reference():
    assert parse_expression(next_chunk("<test>")) == RuleReference(rule_name="test")


def test_sentence_no_group():
    assert parse_sentence("this is a test") == Sentence(
        items=[t(text="this "), t(text="is "), t(text="a "), t(text="test")]
    )


def test_sentence_group():
    assert parse_sentence("(this is a test)") == Sentence(
        items=[t(text="this "), t(text="is "), t(text="a "), t(text="test")]
    )


def test_sentence_optional():
    assert parse_sentence("[this is a test]") == Sentence(
        type=SequenceType.ALTERNATIVE,
        items=[
            group(
                items=[
                    t(text="this "),
                    t(text="is "),
                    t(text="a "),
                    t(text="test"),
                ]
            ),
            TextChunk.empty(),
        ],
    )


def test_sentence_optional_suffix():
    assert parse_sentence("test[s]") == Sentence(
        type=SequenceType.GROUP,
        items=[
            t(text="test"),
            alt(items=[group(items=[t(text="s")]), TextChunk.empty()]),
        ],
    )


def test_sentence_alternative_whitespace():
    assert parse_sentence("test ( 1 | 2)") == Sentence(
        type=SequenceType.GROUP,
        items=[
            t(text="test "),
            alt(items=[group(items=[t(text=" 1 ")]), group(items=[t(text=" 2")])]),
        ],
    )


# -----------------------------------------------------------------------------


def t(**kwargs):
    return TextChunk(**kwargs)


def group(**kwargs):
    return Sequence(type=SequenceType.GROUP, **kwargs)


def alt(**kwargs):
    return Sequence(type=SequenceType.ALTERNATIVE, **kwargs)

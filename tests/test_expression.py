import unittest

from hassil.parser import ParseChunk, ParseType, next_chunk
from hassil.expression import (
    TextChunk,
    Sequence,
    SequenceType,
    ListReference,
    RuleReference,
    Sentence,
)
from hassil.parse_expression import parse_expression

# -----------------------------------------------------------------------------


def test_word():
    assert parse_expression(next_chunk("test")) == t(text="test")


# class SequenceTestCase(unittest.TestCase):
#     def test_group(self):
#         self.assertEqual(
#             parse_expression(next_chunk("(test test2)")),
#             group(
#                 items=[w(text="test"), w(text="test2")],
#             ),
#         )

#     def test_group_sub_word(self):
#         self.assertEqual(
#             parse_expression(next_chunk("(test test2):test3")),
#             group(items=[w(text="test"), w(text="test2")], substitution="test3"),
#         )

#     def test_group_sub_group(self):
#         self.assertEqual(
#             parse_expression(next_chunk("(test test2):(test3 test4)")),
#             group(
#                 items=[w(text="test"), w(text="test2")], substitution=["test3", "test4"]
#             ),
#         )

#     def test_group_tag(self):
#         self.assertEqual(
#             parse_expression(next_chunk("(test test2){test3}")),
#             group(items=[w(text="test"), w(text="test2")], tag=Tag(tag_text="test3")),
#         )

#     def test_group_in_group(self):
#         self.assertEqual(
#             parse_expression(next_chunk("((test test2))")),
#             group(
#                 items=[group(items=[w(text="test"), w(text="test2")])],
#             ),
#         )

#     def test_optional(self):
#         self.assertEqual(
#             parse_expression(next_chunk("[test test2]")),
#             alt(
#                 items=[
#                     group(
#                         items=[Word(text="test"), Word(text="test2")],
#                     ),
#                     Word.empty(),
#                 ],
#             ),
#         )

#     def test_group_alternative(self):
#         self.assertEqual(
#             parse_expression(next_chunk("(test | test2)")),
#             alt(
#                 items=[group(items=[w(text="test")]), group(items=[w(text="test2")])],
#             ),
#         )


# # -----------------------------------------------------------------------------


# class ReferenceTestCase(unittest.TestCase):
#     def test_slot_reference(self):
#         self.assertEqual(
#             parse_expression(next_chunk("$test")), SlotReference(slot_name="test")
#         )

#     def test_rule_reference(self):
#         self.assertEqual(
#             parse_expression(next_chunk("<test>")), RuleReference(rule_name="test")
#         )


# # -----------------------------------------------------------------------------


# class NumberTestCase(unittest.TestCase):
#     def test_number(self):
#         self.assertEqual(parse_expression(next_chunk("100")), Number(number=100))

#     def test_number_range(self):
#         self.assertEqual(
#             parse_expression(next_chunk("1..100")),
#             NumberRange(lower_bound=1, upper_bound=100),
#         )

#     def test_number_range_with_step(self):
#         self.assertEqual(
#             parse_expression(next_chunk("1..100,2")),
#             NumberRange(lower_bound=1, upper_bound=100, step=2),
#         )


# # -----------------------------------------------------------------------------


# class SentenceTestCase(unittest.TestCase):
#     def test_no_group(self):
#         self.assertEqual(
#             Sentence.parse("this is a test"),
#             Sentence(items=[w(text="this"), w(text="is"), w(text="a"), w(text="test")]),
#         )

#     def test_group(self):
#         self.assertEqual(
#             Sentence.parse("(this is a test)"),
#             Sentence(items=[w(text="this"), w(text="is"), w(text="a"), w(text="test")]),
#         )

#     def test_optional(self):
#         self.assertEqual(
#             Sentence.parse("[this is a test]"),
#             Sentence(
#                 type=SequenceType.ALTERNATIVE,
#                 items=[
#                     group(
#                         items=[
#                             w(text="this"),
#                             w(text="is"),
#                             w(text="a"),
#                             w(text="test"),
#                         ]
#                     ),
#                     Word.empty(),
#                 ],
#             ),
#         )


# -----------------------------------------------------------------------------


def t(**kwargs):
    return TextChunk(**kwargs)


def group(**kwargs):
    return Sequence(type=SequenceType.GROUP, **kwargs)


def alt(**kwargs):
    return Sequence(type=SequenceType.ALTERNATIVE, **kwargs)

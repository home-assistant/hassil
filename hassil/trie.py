"""Specialized implementation of a trie.

See: https://en.wikipedia.org/wiki/Trie
"""

from collections import deque
from dataclasses import dataclass
from typing import Any, Dict, Iterable, Optional, Tuple


@dataclass
class TrieNode:
    """Node in trie."""

    id: int
    text: Optional[str] = None
    value: Any = None
    children: "Optional[Dict[str, TrieNode]]" = None


class Trie:
    """A specialized trie data structure that finds all known words in a string."""

    def __init__(self) -> None:
        self.roots: Dict[str, TrieNode] = {}
        self._next_id = 0

    def insert(self, text: str, value: Any) -> None:
        """Insert a word and value into the trie."""
        current_node: Optional[TrieNode] = None
        current_children: Optional[Dict[str, TrieNode]] = self.roots

        last_idx = len(text) - 1
        for i, c in enumerate(text):
            if current_children is None:
                assert current_node is not None
                current_node.children = current_children = {}

            current_node = current_children.get(c)
            if current_node is None:
                current_node = TrieNode(id=self.next_id())
                current_children[c] = current_node

            if i == last_idx:
                current_node.text = text
                current_node.value = value

            current_children = current_node.children

    def find(self, text: str) -> Iterable[Tuple[str, Any]]:
        """Yield (text, value) pairs of all words found in the string."""
        q = deque([(self.roots, text)])
        visited = set()

        while q:
            item = q.popleft()
            current_children, current_text = item
            if not current_text:
                continue

            current_char = current_text[0]
            next_text = current_text[1:]

            if next_text:
                q.append((current_children, next_text))

            node = current_children.get(current_char)
            if (node is not None) and (node.id not in visited):
                visited.add(node.id)

                if node.text is not None:
                    yield (node.text, node.value)

                if node.children and next_text:
                    q.append((node.children, next_text))

    def next_id(self) -> int:
        current_id = self._next_id
        self._next_id += 1
        return current_id

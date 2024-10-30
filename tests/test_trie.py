from hassil.trie import Trie


def test_insert_find() -> None:
    trie = Trie()
    trie.insert("1", 1)
    trie.insert("two", 2)
    trie.insert("twenty two", 22)

    assert list(trie.find("set to 1")) == [("1", 1)]
    assert list(trie.find("set to 1, then two, then finally twenty two please")) == [
        ("1", 1),
        ("two", 2),
        ("twenty two", 22),
    ]

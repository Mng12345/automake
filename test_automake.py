import unittest
from typing import List
from automake import *


def test_parse_includes():
    file1: str = "E:\\word2vec_me\\word2vec.c"
    file2: str = "E:/word2vec_me/word2vec.c"
    file3: str = "E:/cutils/random.c"
    includes1: List[str] = parse_includes(file1)
    includes2: List[str] = parse_includes(file2)
    includes3: List[str] = parse_includes(file3)
    assert len(includes1) == 1
    assert includes1[0] == "E:/cutils/random.h"
    assert len(includes2) == 1
    assert includes2[0] == "E:/cutils/random.h"
    assert len(includes3) == 1
    assert includes3[0] == "E:/cutils/random.h"


def test_makefile():
    main_file = "E:/word2vec_me/word2vec.c"
    make_file: List[str] = []
    makefile(main_file=main_file, curr_file=main_file, make_file=make_file, debug=True)
    for file in make_file:
        print(file)


if __name__ == "__main__":
    test_makefile()


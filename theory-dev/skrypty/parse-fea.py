#!/usr/bin/env python3

from fontTools.feaLib.parser import Parser

input_fea = sys.argv[1]

def parse_fea(input_fea):
    from fontTools.feaLib.parser import Parser
    Parser('tst01-anchors.fea').parse()


input_fea = sys.argv[1]

from app.nlp import *

def test_remove_non_alphanum():
    inp = 'A.? + 12312 anc N p'
    expect = 'A  12312 anc N p'
    assert remove_non_alphanum(inp) == expect

def test_simple_tokenizer():
    inp = 'framework makes easy to write small tests, yet scales complex functional testing for applications.'
    expect = ['framework', 'make', 'easy', 'ten', 'write', 'small', \
              'test', 'yet', 'scale', 'complex', 'functional', 'test', 'for', 'application']
    assert simple_tokenizer(inp) == expect

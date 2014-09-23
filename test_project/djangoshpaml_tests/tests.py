from os.path import join

import sys

from django.conf import settings
from django.test import TestCase

def write(*a, **kw):
    sys.stdout.write(*a, **kw)
    sys.stdout.flush()

def assert_equals(expected_output, actual_output):
    if expected_output != actual_output:
        write("\nexpected:" + repr(expected_output))
        write("\nactual  :" + repr(actual_output))
        raise Exception('values not equal')

def assert_shpaml(expected_output, source):
    from shpaml import shpaml
    actual_output = shpaml.convert_text(source).strip()
    assert_equals(expected_output.strip(), actual_output)

def assert_indent(expected_output, source):
    from shpaml import shpaml
    def dot(s):
        return '. ' + s
    if '. ' in expected_output:
        leaf_method = dot
    else:
        leaf_method = lambda x: x
    def clean(s):
        return s.strip()
    assert_equals(
            clean(expected_output),
            clean(
                shpaml.indent(clean(source),
                    test_branch_method,
                    leaf_method,
                    shpaml.PASS_SYNTAX,
                    shpaml.FLUSH_LEFT_SYNTAX,
                    shpaml.FLUSH_LEFT_EMPTY_LINE,
                    shpaml.find_indentation,
                    )))

def test_branch_method(output, block, recurse):
    prefix, line = block[0]
    closer = prefix + '/' + line
    output.append(prefix + line)
    recurse(block[1:])
    output.append(closer)

def run_test(test_type, test):
    blocks = ['', '']
    i = 0
    for line in test:
        if line.startswith('---'):
            i = 1
        else:
            blocks[i] += line
    source, expected = blocks
    if 'shpaml' in test_type:
        assert_shpaml(expected, source)
    else:
        assert_indent(expected, source)

def run_suite(suite_fn):
    test = None
    for line in open(suite_fn):
        if line.startswith('==='):
            if test:
                run_test(test_type, test)
            test_type = line
            test = []
        else:
            test.append(line)
    run_test(test_type, test)


class ShpamlTests(TestCase):

    def setUp(self):
        pass
    
    
    def test_shpaml(self):
        run_suite(join(settings.PROJECT_ROOT, 'test.suite'))


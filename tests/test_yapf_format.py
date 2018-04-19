#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import unittest

try:
    import tests.testing as testing
    from tests.unittests_helper import CustomTestCase
except ImportError:
    import testing
    from unittests_helper import CustomTestCase

from yapf.yapflib.yapf_api import FormatCode


def _read_utf_8_file(filename):
    if sys.version_info.major == 2:  ## Python 2 specific
        with open(filename, 'rb') as f:
            return unicode(f.read(), 'utf-8')
    else:
        with open(filename, encoding='utf-8') as f:
            return f.read()


class YAPF_Style_Test(CustomTestCase):
    @classmethod
    def setUpClass(cls):

        cls.badly_formatted_files = list()
        cls.files_2_test = testing.list_all_py_files()

    def test_files_format(self):

        for file in testing.list_all_py_files():

            print(file)
            code = _read_utf_8_file(file)

            # https://pypi.python.org/pypi/yapf/0.20.2#example-as-a-module
            diff, changed = FormatCode(code, filename=file, style_config='.style.yapf', print_diff=True)

            if changed:
                print(diff)
                self.badly_formatted_files.append(file)

        with self.assertNotRaises(Exception):

            str_err = ""

            if self.badly_formatted_files:
                for filename in self.badly_formatted_files:
                    str_err += 'yapf -i %s\n' % filename

                str_err = "\n======================================================================================\n" \
                          "Bad Coding Style: %d file(s) need to be formatted, run the following commands to fix: \n%s" \
                          "======================================================================================" % (
                    len(self.badly_formatted_files), str_err)

                raise Exception(str_err)


if __name__ == '__main__':
    unittest.main()

# -*- coding: iso-8859-1 -*-
""" Test script for the Unicode implementation.

Written by Marc-Andre Lemburg (mal@lemburg.com).

(c) Copyright CNRI, All Rights Reserved. NO WARRANTY.

"""#"
import unittest, sys, string, codecs, new
from test import support, string_tests

class UnicodeTest(
    string_tests.CommonTest,
    string_tests.MixinStrUnicodeUserStringTest
    ):
    type2test = str

    def checkequalnofix(self, result, object, methodname, *args):
        method = getattr(object, methodname)
        realresult = method(*args)
        self.assertEqual(realresult, result)
        self.assertTrue(isinstance(realresult, type(result)))

        # if the original is returned make sure that
        # this doesn't happen with subclasses
        if realresult is object:
            class usub(str):
                def __repr__(self):
                    return 'usub(%r)' % str.__repr__(self)
            object = usub(object)
            method = getattr(object, methodname)
            realresult = method(*args)
            self.assertEqual(realresult, result)
            self.assertTrue(object is not realresult)

    def test_repr(self):
        if not sys.platform.startswith('java'):
            # Test basic sanity of repr()
            self.assertEqual(repr('abc'), "u'abc'")
            self.assertEqual(repr('ab\\c'), "u'ab\\\\c'")
            self.assertEqual(repr('ab\\'), "u'ab\\\\'")
            self.assertEqual(repr('\\c'), "u'\\\\c'")
            self.assertEqual(repr('\\'), "u'\\\\'")
            self.assertEqual(repr('\n'), "u'\\n'")
            self.assertEqual(repr('\r'), "u'\\r'")
            self.assertEqual(repr('\t'), "u'\\t'")
            self.assertEqual(repr('\b'), "u'\\x08'")
            self.assertEqual(repr("'\""), """u'\\'"'""")
            self.assertEqual(repr("'\""), """u'\\'"'""")
            self.assertEqual(repr("'"), '''u"'"''')
            self.assertEqual(repr('"'), """u'"'""")
            latin1repr = (
                "u'\\x00\\x01\\x02\\x03\\x04\\x05\\x06\\x07\\x08\\t\\n\\x0b\\x0c\\r"
                "\\x0e\\x0f\\x10\\x11\\x12\\x13\\x14\\x15\\x16\\x17\\x18\\x19\\x1a"
                "\\x1b\\x1c\\x1d\\x1e\\x1f !\"#$%&\\'()*+,-./0123456789:;<=>?@ABCDEFGHI"
                "JKLMNOPQRSTUVWXYZ[\\\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\\x7f"
                "\\x80\\x81\\x82\\x83\\x84\\x85\\x86\\x87\\x88\\x89\\x8a\\x8b\\x8c\\x8d"
                "\\x8e\\x8f\\x90\\x91\\x92\\x93\\x94\\x95\\x96\\x97\\x98\\x99\\x9a\\x9b"
                "\\x9c\\x9d\\x9e\\x9f\\xa0\\xa1\\xa2\\xa3\\xa4\\xa5\\xa6\\xa7\\xa8\\xa9"
                "\\xaa\\xab\\xac\\xad\\xae\\xaf\\xb0\\xb1\\xb2\\xb3\\xb4\\xb5\\xb6\\xb7"
                "\\xb8\\xb9\\xba\\xbb\\xbc\\xbd\\xbe\\xbf\\xc0\\xc1\\xc2\\xc3\\xc4\\xc5"
                "\\xc6\\xc7\\xc8\\xc9\\xca\\xcb\\xcc\\xcd\\xce\\xcf\\xd0\\xd1\\xd2\\xd3"
                "\\xd4\\xd5\\xd6\\xd7\\xd8\\xd9\\xda\\xdb\\xdc\\xdd\\xde\\xdf\\xe0\\xe1"
                "\\xe2\\xe3\\xe4\\xe5\\xe6\\xe7\\xe8\\xe9\\xea\\xeb\\xec\\xed\\xee\\xef"
                "\\xf0\\xf1\\xf2\\xf3\\xf4\\xf5\\xf6\\xf7\\xf8\\xf9\\xfa\\xfb\\xfc\\xfd"
                "\\xfe\\xff'")
            testrepr = repr(''.join(map(chr, range(256))))
            self.assertEqual(testrepr, latin1repr)

    def test_count(self):
        string_tests.CommonTest.test_count(self)
        # check mixed argument types
        self.checkequalnofix(3,  'aaa', 'count', 'a')
        self.checkequalnofix(0,  'aaa', 'count', 'b')
        self.checkequalnofix(3, 'aaa', 'count',  'a')
        self.checkequalnofix(0, 'aaa', 'count',  'b')
        self.checkequalnofix(0, 'aaa', 'count',  'b')
        self.checkequalnofix(1, 'aaa', 'count',  'a', -1)
        self.checkequalnofix(3, 'aaa', 'count',  'a', -10)
        self.checkequalnofix(2, 'aaa', 'count',  'a', 0, -1)
        self.checkequalnofix(0, 'aaa', 'count',  'a', 0, -10)

    def test_find(self):
        self.checkequalnofix(0,  'abcdefghiabc', 'find', 'abc')
        self.checkequalnofix(9,  'abcdefghiabc', 'find', 'abc', 1)
        self.checkequalnofix(-1, 'abcdefghiabc', 'find', 'def', 4)

        self.assertRaises(TypeError, 'hello'.find)
        self.assertRaises(TypeError, 'hello'.find, 42)

    def test_rfind(self):
        string_tests.CommonTest.test_rfind(self)
        # check mixed argument types
        self.checkequalnofix(9,   'abcdefghiabc', 'rfind', 'abc')
        self.checkequalnofix(12,  'abcdefghiabc', 'rfind', '')
        self.checkequalnofix(12, 'abcdefghiabc', 'rfind',  '')

    def test_index(self):
        string_tests.CommonTest.test_index(self)
        # check mixed argument types
        for (t1, t2) in ((str, str), (str, str)):
            self.checkequalnofix(0, t1('abcdefghiabc'), 'index',  t2(''))
            self.checkequalnofix(3, t1('abcdefghiabc'), 'index',  t2('def'))
            self.checkequalnofix(0, t1('abcdefghiabc'), 'index',  t2('abc'))
            self.checkequalnofix(9, t1('abcdefghiabc'), 'index',  t2('abc'), 1)
            self.assertRaises(ValueError, t1('abcdefghiabc').index, t2('hib'))
            self.assertRaises(ValueError, t1('abcdefghiab').index,  t2('abc'), 1)
            self.assertRaises(ValueError, t1('abcdefghi').index,  t2('ghi'), 8)
            self.assertRaises(ValueError, t1('abcdefghi').index,  t2('ghi'), -1)

    def test_rindex(self):
        string_tests.CommonTest.test_rindex(self)
        # check mixed argument types
        for (t1, t2) in ((str, str), (str, str)):
            self.checkequalnofix(12, t1('abcdefghiabc'), 'rindex',  t2(''))
            self.checkequalnofix(3,  t1('abcdefghiabc'), 'rindex',  t2('def'))
            self.checkequalnofix(9,  t1('abcdefghiabc'), 'rindex',  t2('abc'))
            self.checkequalnofix(0,  t1('abcdefghiabc'), 'rindex',  t2('abc'), 0, -1)

            self.assertRaises(ValueError, t1('abcdefghiabc').rindex,  t2('hib'))
            self.assertRaises(ValueError, t1('defghiabc').rindex,  t2('def'), 1)
            self.assertRaises(ValueError, t1('defghiabc').rindex,  t2('abc'), 0, -1)
            self.assertRaises(ValueError, t1('abcdefghi').rindex,  t2('ghi'), 0, 8)
            self.assertRaises(ValueError, t1('abcdefghi').rindex,  t2('ghi'), 0, -1)

    def test_translate(self):
        self.checkequalnofix('bbbc', 'abababc', 'translate', {ord('a'):None})
        self.checkequalnofix('iiic', 'abababc', 'translate', {ord('a'):None, ord('b'):ord('i')})
        self.checkequalnofix('iiix', 'abababc', 'translate', {ord('a'):None, ord('b'):ord('i'), ord('c'):'x'})
        self.checkequalnofix('<i><i><i>c', 'abababc', 'translate', {ord('a'):None, ord('b'):'<i>'})
        self.checkequalnofix('c', 'abababc', 'translate', {ord('a'):None, ord('b'):''})
        self.checkequalnofix('xyyx', 'xzx', 'translate', {ord('z'):'yy'})

        self.assertRaises(TypeError, 'hello'.translate)
        self.assertRaises(TypeError, 'abababc'.translate, {ord('a'):''})

    def test_split(self):
        string_tests.CommonTest.test_split(self)

        # Mixed arguments
        self.checkequalnofix(['a', 'b', 'c', 'd'], 'a//b//c//d', 'split', '//')
        self.checkequalnofix(['a', 'b', 'c', 'd'], 'a//b//c//d', 'split', '//')
        # 2.5 (and perhaps before) requires that the separator be a non-empty string
        # self.checkequalnofix([u'endcase ', u''], u'endcase test', 'split', 'test')

    def test_join(self):
        string_tests.MixinStrUnicodeUserStringTest.test_join(self)

        # mixed arguments
        self.checkequalnofix('a b c d', ' ', 'join', ['a', 'b', 'c', 'd'])
        self.checkequalnofix('abcd', '', 'join', ('a', 'b', 'c', 'd'))
        self.checkequalnofix('w x y z', ' ', 'join', string_tests.Sequence('wxyz'))
        self.checkequalnofix('a b c d', ' ', 'join', ['a', 'b', 'c', 'd'])
        self.checkequalnofix('a b c d', ' ', 'join', ['a', 'b', 'c', 'd'])
        self.checkequalnofix('abcd', '', 'join', ('a', 'b', 'c', 'd'))
        self.checkequalnofix('w x y z', ' ', 'join', string_tests.Sequence('wxyz'))

    def test_strip(self):
        string_tests.CommonTest.test_strip(self)
        self.assertRaises(UnicodeError, "hello".strip, "\xff")

    def test_replace(self):
        string_tests.CommonTest.test_replace(self)

        # method call forwarded from str implementation because of unicode argument
        self.checkequalnofix('one@two!three!', 'one!two!three!', 'replace', '!', '@', 1)
        self.assertRaises(TypeError, 'replace'.replace, "r", 42)

    def test_comparison(self):
        # Comparisons:
        self.assertEqual('abc', 'abc')
        self.assertEqual('abc', 'abc')
        self.assertEqual('abc', 'abc')
        self.assertTrue('abcd' > 'abc')
        self.assertTrue('abcd' > 'abc')
        self.assertTrue('abcd' > 'abc')
        self.assertTrue('abc' < 'abcd')
        self.assertTrue('abc' < 'abcd')
        self.assertTrue('abc' < 'abcd')

        if 0:
            # Move these tests to a Unicode collation module test...
            # Testing UTF-16 code point order comparisons...

            # No surrogates, no fixup required.
            self.assertTrue('\u0061' < '\u20ac')
            # Non surrogate below surrogate value, no fixup required
            #self.assert_(u'\u0061' < u'\ud800\udc02')

            # Non surrogate above surrogate value, fixup required
            def test_lecmp(s, s2):
                self.assertTrue(s < s2)

#             def test_fixup(s):
#                 s2 = u'\ud800\udc01'
#                 test_lecmp(s, s2)
#                 s2 = u'\ud900\udc01'
#                 test_lecmp(s, s2)
#                 s2 = u'\uda00\udc01'
#                 test_lecmp(s, s2)
#                 s2 = u'\udb00\udc01'
#                 test_lecmp(s, s2)
#                 s2 = u'\ud800\udd01'
#                 test_lecmp(s, s2)
#                 s2 = u'\ud900\udd01'
#                 test_lecmp(s, s2)
#                 s2 = u'\uda00\udd01'
#                 test_lecmp(s, s2)
#                 s2 = u'\udb00\udd01'
#                 test_lecmp(s, s2)
#                 s2 = u'\ud800\ude01'
#                 test_lecmp(s, s2)
#                 s2 = u'\ud900\ude01'
#                 test_lecmp(s, s2)
#                 s2 = u'\uda00\ude01'
#                 test_lecmp(s, s2)
#                 s2 = u'\udb00\ude01'
#                 test_lecmp(s, s2)
#                 s2 = u'\ud800\udfff'
#                 test_lecmp(s, s2)
#                 s2 = u'\ud900\udfff'
#                 test_lecmp(s, s2)
#                 s2 = u'\uda00\udfff'
#                 test_lecmp(s, s2)
#                 s2 = u'\udb00\udfff'
#                 test_lecmp(s, s2)

#                 test_fixup(u'\ue000')
#                 test_fixup(u'\uff61')

        # Surrogates on both sides, no fixup required
        # self.assert_(u'\ud800\udc02' < u'\ud84d\udc56')

    def test_islower(self):
        string_tests.MixinStrUnicodeUserStringTest.test_islower(self)
        self.checkequalnofix(False, '\u1FFc', 'islower')

    def test_isupper(self):
        string_tests.MixinStrUnicodeUserStringTest.test_isupper(self)
        if not sys.platform.startswith('java'):
            self.checkequalnofix(False, '\u1FFc', 'isupper')

    def test_istitle(self):
        string_tests.MixinStrUnicodeUserStringTest.test_title(self)
        self.checkequalnofix(True, '\u1FFc', 'istitle')
        self.checkequalnofix(True, 'Greek \u1FFcitlecases ...', 'istitle')

    def test_isspace(self):
        string_tests.MixinStrUnicodeUserStringTest.test_isspace(self)
        self.checkequalnofix(True, '\u2000', 'isspace')
        self.checkequalnofix(True, '\u200a', 'isspace')
        self.checkequalnofix(False, '\u2014', 'isspace')

    def test_isalpha(self):
        string_tests.MixinStrUnicodeUserStringTest.test_isalpha(self)
        self.checkequalnofix(True, '\u1FFc', 'isalpha')

    def test_isdecimal(self):
        self.checkequalnofix(False, '', 'isdecimal')
        self.checkequalnofix(False, 'a', 'isdecimal')
        self.checkequalnofix(True, '0', 'isdecimal')
        self.checkequalnofix(False, '\u2460', 'isdecimal') # CIRCLED DIGIT ONE
        self.checkequalnofix(False, '\xbc', 'isdecimal') # VULGAR FRACTION ONE QUARTER
        self.checkequalnofix(True, '\u0660', 'isdecimal') # ARABIC-INDIC DIGIT ZERO
        self.checkequalnofix(True, '0123456789', 'isdecimal')
        self.checkequalnofix(False, '0123456789a', 'isdecimal')

        self.checkraises(TypeError, 'abc', 'isdecimal', 42)

    def test_isdigit(self):
        string_tests.MixinStrUnicodeUserStringTest.test_isdigit(self)
        # JYTHON: U+2460 is CIRCLED DIGIT ONE; it's not a digit
        # self.checkequalnofix(True, u'\u2460', 'isdigit')
        self.checkequalnofix(False, '\xbc', 'isdigit')
        self.checkequalnofix(True, '\u0660', 'isdigit')

    def test_isnumeric(self):
        self.checkequalnofix(False, '', 'isnumeric')
        self.checkequalnofix(False, 'a', 'isnumeric')
        self.checkequalnofix(True, '0', 'isnumeric')
        self.checkequalnofix(True, '\u2460', 'isnumeric')
        self.checkequalnofix(True, '\xbc', 'isnumeric')
        self.checkequalnofix(True, '\u0660', 'isnumeric')
        self.checkequalnofix(True, '0123456789', 'isnumeric')
        self.checkequalnofix(False, '0123456789a', 'isnumeric')

        self.assertRaises(TypeError, "abc".isnumeric, 42)

    def test_contains(self):
        # Testing Unicode contains method
        self.assertTrue('a' in 'abdb')
        self.assertTrue('a' in 'bdab')
        self.assertTrue('a' in 'bdaba')
        self.assertTrue('a' in 'bdba')
        self.assertTrue('a' in 'bdba')
        self.assertTrue('a' in 'bdba')
        self.assertTrue('a' not in 'bdb')
        self.assertTrue('a' not in 'bdb')
        self.assertTrue('a' in 'bdba')
        self.assertTrue('a' in ('a', 1, None))
        self.assertTrue('a' in (1, None, 'a'))
        self.assertTrue('a' in (1, None, 'a'))
        self.assertTrue('a' in ('a', 1, None))
        self.assertTrue('a' in (1, None, 'a'))
        self.assertTrue('a' in (1, None, 'a'))
        self.assertTrue('a' not in ('x', 1, 'y'))
        self.assertTrue('a' not in ('x', 1, None))
        self.assertTrue('abcd' not in 'abcxxxx')
        self.assertTrue('ab' in 'abcd')
        self.assertTrue('ab' in 'abc')
        self.assertTrue('ab' in 'abc')
        self.assertTrue('ab' in (1, None, 'ab'))
        self.assertTrue('' in 'abc')
        self.assertTrue('' in 'abc')

        # If the following fails either
        # the contains operator does not propagate UnicodeErrors or
        # someone has changed the default encoding
        #self.assertRaises(UnicodeError, 'g\xe2teau'.__contains__, u'\xe2')

        self.assertTrue('' in '')
        self.assertTrue('' in '')
        self.assertTrue('' in '')
        self.assertTrue('' in 'abc')
        self.assertTrue('' in 'abc')
        self.assertTrue('' in 'abc')
        self.assertTrue('\0' not in 'abc')
        self.assertTrue('\0' not in 'abc')
        self.assertTrue('\0' not in 'abc')
        self.assertTrue('\0' in '\0abc')
        self.assertTrue('\0' in '\0abc')
        self.assertTrue('\0' in '\0abc')
        self.assertTrue('\0' in 'abc\0')
        self.assertTrue('\0' in 'abc\0')
        self.assertTrue('\0' in 'abc\0')
        self.assertTrue('a' in '\0abc')
        self.assertTrue('a' in '\0abc')
        self.assertTrue('a' in '\0abc')
        self.assertTrue('asdf' in 'asdf')
        self.assertTrue('asdf' in 'asdf')
        self.assertTrue('asdf' in 'asdf')
        self.assertTrue('asdf' not in 'asd')
        self.assertTrue('asdf' not in 'asd')
        self.assertTrue('asdf' not in 'asd')
        self.assertTrue('asdf' not in '')
        self.assertTrue('asdf' not in '')
        self.assertTrue('asdf' not in '')

        self.assertRaises(TypeError, "abc".__contains__)

    def test_formatting(self):
        string_tests.MixinStrUnicodeUserStringTest.test_formatting(self)
        # Testing Unicode formatting strings...
        self.assertEqual("%s, %s" % ("abc", "abc"), 'abc, abc')
        self.assertEqual("%s, %s, %i, %f, %5.2f" % ("abc", "abc", 1, 2, 3), 'abc, abc, 1, 2.000000,  3.00')
        self.assertEqual("%s, %s, %i, %f, %5.2f" % ("abc", "abc", 1, -2, 3), 'abc, abc, 1, -2.000000,  3.00')
        self.assertEqual("%s, %s, %i, %f, %5.2f" % ("abc", "abc", -1, -2, 3.5), 'abc, abc, -1, -2.000000,  3.50')
        self.assertEqual("%s, %s, %i, %f, %5.2f" % ("abc", "abc", -1, -2, 3.57), 'abc, abc, -1, -2.000000,  3.57')
        self.assertEqual("%s, %s, %i, %f, %5.2f" % ("abc", "abc", -1, -2, 1003.57), 'abc, abc, -1, -2.000000, 1003.57')
        self.assertEqual("%r, %r" % ("abc", "abc"), "u'abc', 'abc'")
        self.assertEqual("%(x)s, %(y)s" % {'x':"abc", 'y':"def"}, 'abc, def')
        self.assertEqual("%(x)s, %(\xfc)s" % {'x':"abc", '\xfc':"def"}, 'abc, def')

        self.assertEqual('%c' % 0x1234, '\u1234')
        self.assertRaises(OverflowError, "%c".__mod__, (sys.maxunicode+1,))

        # formatting jobs delegated from the string implementation:
        self.assertEqual('...%(foo)s...' % {'foo':"abc"}, '...abc...')
        self.assertEqual('...%(foo)s...' % {'foo':"abc"}, '...abc...')
        self.assertEqual('...%(foo)s...' % {'foo':"abc"}, '...abc...')
        self.assertEqual('...%(foo)s...' % {'foo':"abc"}, '...abc...')
        self.assertEqual('...%(foo)s...' % {'foo':"abc",'def':123},  '...abc...')
        self.assertEqual('...%(foo)s...' % {'foo':"abc",'def':123}, '...abc...')
        self.assertEqual('...%s...%s...%s...%s...' % (1, 2, 3, "abc"), '...1...2...3...abc...')
        self.assertEqual('...%%...%%s...%s...%s...%s...%s...' % (1, 2, 3, "abc"), '...%...%s...1...2...3...abc...')
        self.assertEqual('...%s...' % "abc", '...abc...')
        self.assertEqual('%*s' % (5, 'abc',), '  abc')
        self.assertEqual('%*s' % (-5, 'abc',), 'abc  ')
        self.assertEqual('%*.*s' % (5, 2, 'abc',), '   ab')
        self.assertEqual('%*.*s' % (5, 3, 'abc',), '  abc')
        self.assertEqual('%i %*.*s' % (10, 5, 3, 'abc',), '10   abc')
        self.assertEqual('%i%s %*.*s' % (10, 3, 5, 3, 'abc',), '103   abc')
        self.assertEqual('%c' % 'a', 'a')


    def test_constructor(self):
        # unicode(obj) tests (this maps to PyObject_Unicode() at C level)

        self.assertEqual(
            str('unicode remains unicode'),
            'unicode remains unicode'
        )

        class UnicodeSubclass(str):
            pass

        self.assertEqual(
            str(UnicodeSubclass('unicode subclass becomes unicode')),
            'unicode subclass becomes unicode'
        )

        self.assertEqual(
            str('strings are converted to unicode'),
            'strings are converted to unicode'
        )

        class UnicodeCompat:
            def __init__(self, x):
                self.x = x
            def __unicode__(self):
                return self.x

        self.assertEqual(
            str(UnicodeCompat('__unicode__ compatible objects are recognized')),
            '__unicode__ compatible objects are recognized')

        class StringCompat:
            def __init__(self, x):
                self.x = x
            def __str__(self):
                return self.x

        self.assertEqual(
            str(StringCompat('__str__ compatible objects are recognized')),
            '__str__ compatible objects are recognized'
        )

        # unicode(obj) is compatible to str():

        o = StringCompat('unicode(obj) is compatible to str()')
        self.assertEqual(str(o), 'unicode(obj) is compatible to str()')
        self.assertEqual(str(o), 'unicode(obj) is compatible to str()')

        for obj in (123, 123.45, 123):
            self.assertEqual(str(obj), str(str(obj)))

        # unicode(obj, encoding, error) tests (this maps to
        # PyUnicode_FromEncodedObject() at C level)

        if not sys.platform.startswith('java'):
            self.assertRaises(
                TypeError,
                str,
                'decoding unicode is not supported',
                'utf-8',
                'strict'
            )

        self.assertEqual(
            str('strings are decoded to unicode', 'utf-8', 'strict'),
            'strings are decoded to unicode'
        )

        self.assertEqual(
            str('strings are decoded to unicode', 'utf-8', 'strict'),
            'strings are decoded to unicode'
        )

        self.assertRaises(TypeError, str, 42, 42, 42)

    def test_codecs_utf7(self):
        utfTests = [
            ('A\u2262\u0391.', 'A+ImIDkQ.'),             # RFC2152 example
            ('Hi Mom -\u263a-!', 'Hi Mom -+Jjo--!'),     # RFC2152 example
            ('\u65E5\u672C\u8A9E', '+ZeVnLIqe-'),        # RFC2152 example
            ('Item 3 is \u00a31.', 'Item 3 is +AKM-1.'), # RFC2152 example
            ('+', '+-'),
            ('+-', '+--'),
            ('+?', '+-?'),
            ('\?', '+AFw?'),
            ('+?', '+-?'),
            (r'\\?', '+AFwAXA?'),
            (r'\\\?', '+AFwAXABc?'),
            (r'++--', '+-+---')
        ]

        for (x, y) in utfTests:
            self.assertEqual(x.encode('utf-7'), y)

        # Lone/misordered surrogates are an error
        self.assertRaises(UnicodeError, str, '+3ADYAA-', 'utf-7')

        # Jython (and some CPython versions): two misplaced surrogates => two replacements
        self.assertEqual(str('+3ADYAA-', 'utf-7', 'replace'), '\ufffd\ufffd')
        # self.assertEqual(unicode('+3ADYAA-', 'utf-7', 'replace'), u'\ufffd')

    def test_codecs_utf8(self):
        self.assertEqual(''.encode('utf-8'), '')
        self.assertEqual('\u20ac'.encode('utf-8'), '\xe2\x82\xac')
        # Jython will not compile Unicode literals with surrogate units
        #self.assertEqual(u'\ud800\udc02'.encode('utf-8'), '\xf0\x90\x80\x82')
        #self.assertEqual(u'\ud84d\udc56'.encode('utf-8'), '\xf0\xa3\x91\x96')
        #self.assertEqual(u'\ud800'.encode('utf-8'), '\xed\xa0\x80')
        #self.assertEqual(u'\udc00'.encode('utf-8'), '\xed\xb0\x80')
        #self.assertEqual(
        #    (u'\ud800\udc02'*1000).encode('utf-8'),
        #    '\xf0\x90\x80\x82'*1000
        #)
        self.assertEqual(
            '\u6b63\u78ba\u306b\u8a00\u3046\u3068\u7ffb\u8a33\u306f'
            '\u3055\u308c\u3066\u3044\u307e\u305b\u3093\u3002\u4e00'
            '\u90e8\u306f\u30c9\u30a4\u30c4\u8a9e\u3067\u3059\u304c'
            '\u3001\u3042\u3068\u306f\u3067\u305f\u3089\u3081\u3067'
            '\u3059\u3002\u5b9f\u969b\u306b\u306f\u300cWenn ist das'
            ' Nunstuck git und'.encode('utf-8'),
            '\xe6\xad\xa3\xe7\xa2\xba\xe3\x81\xab\xe8\xa8\x80\xe3\x81'
            '\x86\xe3\x81\xa8\xe7\xbf\xbb\xe8\xa8\xb3\xe3\x81\xaf\xe3'
            '\x81\x95\xe3\x82\x8c\xe3\x81\xa6\xe3\x81\x84\xe3\x81\xbe'
            '\xe3\x81\x9b\xe3\x82\x93\xe3\x80\x82\xe4\xb8\x80\xe9\x83'
            '\xa8\xe3\x81\xaf\xe3\x83\x89\xe3\x82\xa4\xe3\x83\x84\xe8'
            '\xaa\x9e\xe3\x81\xa7\xe3\x81\x99\xe3\x81\x8c\xe3\x80\x81'
            '\xe3\x81\x82\xe3\x81\xa8\xe3\x81\xaf\xe3\x81\xa7\xe3\x81'
            '\x9f\xe3\x82\x89\xe3\x82\x81\xe3\x81\xa7\xe3\x81\x99\xe3'
            '\x80\x82\xe5\xae\x9f\xe9\x9a\x9b\xe3\x81\xab\xe3\x81\xaf'
            '\xe3\x80\x8cWenn ist das Nunstuck git und'
        )

        # UTF-8 specific decoding tests
        self.assertEqual(str('\xf0\xa3\x91\x96', 'utf-8'), '\U00023456' )
        self.assertEqual(str('\xf0\x90\x80\x82', 'utf-8'), '\U00010002' )
        self.assertEqual(str('\xe2\x82\xac', 'utf-8'), '\u20ac' )

        # Other possible utf-8 test cases:
        # * strict decoding testing for all of the
        #   UTF8_ERROR cases in PyUnicode_DecodeUTF8

    def test_codecs_idna(self):
        # Test whether trailing dot is preserved
        self.assertEqual("www.python.org.".encode("idna"), "www.python.org.")

    def test_codecs_errors(self):
        # Error handling (encoding)
        self.assertRaises(UnicodeError, 'Andr\202 x'.encode, 'ascii')
        self.assertRaises(UnicodeError, 'Andr\202 x'.encode, 'ascii', 'strict')
        self.assertEqual('Andr\202 x'.encode('ascii', 'ignore'), "Andr x")
        self.assertEqual('Andr\202 x'.encode('ascii', 'replace'), "Andr? x")

        # Error handling (decoding)
        self.assertRaises(UnicodeError, str, 'Andr\202 x', 'ascii')
        self.assertRaises(UnicodeError, str, 'Andr\202 x', 'ascii', 'strict')
        self.assertEqual(str('Andr\202 x', 'ascii', 'ignore'), "Andr x")
        self.assertEqual(str('Andr\202 x', 'ascii', 'replace'), 'Andr\uFFFD x')

        # Error handling (unknown character names)
        self.assertEqual("\\N{foo}xx".decode("unicode-escape", "ignore"), "xx")

        # Error handling (truncated escape sequence)
        self.assertRaises(UnicodeError, "\\".decode, "unicode-escape")

        # Error handling (bad decoder return)
        def search_function(encoding):
            def decode1(input, errors="strict"):
                return 42 # not a tuple
            def encode1(input, errors="strict"):
                return 42 # not a tuple
            def encode2(input, errors="strict"):
                return (42, 42) # no unicode
            def decode2(input, errors="strict"):
                return (42, 42) # no unicode
            if encoding=="test.unicode1":
                return (encode1, decode1, None, None)
            elif encoding=="test.unicode2":
                return (encode2, decode2, None, None)
            else:
                return None
        codecs.register(search_function)
        self.assertRaises(TypeError, "hello".decode, "test.unicode1")
        self.assertRaises(TypeError, str, "hello", "test.unicode2")
        self.assertRaises(TypeError, "hello".encode, "test.unicode1")
        self.assertRaises(TypeError, "hello".encode, "test.unicode2")
        # executes PyUnicode_Encode()
        import imp
        self.assertRaises(
            ImportError,
            imp.find_module,
            "non-existing module",
            ["non-existing dir"]
        )

        # Error handling (wrong arguments)
        self.assertRaises(TypeError, "hello".encode, 42, 42, 42)

        # Error handling (PyUnicode_EncodeDecimal())
        self.assertRaises(UnicodeError, int, "\u0200")

    def test_codecs(self):
        # Encoding
        self.assertEqual('hello'.encode('ascii'), 'hello')
        self.assertEqual('hello'.encode('utf-7'), 'hello')
        self.assertEqual('hello'.encode('utf-8'), 'hello')
        self.assertEqual('hello'.encode('utf8'), 'hello')
        self.assertEqual('hello'.encode('utf-16-le'), 'h\000e\000l\000l\000o\000')
        self.assertEqual('hello'.encode('utf-16-be'), '\000h\000e\000l\000l\000o')
        self.assertEqual('hello'.encode('latin-1'), 'hello')

        # Roundtrip safety for BMP (just the first 1024 chars)
        u = ''.join(map(chr, range(1024)))
        for encoding in ('utf-7', 'utf-8', 'utf-16', 'utf-16-le', 'utf-16-be',
                         'raw_unicode_escape', 'unicode_escape', 'unicode_internal'):
            self.assertEqual(str(u.encode(encoding), encoding), u)

        # Roundtrip safety for BMP (just the first 256 chars)
        u = ''.join(map(chr, range(256)))
        for encoding in ('latin-1',):
            self.assertEqual(str(u.encode(encoding), encoding), u)

        # Roundtrip safety for BMP (just the first 128 chars)
        u = ''.join(map(chr, range(128)))
        for encoding in ('ascii',):
            self.assertEqual(str(u.encode(encoding), encoding), u)

        # Roundtrip safety for non-BMP (just a few chars)
        u = '\U00010001\U00020002\U00030003\U00040004\U00050005'
        for encoding in ('utf-8', 'utf-16', 'utf-16-le', 'utf-16-be',
                         #'raw_unicode_escape',
                         'unicode_escape', 'unicode_internal'):
            self.assertEqual(str(u.encode(encoding), encoding), u)

        # UTF-8 must be roundtrip safe for all UCS-2 code points
        # This excludes surrogates: in the full range, there would be
        # a surrogate pair (\udbff\udc00), which gets converted back
        # to a non-BMP character (\U0010fc00)
        u = ''.join(map(chr, list(range(0, 0xd800))+list(range(0xe000, 0x10000))))
        for encoding in ('utf-8',):
            self.assertEqual(str(u.encode(encoding), encoding), u)

    def test_codecs_charmap(self):
        # 0-127
        s = ''.join(map(chr, range(128)))
        for encoding in (
            'cp037', 'cp1026',
            'cp437', 'cp500', 'cp737', 'cp775', 'cp850',
            'cp852', 'cp855', 'cp860', 'cp861', 'cp862',
            'cp863', 'cp865', 'cp866',
            'iso8859_10', 'iso8859_13', 'iso8859_14', 'iso8859_15',
            'iso8859_2', 'iso8859_3', 'iso8859_4', 'iso8859_5', 'iso8859_6',
            'iso8859_7', 'iso8859_9', 'koi8_r', 'latin_1',
            'mac_cyrillic', 'mac_latin2',

            'cp1250', 'cp1251', 'cp1252', 'cp1253', 'cp1254', 'cp1255',
            'cp1256', 'cp1257', 'cp1258',
            'cp856', 'cp857', 'cp864', 'cp869', 'cp874',

            'mac_greek', 'mac_iceland', 'mac_roman', 'mac_turkish',
            'cp1006', 'iso8859_8',

            ### These have undefined mappings:
            #'cp424',

            ### These fail the round-trip:
            #'cp875'

            ):
            self.assertEqual(str(s, encoding).encode(encoding), s)

        # 128-255
        s = ''.join(map(chr, range(128, 256)))
        for encoding in (
            'cp037', 'cp1026',
            'cp437', 'cp500', 'cp737', 'cp775', 'cp850',
            'cp852', 'cp855', 'cp860', 'cp861', 'cp862',
            'cp863', 'cp865', 'cp866',
            'iso8859_10', 'iso8859_13', 'iso8859_14', 'iso8859_15',
            'iso8859_2', 'iso8859_4', 'iso8859_5',
            'iso8859_9', 'koi8_r', 'latin_1',
            'mac_cyrillic', 'mac_latin2',

            ### These have undefined mappings:
            #'cp1250', 'cp1251', 'cp1252', 'cp1253', 'cp1254', 'cp1255',
            #'cp1256', 'cp1257', 'cp1258',
            #'cp424', 'cp856', 'cp857', 'cp864', 'cp869', 'cp874',
            #'iso8859_3', 'iso8859_6', 'iso8859_7',
            #'mac_greek', 'mac_iceland','mac_roman', 'mac_turkish',

            ### These fail the round-trip:
            #'cp1006', 'cp875', 'iso8859_8',

            ):
            self.assertEqual(str(s, encoding).encode(encoding), s)

    def test_concatenation(self):
        self.assertEqual(("abc" "def"), "abcdef")
        self.assertEqual(("abc" "def"), "abcdef")
        self.assertEqual(("abc" "def"), "abcdef")
        self.assertEqual(("abc" "def" "ghi"), "abcdefghi")
        self.assertEqual(("abc" "def" "ghi"), "abcdefghi")

    def test_printing(self):
        class BitBucket:
            def write(self, text):
                pass

        out = BitBucket()
        print('abc', file=out)
        print('abc', 'def', file=out)
        print('abc', 'def', file=out)
        print('abc', 'def', file=out)
        print('abc\n', file=out)
        print('abc\n', end=' ', file=out)
        print('abc\n', end=' ', file=out)
        print('def\n', file=out)
        print('def\n', file=out)

    def test_ucs4(self):
        if sys.maxunicode == 0xFFFF:
            return
        x = '\U00100000'
        y = x.encode("raw-unicode-escape").decode("raw-unicode-escape")
        self.assertEqual(x, y)

def test_main():
    support.run_unittest(UnicodeTest)

if __name__ == "__main__":
    test_main()

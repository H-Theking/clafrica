import unittest
from src.inputmethod import ClafricaKeyboard
from src.keyboardthread import input_method
# import re


class MyTestCase(unittest.TestCase):
    #
    # def setUp(self):
    #     self.concur = ClafricaKeyboard()
    #     self.concur.run()
    #
    # def tearDown(self):
    #     self.concur.pause()
    #     del self.concur
    #
    # def test_stop_listener(self):
    #     self.concur.pause()
    #     self.assertFalse(self.concur.running)

    def setUp(self):
        self.kbthread = input_method
        self.cKeyboard = ClafricaKeyboard()
        self.kbthread.start()

    def tearDown(self):
        self.kbthread.pause()
        del self.kbthread, self.cKeyboard

    def test_exact_code(self):
        code = 'a94'
        expected = 'a̤̍'
        print(self.kbthread.listener.type(code))
        # self.assertTrue(True, True)
        # self.assertEqual(self.kbthread., expected)
    #
    # def setUp(self):
    #     self.concur = Concur()
    #     self.cKeyboard = ClafricaKeyboard()
    #     self.concur.run()

    # def tearDown(self):
    #     self.concur.pause()
    #     del self.concur, self.cKeyboard
    #
    # def test_code_with_extra_character(self):
    #     code = 'a9e'
    #     expected = 'a̤̍', 'e'
    #     self.assertEqual(self.concur.code_with_extra(code), expected)

    # def test_no_code_with_last_valid(self):
    #     """
    #     This test will has no bearing on the old mungaka alphabet
    #     as all there is no scenario such scenario
    #     :return: None
    #     """
    #     code = 'affa'
    #     expected = None, 'a'
    #     self.assertEqual(self.concur.invalid_code_with_valid_last(code), expected)

    # def test_all_codes(self):
    #     self.concur.run()
    #     codes_list_returned = map(self.cKeyboard.find_character, self.cKeyboard.codes.keys())
    #     print(codes_list_returned)
        # self.assertEqual(self.cKeyboard.codes.values(), self.concur.listener.type("".join(codes_list_returned)))


if __name__ == '__main__':
    unittest.main()

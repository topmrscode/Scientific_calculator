import unittest
import operator
import string
import numbers
import math
import computer


class TestStringMethods(unittest.TestCase):
    computer = computer.Computer()

    def test_converter(self):
        self.assertEqual(self.computer._converter("F", 16), 15, "Converter didn't worked with Hexa base")
        self.assertEqual(self.computer._converter("FFE123", 16), 16769315, "Converter didn't worked with Hexa base")
        self.assertEqual(self.computer._converter("113", 8), 75, "Converter didn't worked with oct base")
        self.assertEqual(self.computer._converter("123123.42", 8), 42579.53125, "Converter didn't worked with oct base")
        self.assertEqual(self.computer._converter("110111011", 2), 443, "Converter didn't worked with bin base")
        self.assertEqual(self.computer._converter("1111.00110", 2), 15.1875, "Converter didn't worked with bin base")

    def _utils_list_from_generator(self, gen):
        myList = []
        for g in gen:
            myList.append(g)
        return myList

    def test_separate(self):
        self.assertEqual(self._utils_list_from_generator(self.computer._separate("123+123")), [123, "+", 123], "Simple formula not split correctly")
        self.assertEqual(self._utils_list_from_generator(self.computer._separate("123+123/10*cos(2)")), [123, "+", 123, "/", 10, "*", "cos", "(", 2, ")"], "Complex formula not split correctly")
        with self.assertRaises(ValueError):
            self._utils_list_from_generator(self.computer._separate("123.12.12+123"))

    def test_check_braces(self):
        self.assertTrue(self.computer._check_braces(["(", 10, "+", 10, ")"]), "Simple formula with braces working")
        self.assertTrue(self.computer._check_braces(["(", "(", 10, ")", "+", 10, ")", "+", "(", 3, "+", 3, ")"]), "More complex formula with braces working")
        self.assertFalse(self.computer._check_braces(["(", "(", 10, "+", 10, ")"]), "Too many right braces")
        self.assertFalse(self.computer._check_braces([")", 10, "+", 10, ")"]), "Starting with left brace")
        self.assertFalse(self.computer._check_braces(["(", 10, "+", 10]), "Missing left brace")

    def test_check_tokens(self):
        self.assertTrue(self.computer._check_tokens([123, "+", 123]), "Tokens verification : simple formula")
        self.assertFalse(self.computer._check_tokens([123, "+", "+", "+", 123]), "Tokens verification : multiple operators chained")
        self.assertFalse(self.computer._check_tokens([123, "+"]), "Tokens verification : finishing with operator")
        self.assertFalse(self.computer._check_tokens([123, "+", "test", 123]), "Tokens verification : simple formula")

    def test_find_digits(self):
        found, expr = self.computer._find_digits("123+4")
        self.assertEqual(found, 123)
        self.assertEqual(expr, "+4")

        found, expr = self.computer._find_digits("123.12+4/45*cos(2)")
        self.assertAlmostEqual(found, 123.12)
        self.assertEqual(expr, "+4/45*cos(2)")

        with self.assertRaises(ValueError):
            found, expr = self.computer._find_digits("123.12.15+4")

        found, expr = self.computer._find_digits("-123+4")
        self.assertEqual(found, -123)
        self.assertEqual(expr, "+4")
    
    def test_shunting_yard(self):
        npi, err = self.computer._shunting_yard("123+4")
        self.assertEqual(err, "")
        self.assertEqual(npi, [123, 4, "+"])

        npi, err = self.computer._shunting_yard("123+4/2*cos(1)")
        self.assertEqual(err, "")
        self.assertEqual(npi, [123, 4, 2, "/", 1, "cos", "*", "+"])

        npi, err = self.computer._shunting_yard("123.12.12+4/2*cos(1)")
        self.assertEqual(err, "Too many dots")
        self.assertEqual(npi, None)

        npi, err = self.computer._shunting_yard("(123+4)/2*cos(1)")
        self.assertEqual(err, "")
        self.assertEqual(npi, [123, 4, '+', 2, '/', 1, 'cos', '*'])

        npi, err = self.computer._shunting_yard("(123+4/2*cos(1)")
        self.assertEqual(err, "Mismatched braces")
        self.assertEqual(npi, None)

        npi, err = self.computer._shunting_yard("(123+4/2*cos(1)")
        self.assertEqual(err, "Mismatched braces")
        self.assertEqual(npi, None)

        npi, err = self.computer._shunting_yard("123 +")
        self.assertEqual(err, "Malformated formula")
        self.assertEqual(npi, None)

    def test_calculate(self):
        res, err = self.computer._calculate([2, 2, "+"])
        self.assertEqual(err, "")
        self.assertEqual(res, 4)

        res, err = self.computer._calculate([2, 2, "*", 3, "+"])
        self.assertEqual(err, "")
        self.assertEqual(res, 7)

        res, err = self.computer._calculate(["exp"])
        self.assertEqual(err, "Malformated Formula")
        self.assertEqual(res, None)

        res, err = self.computer._calculate(["cos"])
        self.assertEqual(err, "Malformated Formula")
        self.assertEqual(res, None)

        res, err = self.computer._calculate(["sin"])
        self.assertEqual(err, "Malformated Formula")
        self.assertEqual(res, None)

        res, err = self.computer._calculate(["tan"])
        self.assertEqual(err, "Malformated Formula")
        self.assertEqual(res, None)

        res, err = self.computer._calculate(["log"])
        self.assertEqual(err, "Malformated Formula")
        self.assertEqual(res, None)

        res, err = self.computer._calculate(["hex"])
        self.assertEqual(err, "Malformated Formula")
        self.assertEqual(res, None)

        res, err = self.computer._calculate(["oct"])
        self.assertEqual(err, "Malformated Formula")
        self.assertEqual(res, None)

        res, err = self.computer._calculate(["bin"])
        self.assertEqual(err, "Malformated Formula")
        self.assertEqual(res, None)

        res, err = self.computer._calculate([2, "+"])
        self.assertEqual(err, "Malformated Formula")
        self.assertEqual(res, None)

        res, err = self.computer._calculate([2, "+"])
        self.assertEqual(err, "Malformated Formula")
        self.assertEqual(res, None)

        res, err = self.computer._calculate([2, 3, "+", "-"])
        self.assertEqual(err, "Malformated Formula")
        self.assertEqual(res, None)



if __name__ == '__main__':
    unittest.main()
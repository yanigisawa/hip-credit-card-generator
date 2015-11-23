import creditCardGenerator
import unittest
import json
import entities

class TestCreditCardGenerator(unittest.TestCase):
    def setUp(self):
        self.ccgen = creditCardGenerator.CreditCardGenerator()

    def test_will_generate_number_with_appropriate_length(self):
        selectedType = self.ccgen.get_credit_card_type("American Express")
        self.assertEquals(selectedType[2], len(self.ccgen.get_random_number(selectedType)))

    def test_random_number_satisfies_checksum(self):
        st = self.ccgen.get_credit_card_type("Discover Card")
        number = self.ccgen.get_random_number(st)
        digits = [int(c) for c in number]
        count = 0
        sum_digits = []
        digits.reverse()
        for d in digits[1:]:
            if count % 2 == 0:
                product = d * 2
                if product > 9:
                    s = sum([int(c) for c in str(product)])
                    sum_digits.append(s)
                else:
                    sum_digits.append(product)
            else:
                sum_digits.append(int(d))
            count += 1

        su = sum(sum_digits) * 9
        checkDigit = [c for c in str(su)][-1]
        self.assertEquals(checkDigit, number[-1])

def main():
    unittest.main()

if __name__ == '__main__':
    main()        

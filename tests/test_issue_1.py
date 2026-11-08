"""Regression test for issue #1:
apply_promo should accept promo codes regardless of case and surrounding whitespace.
"""
import unittest
from shop.cart import Cart


class PromoNormalizationTests(unittest.TestCase):

    def test_lowercase_promo(self):
        """'save10' should be accepted the same as 'SAVE10'."""
        c = Cart()
        c.apply_promo('save10')
        self.assertEqual(c.promo, 'SAVE10')

    def test_mixed_case_promo(self):
        """'Save10' should be accepted the same as 'SAVE10'."""
        c = Cart()
        c.apply_promo('Save10')
        self.assertEqual(c.promo, 'SAVE10')

    def test_promo_with_leading_whitespace(self):
        """' SAVE10' (leading space, e.g. copied from email) should be accepted."""
        c = Cart()
        c.apply_promo(' SAVE10')
        self.assertEqual(c.promo, 'SAVE10')

    def test_promo_with_trailing_whitespace(self):
        """'SAVE10 ' (trailing space, e.g. copied from email) should be accepted."""
        c = Cart()
        c.apply_promo('SAVE10 ')
        self.assertEqual(c.promo, 'SAVE10')

    def test_promo_lowercase_with_whitespace(self):
        """' save10 ' should be accepted the same as 'SAVE10'."""
        c = Cart()
        c.apply_promo(' save10 ')
        self.assertEqual(c.promo, 'SAVE10')

    def test_discount_applied_after_lowercase_promo(self):
        """Discount must actually be applied when promo was entered in lowercase."""
        c = Cart()
        c.add('k1')          # 249 000 kopecks
        c.apply_promo('save10')
        self.assertEqual(c.goods_total(), 224100)   # 249000 * 0.90

    def test_invalid_promo_still_raises(self):
        """Normalization must not swallow genuinely invalid codes."""
        with self.assertRaises(ValueError):
            Cart().apply_promo('UNKNOWN')

    def test_invalid_promo_lowercase_still_raises(self):
        """A lowercased invalid code must still raise ValueError."""
        with self.assertRaises(ValueError):
            Cart().apply_promo('unknown')


if __name__ == '__main__':
    unittest.main()

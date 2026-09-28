import unittest

from duckfine import DuckFine


class TestDuckFine(unittest.TestCase):
    def setUp(self):
        self.fine = DuckFine("member-123")

    def test_stores_member_id(self):
        self.assertEqual(self.fine.member_id, "member-123")

    def test_initial_total_owed_is_zero(self):
        self.assertEqual(self.fine.total_owed, 0.0)

    def test_charge_returns_zero_when_returned_on_time(self):
        self.assertEqual(self.fine.charge(0), 0.0)

    def test_charge_returns_zero_on_last_grace_day(self):
        self.assertEqual(self.fine.charge(2), 0.0)

    def test_charge_applies_daily_fee_after_grace_period(self):
        self.assertEqual(self.fine.charge(3), 0.50)

    def test_deluxe_charge_is_double_the_standard_fee(self):
        self.assertEqual(self.fine.charge(3, deluxe=True), 1.00)

    def test_standard_charge_does_not_exceed_maximum_fee(self):
        self.assertEqual(self.fine.charge(20), 5.00)

    def test_deluxe_charge_does_not_exceed_maximum_fee(self):
        self.assertEqual(self.fine.charge(20, deluxe=True), 5.00)

    def test_charge_adds_fee_to_total_owed(self):
        self.fine.charge(4)

        self.assertEqual(self.fine.total_owed, 1.00)

    def test_repeated_charges_accumulate_in_total_owed(self):
        self.fine.charge(3)
        self.fine.charge(4)

        self.assertEqual(self.fine.total_owed, 1.50)

    def test_negative_days_late_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.fine.charge(-1)

    def test_rejected_charge_does_not_change_total_owed(self):
        try:
            self.fine.charge(-1)
        except ValueError:
            pass

        self.assertEqual(self.fine.total_owed, 0.0)


if __name__ == "__main__":
    unittest.main()

import unittest
import time
from sainsmart_relay.relay import FTDIBitbangRelay

class TestRelayCombinations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize the relay board
        cls.relay_board = FTDIBitbangRelay(verbosity=2)  # Adjust verbosity as needed

    @classmethod
    def tearDownClass(cls):
        # Clean up and close the relay board connection
        cls.relay_board.close()

    def set_relay_pattern(self, pattern):
        # Set relays according to the bit pattern
        for i in range(4):
            state = 'on' if (pattern & (1 << i)) else 'off'
            self.relay_board.set_relay(i + 1, state)
            time.sleep(0.1)  # Pause between commands

        # Read back and verify the pattern
        current_state = self.relay_board.local_state
        self.assertEqual(current_state, pattern, f"Failed to set pattern {pattern:04b}")

    def test_relay_combinations(self):
        for pattern in range(16):  # 16 combinations from 0000 to 1111
            with self.subTest(pattern=pattern):
                self.set_relay_pattern(pattern)
                time.sleep(1)  # Pause before the next pattern

# Run the tests
if __name__ == '__main__':
    unittest.main()

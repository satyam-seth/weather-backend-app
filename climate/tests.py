from django.test import TestCase

# Create your tests here.


class DummyTestCase(TestCase):
    """Dummy Test Case"""

    def test_dummy(self):
        """A dummy test that always passes"""

        self.assertEqual(1 + 1, 2)

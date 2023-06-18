from unittest import TestCase

from pycommons.base.function import Supplier


class TestSupplier(TestCase):
    def test_supplier_with_lambda(self):
        supplier = Supplier.of(lambda: 4**2)
        self.assertEqual(16, supplier())
        self.assertEqual(16, supplier.get())
        self.assertTrue("BasicSupplier" in str(type(supplier)))

    def test_supplier_with_functional_interface(self):
        class PowerSupplier(Supplier[int]):
            def get(self) -> int:
                return 4**2

        supplier = Supplier.of(PowerSupplier())
        self.assertEqual(16, supplier())
        self.assertEqual(16, supplier.get())
        self.assertFalse("BasicSupplier" in str(type(supplier)))

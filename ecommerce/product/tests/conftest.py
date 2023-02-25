import pytest
from pytest_factoryboy import register
from product.tests.factory import (
    ProductFactory,
    ProductArributeFactory,
    ProductVariantFactory,
)

register(ProductFactory)
register(ProductArributeFactory)
register(ProductVariantFactory)


@pytest.fixture
def multi_variant_product():
    obj = ProductVariantFactory.create(
        attribute=[ProductArributeFactory() for i in range(5)]
    )
    return obj.product

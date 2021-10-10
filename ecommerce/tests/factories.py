import factory
import pytest
from faker import Faker
from pytest_factoryboy import register

fake = Faker()

from ecommerce.inventory import models


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Category

    name = fake.lexify(text="cat_name_??????")
    slug = fake.lexify(text="cat_slug_??????")


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Product

    web_id = fake.lexify(text="prod_web_id_??????")
    slug = fake.lexify(text="prod_slug_??????")
    name = fake.lexify(text="prod_name_??????")
    description = fake.text()
    is_active = True
    created_at = "2021-09-04 22:14:18.279092"
    updated_at = "2021-09-04 22:14:18.279092"

    @factory.post_generation
    def category(self, create, extracted, **kwargs):
        if not create or not extracted:
            # Simple build, or nothing to add, do nothing.
            return

        if extracted:
            # A list of categories were passed in, use them
            for cat in extracted:
                self.category.add(cat)


class ProductTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ProductType

    name = fake.lexify(text="type??????")


class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Brand

    name = fake.lexify(text="brand??????")


class ProductInventoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ProductInventory

    sku = fake.lexify(text="sku_??????????")
    upc = fake.lexify(text="upc_??????????")
    product_type = factory.SubFactory(ProductTypeFactory)
    product = factory.SubFactory(ProductFactory)
    brand = factory.SubFactory(BrandFactory)
    is_active = 1
    retail_price = 97
    store_price = 92
    sale_price = 46
    weight = 987


class StockFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Stock

    product_inventory = factory.SubFactory(ProductInventoryFactory)
    last_checked = "2021-09-04 22:14:18.279095"
    units = 2
    units_sold = 0


class MediaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Media

    product_inventory = factory.SubFactory(ProductInventoryFactory)
    image = "images/default.png"
    alt_text = "a default image solid color"
    is_feature = True
    created_at = "2021-09-04 22 :14:18.279095"
    updated_at = "2021-09-04 22:14:18.279095"


class ProductAttributeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ProductAttribute

    name = factory.Sequence(lambda n: "attribute_name_%d" % n)
    description = factory.Sequence(lambda n: "description_%d" % n)


class ProductAttributeValueFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ProductAttributeValue

    product_attribute = factory.SubFactory(ProductAttributeFactory)
    attribute_value = fake.lexify(text="attribute_value_??????")


class ProductAttributeValuesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ProductAttributeValues

    attributevalues = factory.SubFactory(ProductAttributeValueFactory)
    productinventory = factory.SubFactory(ProductInventoryFactory)


class ProductWithAttributeValuesFactory(ProductInventoryFactory):
    attributevalues1 = factory.RelatedFactory(
        ProductAttributeValuesFactory,
        factory_related_name="productinventory",
    )
    attributevalues2 = factory.RelatedFactory(
        ProductAttributeValuesFactory,
        factory_related_name="productinventory",
    )


register(CategoryFactory)
register(ProductFactory)
register(ProductTypeFactory)
register(BrandFactory)
register(ProductInventoryFactory)
register(StockFactory)
register(MediaFactory)
register(ProductAttributeFactory)
register(ProductAttributeValueFactory)
register(ProductAttributeValuesFactory)
register(ProductWithAttributeValuesFactory)

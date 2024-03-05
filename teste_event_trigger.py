from core.models import Product, Store

Store.objects.all().delete()
Product.objects.all().delete()

store = Store.objects.create(
    name="Amazon",
    document="123456789"
)
product = Product.objects.create(
    name="Vivobook",
    price=20,
    description="Notebook",
    sku="SKU001",
    store=store
)

product = Product.objects.get(name="Vivobook")
product.price = 30
product.save()

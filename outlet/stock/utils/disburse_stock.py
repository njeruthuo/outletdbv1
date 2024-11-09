from django.db import transaction
from django.core.exceptions import ValidationError

from outlet.shop.models import ShopStock
from outlet.stock.models import Stock, StockDisbursement


@transaction.atomic
def disburse_stock(shop, product, disburse_quantity, disbursed_by=None):
    try:
        # Fetch the central stock for the product
        central_stock = Stock.objects.get(product=product)
        if central_stock.quantity < disburse_quantity:
            raise ValidationError(
                "Not enough stock available for disbursement.")

        # Deduct from central stock
        central_stock.quantity -= disburse_quantity
        central_stock.save()

        # Fetch or create ShopStock for the specific product in the shop
        shop_stock, created = ShopStock.objects.get_or_create(
            shop=shop, product=product)

        # Increase the shop's stock quantity
        shop_stock.quantity += disburse_quantity
        shop_stock.save()

        # Log the disbursement in StockDisbursement
        StockDisbursement.objects.create(
            shop=shop,
            product=product,
            disburse_quantity=disburse_quantity,
            disbursed_by=disbursed_by
        )

        return f"Successfully disbursed {disburse_quantity} units of {product.name} to {shop.branch_name}."
    except Stock.DoesNotExist:
        raise ValidationError("Product does not exist in central stock.")
    except Exception as e:
        raise ValidationError(f"Error during stock disbursement: {str(e)}")

from django.db import transaction
from django.core.exceptions import ValidationError

from stock.models import Stock
from shop.models import StockDisbursementStatuses
from shop.models import ShopStock, StockDisbursement


@transaction.atomic
def disburse_stock(shop=None, product=None, disburse_quantity=None, disbursed_by=None):
    try:

        # Fetch the central stock for the product
        central_stock = Stock.objects.select_for_update().filter(product=product).first()
        if not central_stock:
            raise ValidationError("Product does not exist in central stock.")

        # print(f"Central stock before disbursement: {central_stock.quantity}")

        # Validate stock levels
        if central_stock.quantity < disburse_quantity:
            raise ValidationError(
                "Not enough stock available for disbursement.")

        # Deduct from central stock
        central_stock.quantity -= disburse_quantity
        central_stock.save()
        # print(f"Central stock after disbursement: {central_stock.quantity}")

        # Fetch or create ShopStock for the product in the shop
        shop_stock, created = ShopStock.objects.get_or_create(
            shop=shop, product=product)
        # print(f"Shop stock before disbursement: {shop_stock.quantity}")

        # Increase shop stock
        shop_stock.quantity += disburse_quantity
        shop_stock.save()
        # print(f"Shop stock after disbursement: {shop_stock.quantity}")

        # Log the disbursement
        dsb = StockDisbursement.objects.create(
            shop=shop,
            product=product,
            disburse_quantity=disburse_quantity,
            disbursed_by=disbursed_by,
            status=StockDisbursementStatuses.DISBURSED
        )
        # print(f"StockDisbursement: {dsb}")

        return f"Successfully disbursed {disburse_quantity} units of {product.name} to {shop.branch_name}."
    except ValidationError as ve:
        print(f"Validation Error: {ve}")
        raise
    except Exception as e:
        print(f"Unexpected Error: {e}")
        raise ValidationError(f"Error during stock disbursement: {str(e)}")

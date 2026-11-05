Price To Weight

There are three types of barcode rules for product

-> 'Unit Product’ (type=’product’). Scanning a product will add a unit of this product to the current order.
-> ‘Priced product’ (type=’price’). A price is extracted from the barcode, and a new line with the given price and a quantity = 1 is added to the current order.
->‘Weighted product’ (type=’weight). A weight is extracted from the barcode, and a new line with the given weight, and a computed price (quantity * Unit price) is added to the current order.

This Module Add a New Feature: 

-> ‘Priced Product (Computed Weight)’ (type=’price_to_weight’). A price is extracted from the barcode, and a new line with the given price, and a computed quantity (Price / Unit Price) is added to the current order.


Configuration

=> Go to Point of Sale > Configuration > Barcode Nomenclatures
=> Edit your barcode rules, according to your barcodes settings
=> Go to Point of Sale > Configuration > Point of Sale
=> Select the ‘Unit Price’ field that will be used to convert the price to weight.

from odoo import fields,models

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    def get_product_info_pos(self, price, quantity, pos_config_id, product_variant_id=False):
        result = super().get_product_info_pos(price, quantity, pos_config_id, product_variant_id=False)
        warehouse_location_list = []
        warehouse_id_list = []
    
        for w in self.env['stock.warehouse'].search([]):
            if w.view_location_id not in warehouse_location_list:
                warehouse_location_list.append(w.view_location_id.name)

        index = 0
        for warehouse_record in result['warehouses']:
            for _ in warehouse_location_list:
                if warehouse_record['id'] not in warehouse_id_list:
                    warehouse_id_list.append(warehouse_record['id'])
                    warehouse_record.update({"location_id":warehouse_location_list[index]})
                    index+=1
        return result
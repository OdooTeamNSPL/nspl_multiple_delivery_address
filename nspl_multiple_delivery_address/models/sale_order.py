from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    custom_partner_id = fields.Many2one('res.partner', string="Delivery Address")

    def _prepare_procurement_values(self, group_id):
        vals = super()._prepare_procurement_values(group_id)
        if self.custom_partner_id:
            vals['custom_partner_id'] = self.custom_partner_id.id
        return vals

    def _get_procurement_group(self):
        self.ensure_one()
        base_group = super()._get_procurement_group()
        if self.custom_partner_id:
            # generate unique group for each delivery address
            name = f"{self.order_id.name}-{self.custom_partner_id.id}"
            group = self.env['procurement.group'].search([('name', '=', name)], limit=1)
            if not group:
                group = self.env['procurement.group'].create({
                    'name': name,
                    'partner_id': self.custom_partner_id.id,
                    'move_type': self.order_id.picking_policy,
                    'sale_id': self.order_id.id,
                })
            return group
        return base_group


class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _get_grouping_keys(self):
        keys = super()._get_grouping_keys()
        if 'custom_partner_id' not in keys:
            keys.append('custom_partner_id')
        return keys


class StockPicking(models.Model):
    _inherit = "stock.picking"

    custom_partner_id = fields.Many2one('res.partner', string="Delivery Address")

class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    custom_partner_id = fields.Many2one('res.partner', string="Delivery Address")


class StockMove(models.Model):
    _inherit = "stock.move"

    custom_partner_id = fields.Many2one('res.partner', string='Delivery Address')

    def _get_new_picking_values(self):
        # Odoo combines multiple stock.moves to create a single picking
        res = super(StockMove, self[0])._get_new_picking_values()
        custom_partner = self.mapped('custom_partner_id')
        if len(custom_partner) == 1:
            res['custom_partner_id'] = custom_partner.id
            res['partner_id'] = custom_partner.id
        return res

    def _prepare_move_line_vals(self, quantity=None, reserved_quant=None, **kwargs):
        vals = super()._prepare_move_line_vals(quantity=quantity, reserved_quant=reserved_quant, **kwargs)
        if self.custom_partner_id:
            vals['custom_partner_id'] = self.custom_partner_id.id
        return vals

    @api.model_create_multi
    def create(self, vals_list):
        moves = super().create(vals_list)
        for move in moves:
            if move.sale_line_id and move.sale_line_id.custom_partner_id:
                move.custom_partner_id = move.sale_line_id.custom_partner_id
        return moves

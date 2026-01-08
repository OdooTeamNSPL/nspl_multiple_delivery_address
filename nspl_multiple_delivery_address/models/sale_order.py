from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    custom_partner_id = fields.Many2one('res.partner', string="Delivery Address")

    def _prepare_procurement_values(self):
        vals = super()._prepare_procurement_values()
        if self.custom_partner_id:
            vals['custom_partner_id'] = self.custom_partner_id.id
        return vals


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        # Confirm sale order first
        res = super().action_confirm()

        # Set custom_partner_id on sale.order.line if empty
        for order in self:
            for line in order.order_line:
                if not line.custom_partner_id:
                    line.custom_partner_id = order.partner_id

        return res


class StockMove(models.Model):
    _inherit = "stock.move"

    custom_partner_id = fields.Many2one('res.partner', string='Delivery Address')

    def _get_new_picking_values(self):
        res = super()._get_new_picking_values()
        partners = self.mapped('custom_partner_id')
        if len(partners) == 1:
            res['custom_partner_id'] = partners.id
            res['partner_id'] = partners.id
        else:
            res['custom_partner_id'] = False
        return res

    @api.model_create_multi
    def create(self, vals_list):
        moves = super().create(vals_list)
        for move in moves:
            # propagate custom_partner_id from sale line
            if move.sale_line_id and move.sale_line_id.custom_partner_id:
                move.custom_partner_id = move.sale_line_id.custom_partner_id
                if move.move_line_ids:
                    move.move_line_ids.write({'custom_partner_id': move.custom_partner_id.id})
        return moves


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    custom_partner_id = fields.Many2one('res.partner', string="Delivery Address")


from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    custom_partner_id = fields.Many2one('res.partner', string="Delivery Address")

    @api.model_create_multi
    def create(self, vals_list):
        pickings = super().create(vals_list)
        for picking in pickings:
            # If picking has no custom_partner_id, take from move lines
            if not picking.custom_partner_id:
                partners = picking.move_ids.mapped('custom_partner_id')
                if len(partners) == 1:
                    picking.custom_partner_id = partners.id
                else:
                    # fallback to main partner of picking or leave empty
                    picking.custom_partner_id = picking.partner_id
            # propagate to move lines just to be safe
            for move in picking.move_ids:
                if move.custom_partner_id != picking.custom_partner_id:
                    move.custom_partner_id = picking.custom_partner_id
                    if move.move_line_ids:
                        move.move_line_ids.write({'custom_partner_id': picking.custom_partner_id.id})
        return pickings

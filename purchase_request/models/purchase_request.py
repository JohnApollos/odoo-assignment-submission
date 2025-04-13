from odoo import api, fields, models
from odoo.exceptions import UserError

class PurchaseRequest(models.Model):
    _name = 'purchase.request'
    _description = 'Purchase Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Request Reference', required=True, copy=False, readonly=True, default='New')
    user_id = fields.Many2one('res.users', string='Requested By', default=lambda self: self.env.user, readonly=True)
    date_request = fields.Date(string='Request Date', default=fields.Date.today, readonly=True)
    partner_id = fields.Many2one('res.partner', string='Vendor', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='State', default='draft', tracking=True)
    line_ids = fields.One2many('purchase.request.line', 'request_id', string='Request Lines')
    purchase_order_ids = fields.One2many('purchase.order', 'purchase_request_id', string='Purchase Orders')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('purchase.request') or 'New'
        return super(PurchaseRequest, self).create(vals_list)

    def action_confirm(self):
        self.write({'state': 'confirmed'})

    def action_done(self):
        self.write({'state': 'done'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_create_purchase_order(self):
        if not self.partner_id:
            raise UserError('Please specify a Vendor for the Purchase Request before creating a Purchase Order.')
        order_lines = [
            (0, 0, {
                'product_id': line.product_id.id,
                'product_qty': line.quantity,
                'name': line.product_id.name,
                'date_planned': fields.Date.today(),
                'product_uom': line.product_id.uom_id.id,
            }) for line in self.line_ids if line.product_id
        ]
        if not order_lines:
            raise UserError('No valid products to create a purchase order.')
        purchase_order = self.env['purchase.order'].create({
            'partner_id': self.partner_id.id,
            'purchase_request_id': self.id,
            'order_line': order_lines,
        })
        return {
            'type': 'ir.actions.act_window',
            'name': 'Purchase Order',
            'res_model': 'purchase.order',
            'res_id': purchase_order.id,
            'view_mode': 'form',
            'target': 'current',
        }

class PurchaseRequestLine(models.Model):
    _name = 'purchase.request.line'
    _description = 'Purchase Request Line'

    request_id = fields.Many2one('purchase.request', string='Purchase Request', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    quantity = fields.Float(string='Quantity', required=True, default=1.0)
    product_uom_id = fields.Many2one('uom.uom', string='Unit of Measure', related='product_id.uom_id')

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    purchase_request_id = fields.Many2one('purchase.request', string='Purchase Request', readonly=True)

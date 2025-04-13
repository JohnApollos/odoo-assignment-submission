from odoo import models, fields

class PurchaseBid(models.Model):
    _name = 'purchase.bid'
    _description = 'Purchase Bid'

    rfq_id = fields.Many2one('purchase.order', string='RFQ', required=True, ondelete='cascade')
    vendor_id = fields.Many2one('res.partner', string='Vendor', required=True, domain=[('supplier_rank', '>', 0)])
    bid_amount = fields.Float(string='Bid Amount', required=True)
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, default=lambda self: self.env.company.currency_id)
    bid_date = fields.Date(string='Bid Date', required=True, default=fields.Date.today)
    is_winning_bid = fields.Boolean(string='Winning Bid', default=False)
    notes = fields.Text(string='Notes')
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')

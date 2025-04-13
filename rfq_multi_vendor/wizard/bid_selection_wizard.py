from odoo import fields, models, api

class BidSelectionWizard(models.TransientModel):
    _name = 'bid.selection.wizard'
    _description = 'Bid Selection Wizard'

    rfq_id = fields.Many2one('purchase.order', string='RFQ', required=True)
    bid_id = fields.Many2one('purchase.bid', string='Bid', required=True, domain="[('rfq_id', '=', rfq_id)]")

    def action_select_winning_bid(self):
        self.ensure_one()
        self.rfq_id.bid_ids.write({'is_winning_bid': False})
        self.bid_id.write({'is_winning_bid': True})
        self.rfq_id.write({'bids_edited': False})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.order',
            'res_id': self.rfq_id.id,
            'view_mode': 'form',
            'target': 'current',
        }

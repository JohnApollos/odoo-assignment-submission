from odoo import api, fields, models
from odoo.exceptions import ValidationError

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    vendor_ids = fields.Many2many('res.partner', string='Vendors', domain=[('supplier_rank', '>', 0)], required=True)
    bid_ids = fields.One2many('purchase.bid', 'rfq_id', string='Bids')
    has_winning_bid = fields.Boolean(string='Has Winning Bid', compute='_compute_has_winning_bid', store=True)
    bids_edited = fields.Boolean(string='Bids Edited', default=False)
    debug_has_winning_bid = fields.Boolean(string='Debug: Has Winning Bid', compute='_compute_has_winning_bid', store=True)
    debug_bids_edited = fields.Boolean(string='Debug: Bids Edited', compute='_compute_debug_bids_edited')
    debug_bid_count = fields.Integer(string='Debug: Bid Count', compute='_compute_debug_bid_count')
    debug_select_winning_bid_visible = fields.Boolean(string='Debug: Select Winning Bid Visible', compute='_compute_debug_select_winning_bid_visible')

    @api.depends('vendor_ids')
    def _compute_partner_id(self):
        for order in self:
            print(f"Computing partner_id for order {order.id or 'new'}: vendor_ids={order.vendor_ids.ids}")
            if not order.vendor_ids:
                default_vendor = self.env['res.partner'].search([('supplier_rank', '>', 0)], limit=1)
                if not default_vendor:
                    default_vendor = self.env['res.partner'].create({
                        'name': 'Default Vendor',
                        'supplier_rank': 1
                    })
                order.vendor_ids = [(6, 0, [default_vendor.id])]
                print(f"Set default vendor_ids={order.vendor_ids.ids}")
            order.partner_id = order.vendor_ids[0]
            print(f"Set partner_id={order.partner_id.id}")

    @api.depends('bid_ids', 'bid_ids.is_winning_bid')
    def _compute_has_winning_bid(self):
        for order in self:
            if not order.bid_ids:
                print(f"RFQ {order.id}: No bids, setting has_winning_bid=False")
                order.has_winning_bid = False
            else:
                order.has_winning_bid = any(bid.is_winning_bid for bid in order.bid_ids)
                print(f"RFQ {order.id}: Bids exist, has_winning_bid={order.has_winning_bid}, winning bids: {[bid.id for bid in order.bid_ids if bid.is_winning_bid]}")

    @api.depends('bids_edited')
    def _compute_debug_bids_edited(self):
        for order in self:
            order.debug_bids_edited = order.bids_edited

    @api.depends('bid_ids')
    def _compute_debug_bid_count(self):
        for order in self:
            order.debug_bid_count = len(order.bid_ids)

    @api.depends('bid_ids', 'has_winning_bid', 'bids_edited')
    def _compute_debug_select_winning_bid_visible(self):
        for order in self:
            visible = bool(order.bid_ids and (not order.has_winning_bid or order.bids_edited))
            print(f"RFQ {order.id}: Select Winning Bid button visibility - bid_ids: {bool(order.bid_ids)}, has_winning_bid: {order.has_winning_bid}, bids_edited: {order.bids_edited}, visible: {visible}")
            order.debug_select_winning_bid_visible = visible

    def action_rfq_send(self):
        self.ensure_one()
        template = self.env.ref('purchase.email_template_edi_purchase')
        if not template:
            raise ValidationError("Email template for RFQ not found.")
        compose_form = self.env.ref('mail.email_compose_message_wizard_form')
        if self.has_winning_bid:
            winning_bid = self.bid_ids.filtered(lambda b: b.is_winning_bid)
            partner_ids = [winning_bid.vendor_id.id] if winning_bid else []
        else:
            partner_ids = self.vendor_ids.ids
        ctx = {
            'default_model': 'purchase.order',
            'default_res_ids': [self.id],
            'default_use_template': bool(template),
            'default_template_id': template.id,
            'default_composition_mode': 'comment',
            'mark_rfq_as_sent': True,
            'custom_layout': "mail.mail_notification_light",
            'force_email': True,
            'default_partner_ids': partner_ids,
        }
        return {
            'name': 'Compose Email',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }

    def action_select_winning_bid(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Select Winning Bid',
            'res_model': 'bid.selection.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_rfq_id': self.id},
        }

    def action_create_purchase_order(self):
        self.ensure_one()
        winning_bid = self.bid_ids.filtered(lambda b: b.is_winning_bid)
        if not winning_bid:
            raise ValidationError("No winning bid selected.")
        order_lines = [
            (0, 0, {
                'product_id': line.product_id.id,
                'product_qty': line.product_qty,
                'price_unit': winning_bid.bid_amount / line.product_qty if line.product_qty else 0,
                'name': line.name,
                'date_planned': fields.Date.today(),
                'product_uom': line.product_uom.id,
            }) for line in self.order_line if line.product_id
        ]
        if not order_lines:
            raise ValidationError("No valid order lines found to create a purchase order.")
        purchase_order = self.env['purchase.order'].create({
            'partner_id': winning_bid.vendor_id.id,
            'vendor_ids': [(6, 0, [winning_bid.vendor_id.id])],
            'currency_id': winning_bid.currency_id.id,
            'order_line': order_lines,
        })
        self.write({'state': 'purchase'})
        return {
            'type': 'ir.actions.act_window',
            'name': 'Purchase Order',
            'res_model': 'purchase.order',
            'res_id': purchase_order.id,
            'view_mode': 'form',
            'target': 'current',
        }

    @api.model_create_multi
    def create(self, vals_list):
        print(f"Creating purchase orders with vals_list={vals_list}")
        for vals in vals_list:
            if 'vendor_ids' not in vals or not vals.get('vendor_ids'):
                default_vendor = self.env['res.partner'].search([('supplier_rank', '>', 0)], limit=1)
                if not default_vendor:
                    default_vendor = self.env['res.partner'].create({
                        'name': 'Default Vendor',
                        'supplier_rank': 1
                    })
                vals['vendor_ids'] = [(6, 0, [default_vendor.id])]
                print(f"Set default vendor_ids={vals['vendor_ids']} for vals={vals}")
            if 'partner_id' not in vals or not vals.get('partner_id'):
                vendor_ids = vals.get('vendor_ids')
                if vendor_ids and isinstance(vendor_ids, list) and vendor_ids[0][0] == 6 and vendor_ids[0][2]:
                    vals['partner_id'] = vendor_ids[0][2][0]
                else:
                    default_vendor = self.env['res.partner'].search([('supplier_rank', '>', 0)], limit=1)
                    if not default_vendor:
                        default_vendor = self.env['res.partner'].create({
                            'name': 'Default Vendor',
                            'supplier_rank': 1
                        })
                    vals['partner_id'] = default_vendor.id
                    print(f"Set default partner_id={vals['partner_id']} for vals={vals}")
        records = super(PurchaseOrder, self).create(vals_list)
        print(f"Created records with IDs={records.ids}")
        return records

    def write(self, vals):
        print(f"Writing to purchase order {self.id}: vals={vals}")
        if 'vendor_ids' in vals and not vals['vendor_ids']:
            raise ValidationError("At least one vendor must be selected for the purchase order.")
        if 'bid_ids' in vals:
            print(f"RFQ {self.id}: Bids modified, setting bids_edited=True")
            self.bids_edited = True
        return super(PurchaseOrder, self).write(vals)

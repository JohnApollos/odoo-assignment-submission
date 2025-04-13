# Odoo Assignment Documentation: Purchase Request and RFQ Multi-Vendor Modules

## Overview

This project consists of two custom Odoo 18.0 modules developed to enhance the procurement process:

* **Purchase Request Module (purchase\_request)**: This module introduces a "Purchase Request" feature, allowing users to create requests for purchasing products, specify a vendor, and generate purchase orders from confirmed requests.

* **RFQ Multi-Vendor Module (rfq\_multi\_vendor)**: This module extends the Request for Quotation (RFQ) functionality in Odoo to support multiple vendors, manage bids, select a winning bid, and generate a purchase order based on the winning bid.

Both modules were developed and tested in Odoo 18.0, ensuring compatibility with the core purchase module.

##   Installation Instructions

###   Prerequisites

* Odoo 18.0 installed on a Linux system (e.g., Ubuntu).

* A virtual environment set up for Odoo.

* Access to the Odoo database (mydb in this case).

###   Steps to Install

1.  **Clone or Copy the Modules:**

    * Place the `purchase_request` and `rfq_multi_vendor` directories into the `custom_addons` directory of your Odoo installation. For example:

        ```
        /home/apollos/Downloads/odoo-18.0/custom_addons/purchase_request/
        /home/apollos/Downloads/odoo-18.0/custom_addons/rfq_multi_vendor
        ```

2.  **Update the Odoo Configuration:**

    * Ensure the `custom_addons` path is included in the Odoo configuration. The command to start Odoo should include the `--addons-path` option, such as:

        ```bash
        ./odoo-bin --addons-path=/home/apollos/Downloads/odoo-18.0/addons,/home/apollos/Downloads/odoo-18.0/custom_addons -d mydb
        ```

3.  **Install the Modules:**

    * Start Odoo with the `-u` option to update and install the modules:

        ```bash
        cd ~/Downloads/odoo-18.0
        source venv/bin/activate
        ./odoo-bin --addons-path=/home/apollos/Downloads/odoo-18.0/addons,/home/apollos/Downloads/odoo-18.0/custom_addons -d mydb -u purchase_request
        ./odoo-bin --addons-path=/home/apollos/Downloads/odoo-18.0/addons,/home/apollos/Downloads/odoo-18.0/custom_addons -d mydb -u rfq_multi_vendor
        ```

4.  **Access Odoo:**

    * Open your browser and navigate to `http://localhost:8069`.

    * Log in with your credentials, go to the "Apps" menu, and confirm that both modules ("Purchase Request" and "RFQ Multiple Vendors") are installed.

##   Module Details

###   1. Purchase Request Module (purchase\_request)

####   Purpose

The `purchase_request` module allows users to create purchase requests, specify a vendor, and generate purchase orders from confirmed requests. It provides a streamlined process for initiating procurement activities.

####   Features

* Create and manage purchase requests with a vendor and product lines.

* Confirm, cancel, or mark requests as done.

* Generate a purchase order from a confirmed request, ensuring a vendor is specified.

* Track the state of requests (Draft, Confirmed, Done, Cancelled).

####   Usage Guide

* **Access Purchase Requests:** Navigate to `Purchases > Purchase Requests`.

* **Create a Purchase Request:**

    * Click "Create".

    * Select a vendor (required), add products and quantities in the "Request Lines" tab, and save.

* **Confirm the Request:** Click "Confirm" to move the request to the "Confirmed" state.

* **Generate a Purchase Order:**

    * Click "Create Purchase Order".

    * Ensure a vendor is selected, or you’ll receive an error. A new purchase order will be created with the specified vendor and products.

* **Complete or Cancel:** Click "Mark as Done" to complete the request, or "Cancel" to cancel it.

####   File Structure

├── init.py├── manifest.py├── models│   ├── init.py│   └── purchase_request.py├── views│   ├── purchase_request_views.xml│   └── purchase_request_line_views.xml├── security│   └── ir.model.access.csv└── data└── sequence.xml
* `__init__.py`: Imports the models package.

* `__manifest__.py`: Module metadata, dependencies (`purchase`, `product`), and data files.

* `models/__init__.py`: Imports the `purchase_request` model.

* `models/purchase_request.py`: Defines the `purchase.request`, `purchase.request.line`, and inherited `purchase.order` models.

* `views/purchase_request_views.xml`: Defines list and form views for `purchase.request`, including the action and menu item.

* `views/purchase_request_line_views.xml`: Defines list and form views for `purchase.request.line`.

* `security/ir.model.access.csv`: Access rights for `purchase.request` and `purchase.request.line`.

* `data/sequence.xml`: Sequence for generating purchase request references (e.g., PR/00001).

####   Notes

* The `partner_id` field is required to generate a purchase order. Existing records without a `partner_id` may need to be updated using the Odoo shell.

* The module uses `list` instead of `tree` for view types to avoid compatibility issues in Odoo 18.0.

###   2. RFQ Multi-Vendor Module (rfq\_multi\_vendor)

####   Purpose

The `rfq_multi_vendor` module enhances the RFQ process by allowing multiple vendors to be assigned to an RFQ, managing bids from those vendors, selecting a winning bid, and generating a purchase order based on the winning bid.

####   Features

* Assign multiple vendors to an RFQ.

* Add and manage bids from vendors, including bid amount, currency, date, notes, and attachments.

* Select a winning bid using a wizard.

* Generate a purchase order from the winning bid.

* Debug fields to monitor the RFQ state (e.g., bid count, winning bid status).

####   Usage Guide

* **Create an RFQ:** Navigate to `Purchases > Requests for Quotation`.

    * Click "Create", add products, and select multiple vendors in the "Vendors" field.

* **Send the RFQ:** Click "Send by Email" to send the RFQ to all selected vendors (or the winning vendor if a bid has been selected).

* **Add Bids:** In the "Bids" tab, add bids for each vendor, specifying the bid amount, currency, and date.

* **Select a Winning Bid:**

    * Click "Select Winning Bid", choose a bid in the wizard, and confirm.

    * The selected bid will be marked as the winning bid, and other bids will be unmarked.

* **Generate a Purchase Order:** Click "Create Purchase Order" to generate a purchase order based on the winning bid.

####   File Structure

├── init.py├── manifest.py├── models│   ├── init.py│   ├── purchase.py│   └── purchase_bid.py├── views│   ├── purchase_bid_views.xml│   ├── purchase_views.xml│   └── purchase_bid_inline_views.xml├── wizard│   ├── init.py│   ├── bid_selection_wizard.py│   └── bid_selection_wizard_views.xml├── security│   └── ir.model.access.csv
* `__init__.py`: Imports the models and wizard packages.

* `__manifest__.py`: Contains module metadata, dependency (`purchase`), and data files.

* `models/__init__.py`: Imports the `purchase` and `purchase_bid` models.

* `models/purchase.py`: Extends `purchase.order` to add multi-vendor and bid management functionality.

* `models/purchase_bid.py`: Defines the `purchase.bid` model for managing bids.

* `views/purchase_bid_views.xml`: Defines list and form views for `purchase.bid`.

* `views/purchase_views.xml`: Extends the `purchase.order` form view to add vendor and bid fields, and adds a "Bids" menu.

* `views/purchase_bid_inline_views.xml`: Inline list and form views for `purchase.bid` in the RFQ form.

* `wizard/__init__.py`: Imports the `bid_selection_wizard` model.

* `wizard/bid_selection_wizard.py`: Defines the `bid.selection.wizard` transient model for selecting a winning bid.

* `wizard/bid_selection_wizard_views.xml`: Form view for the `bid.selection.wizard` model.

* `security/ir.model.access.csv`: Access rights for `purchase.bid` and `bid.selection.wizard`.

####   Notes

* The module uses `list` instead of `tree` for view types, similar to the `purchase_request` module.

* Debug fields (e.g., `debug_has_winning_bid`, `debug_bid_count`) are included for troubleshooting and can be removed in a production environment.

##   Testing

Both modules were thoroughly tested in Odoo 18.0:

**Purchase Request:**

* Created purchase requests with and without vendors.

* Confirmed requests and generated purchase orders.

* Tested cancellation and marking as done.

* Verified error handling when no vendor is specified.

**RFQ Multi-Vendor:**

* Created RFQs with multiple vendors.

* Added bids, selected a winning bid, and generated a purchase order.

* Tested email sending to vendors and debug field visibility.

* No errors were encountered after resolving initial issues (e.g., view type mismatches, missing licenses).

##   Future Enhancements

**Purchase Request Module:**

* Add an approval workflow before confirming requests.

* Create a PDF report summarizing purchase requests.

* Auto-suggest vendors based on product history.

**RFQ Multi-Vendor Module:**

* Add bid comparison reports or charts.

* Implement email notifications for vendors when their bid is selected.

* Remove debug fields for production use.

##   Troubleshooting

* **Error: "View types not defined tree found in act\_window action"**: This was resolved by changing `view_mode` from `tree,form` to `list,form` to match the `type="list"` in view definitions.

* **Error: "NOT NULL constraint on partner\_id"**:

    * Made `partner_id` non-required temporarily.

    * To make it required, update existing records using the Odoo shell:

        ```bash
        ./odoo-bin shell --addons-path=/home/apollos/Downloads/odoo-18.0/addons,/home/apollos/Downloads/odoo-18.0/custom_addons -d mydb
        ```

        In the shell:

        ```python
        default_vendor = env['res.partner'].search([('supplier_rank', '>', 0)], limit=1)
        requests = env['purchase.request'].search([('partner_id', '=', False)])
        for request in requests:
            request.partner_id = default_vendor
        env.cr.commit()
        exit()
        ```

##   Conclusion

The `purchase_request` and `rfq_multi_vendor` modules successfully extend Odoo’s procurement capabilities, providing a robust solution for managing purchase requests and multi-vendor RFQs. Both modules are fully functional, well-documented, and ready for use in Odoo 18.0.

**Author:** John Apollos Olal Onyango
**Date:** April 13, 2025

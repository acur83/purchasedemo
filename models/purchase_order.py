# -*- coding:utf-8 -*-
# ---------------------------------------------------------------------
# 
# ---------------------------------------------------------------------
# Copyright (c) 2017 BDC International Develop Team and Contributors
# All rights reserved.
#
# This is free software; you can redistribute it and/or modify it under
# the terms of the LICENCE attached (see LICENCE file) in the distribution
# package.
#
# Created on 11-04-19

from openerp import models, fields, api
from openerp.tools.translate import _
from odoo import exceptions


class PurchaseOrder(models.Model):
    """
    Purchase Order model customization.
    
    """
    _inherit = 'purchase.order'

    user_department_id = fields.Many2one('hr.department', store=True,
                                         compute='_compute_user_department')
    manager_loged_user = fields.Boolean(store=True, compute='_is_manager_user',
                                        default=True)
    state = fields.Selection([('draft', 'RFQ'),
                              ('sent', 'RFQ Sent'),
                              ('to approve', 'To Approve'),
                              ('purchase', 'Purchase Order'),
                              ('Approved', 'Approved'),
                              ('done', 'Locked'),
                              ('cancel', 'Cancelled')],
                             string='Status', readonly=True,
                             index=True, copy=False,
                             default='draft', track_visibility='onchange')

    @api.multi
    def action_view_invoice(self):
        '''Is needed redefine for avoid that the user can create a bill
        without a department manager approved.

        '''
        if self.state == 'Approved':
            return super(PurchaseOrder,self).action_view_invoice()
        else:
            raise exceptions.ValidationError(_('"Error"\
            Please aprove the purchase first..'))

    @api.multi
    def aprove_purchase(self):
        ''' Confirm the purchase.
        Also check if the logged user have the needed access for confirm a
        purchase order and raise an exception if not.

        '''
        # groups_name = ['Technical Features']
        groups_name = []
        if self.user_department_id:
            groups_name.append(
                self.user_department_id.name + '_Purchases_Manager')
            groups_name.append(
                self.user_department_id.name + '_Admin_Purchases')
        manager_groups = self.env['res.groups'].search([
            ('name','in', groups_name)
        ])
        flag = False
        for group in manager_groups:
            if self.env.user.id in group.users.ids:
                self.write({'state': 'Approved'})
                flag = True
        if not flag:
            raise exceptions.ValidationError(_('"Error"\
            You have no access to confirm a Purchase, please contact with\
            the department manager.'))
        else:
            return super(PurchaseOrder,self).action_view_invoice()

    @api.depends('state', 'partner_id')
    def _is_manager_user(self):
        self.manager_loged_user = False

    @api.depends('partner_id')
    def _compute_user_department(self):
        ''' Define if the logged user have an assigned department and store
        it in the purchase order for filter later using the created user rules. 

        '''
        if self.user_id.employee_ids.department_id:
            self.user_department_id = self.user_id.employee_ids.department_id.id

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


class HrDeparment(models.Model):
    """
    Hr Department Model customization.
    TODO: DOCUMENT
    
    """
    _inherit = 'hr.department'

    @api.model
    def create(self, vals):
        ''' Create the category, groups related with this new 
        department so the users could have two roles; user or manager
        and each one of this have diferents access level.

        '''
        IrModuleCat = self.env['ir.module.category']
        ResGroups = self.env['res.groups']
        IrRule = self.env['ir.rule']
        dptoCateg = IrModuleCat.sudo().create({
            'name' : vals.get('name') + " Deparment",
            'description' : 'Custom Purchase {dptoName}'.format(
                dptoName=vals.get('name', '')),
            'sequence' : 1
        })
        purchase_model_id = self.env['ir.model'].search(
            [('name', '=', 'Purchase Order')])        
        group_user = ResGroups.create({
            'name': '{dptoName}_Purchases_User'.format(
                dptoName=vals.get('name')),
            'category_id' : dptoCateg.id,
            # 'implied_ids': ResGroups.search([('name', '=', 'User')])
        })
        user_domain = "[('create_uid','=',user.id)]"
        userRule = IrRule.create({
            'name': 'Custom_Purchase_User_Rule_{dptoName}'.format(
                dptoName=vals.get('name')),
            'model_id': purchase_model_id.id,
            'groups': group_user,
            'domain_force': user_domain
        })
        userRule.groups = group_user        
        # ******************************************************************        
        group_manager = ResGroups.create({
            'name': '{dptoName}_Purchases_Manager'.format(
                dptoName=vals.get('name')),
            'category_id' : dptoCateg.id,
            # 'implied_ids': ResGroups.search([('name', '=', 'User')])
        })
        manager_domain = "['|', ('create_uid', '=', user.id),\
        ('user_department_id.member_ids.user_id', 'in', [user.id])]"
        managerRule = IrRule.create({
            'name': 'Custom_Purchase_Manager_Rule_{dptoName}'.format(
                dptoName=vals.get('name')),
            'model_id': purchase_model_id.id,
            'groups': group_manager,
            'domain_force': manager_domain
        })
        managerRule.groups = group_manager
        # ******************************************************************
        group_admin = ResGroups.create({
            'name': '{dptoName}_Admin_Purchases'.format(
                dptoName=vals.get('name')),
            'category_id' : dptoCateg.id,
        })
        managerRule = IrRule.create({
            'name': 'Custom_Purchases_Admin_Rule_{dptoName}'.format(
                dptoName=vals.get('name')),
            'model_id': purchase_model_id.id,
            'groups': group_admin,
            'domain_force': "[(1,'=',1)]"
        })
        managerRule.groups = group_admin
        return super(HrDeparment,self).create(vals)


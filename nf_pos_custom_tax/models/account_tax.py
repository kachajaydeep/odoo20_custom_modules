# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT.

import ast

from odoo import api, models, fields, _
from odoo.exceptions import ValidationError

from odoo.addons.account_tax_python.tools.formula_utils import (
    normalize_formula,
)    

_ALLOWED_FUNCS = ('min', 'max')

_ALLOWED_NAMES = (
    'price_unit',
    'quantity',
    'base',
    'product',
    'uom',
)

_ALLOWED_CONSTANT_T = (
    int,
    float,
    type(None),
)

# Same whitelist as Odoo 19 + ast.IfExp
_NODE_WHITELIST = (
    ast.Expression, ast.Name, ast.Call, ast.Subscript,
    ast.Constant,
    ast.BinOp, ast.Add, ast.Sub, ast.Mult, ast.Div,
    ast.BoolOp, ast.And, ast.Or,
    ast.Compare, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    ast.UnaryOp, ast.UAdd, ast.USub,
    
    # Added by custom module
    ast.IfExp,
)

class TaxFormulaValidator(ast.NodeVisitor):
    """Odoo 19 tax formula validator with if/else support."""

    def __init__(self, env):
        self.env = env
        super().__init__()

    def visit(self, node):
        if not isinstance(node, _NODE_WHITELIST):
            raise ValidationError(
                self.env._(
                    "Invalid AST node: %s",
                    type(node).__name__,
                )
            )
        super().visit(node)

    def visit_Constant(self, node):
        if not isinstance(node.value, _ALLOWED_CONSTANT_T):
            raise ValidationError(
                self.env._(
                    "Only int, float or None are allowed as constant values"
                )
            )

    def visit_Name(self, node):
        if node.id not in _ALLOWED_NAMES:
            raise ValidationError(
                self.env._(
                    "Unknown identifier: %s",
                    node.id,
                )
            )

        if not isinstance(node.ctx, ast.Load):
            raise ValidationError(
                self.env._(
                    "Only read access to identifiers is allowed"
                )
            )

    def visit_Call(self, node):
        if not (
            isinstance(node.func, ast.Name)
            and node.func.id in _ALLOWED_FUNCS
            and isinstance(node.func.ctx, ast.Load)
        ):
            raise ValidationError(
                self.env._("Unknown function call")
            )

        for arg in node.args:
            self.visit(arg)

        if node.keywords:
            raise ValidationError(
                self.env._("Kwargs are not allowed")
            )

    def visit_Subscript(self, node):
        if not (
            isinstance(node.value, ast.Name)
            and node.value.id in ("product", "uom")
            and isinstance(node.slice, ast.Constant)
            and isinstance(node.slice.value, str)
            and isinstance(node.ctx, ast.Load)
        ):
            raise ValidationError(
                self.env._(
                    "Only product['string'] or "
                    "uom['string'] read-access is allowed"
                )
            )

        self.visit(node.value)


def _check_custom_formula(env, formula):
    """Validate formula like Odoo 19, but additionally allow if/else."""

    try:
        tree = ast.parse(formula, mode="eval")
    except (SyntaxError, ValueError):
        raise ValidationError(
            env._("Invalid formula")
        )

    TaxFormulaValidator(env).visit(tree)


class AccountTax(models.Model):
    _inherit = "account.tax"

    @api.model
    def _check_and_normalize_formula(self, formula):
        """Override Odoo 19 validation to support Python if/else."""

        def is_field_serializable(model, field_name):
            assert isinstance(
                field_name,
                str,
            ), "Field name must be a string"

            field = self.env[model]._fields.get(field_name)

            return (
                isinstance(field, fields.Field)
                and not field.relational
            )

        transformed_formula, accessed_fields = normalize_formula(
            self.env,
            (formula or '0.0').strip(),
            field_predicate=is_field_serializable,
        )

        # DO NOT call Odoo's check_formula().
        # Use our custom validator instead.
        _check_custom_formula(
            self.env,
            transformed_formula,
        )

        return transformed_formula, accessed_fields
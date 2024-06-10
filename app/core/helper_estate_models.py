"""
Helper modes for use in Estate main model
"""

from django.db import models


class Asset(models.Model):
    name = models.CharField(max_length=255)
    estate = models.ForeignKey('core.Estate', related_name='assets', on_delete=models.CASCADE)


class Expense(models.Model):
    name = models.CharField(max_length=255)
    estate = models.ForeignKey('core.Estate', related_name='expenses', on_delete=models.CASCADE)


class Dispute(models.Model):
    description = models.TextField()
    estate = models.ForeignKey('core.Estate', related_name='disputes', on_delete=models.CASCADE)


# region < Expense helper models>
class TaxLiability(models.Model):
    description = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=9, decimal_places=2)
    expense = models.ForeignKey(Expense, related_name='tax_liabilities', on_delete=models.CASCADE)


class SecuredMortgages(models.Model):
    description = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=9, decimal_places=2)
    expense = models.ForeignKey(Expense, related_name='secured_mortgages', on_delete=models.CASCADE)


class OtherExpenses(models.Model):
    description = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=9, decimal_places=2)
    expense = models.ForeignKey(Expense, related_name='other_expenses', on_delete=models.CASCADE)


# endregion

# region <Assets helper models>
class RealAndLeaseholdProperty(models.Model):
    description = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=9, decimal_places=2)
    assets = models.ForeignKey(Asset, related_name='real_and_leaseholdproperties', on_delete=models.CASCADE)


class HouseholdContent(models.Model):
    description = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=9, decimal_places=2)
    assets = models.ForeignKey(Asset, related_name='household_contents', on_delete=models.CASCADE)


class CarsAndBoats(models.Model):
    description = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=9, decimal_places=2)
    assets = models.ForeignKey(Asset, related_name='cars_and_boats', on_delete=models.CASCADE)


class BusinessAssetsNotIncludedElsewhere(models.Model):
    desc = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=9, decimal_places=2)
    assets = models.ForeignKey(Asset, related_name='business_assets_not_included_elsewhere', on_delete=models.CASCADE)


class AssetsWithFinancialInstitutions(models.Model):
    desc = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=9, decimal_places=2)
    assets = models.ForeignKey(Asset, related_name='assets_with_financial_institutions', on_delete=models.CASCADE)


class FundsfromLifeInsurances(models.Model):
    desc = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=9, decimal_places=2)
    assets = models.ForeignKey(Asset, related_name='funds_from_life_insurances', on_delete=models.CASCADE)


class DebtsOwingToTheDeceased(models.Model):
    desc = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=9, decimal_places=2)
    assets = models.ForeignKey(Asset, related_name='debts_owing_to_the_deceased', on_delete=models.CASCADE)


class StocksSharesSecurities(models.Model):
    desc = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=9, decimal_places=2)
    assets = models.ForeignKey(Asset, related_name='stocks_shares_securities', on_delete=models.CASCADE)


class UnpaidPurchaseMoney(models.Model):
    desc = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=9, decimal_places=2)
    assets = models.ForeignKey(Asset, related_name='unpaid_purchase_money', on_delete=models.CASCADE)


class OtherPropertyNotIncluded(models.Model):
    desc = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=9, decimal_places=2)
    assets = models.ForeignKey(Asset, related_name='other_property_not_included', on_delete=models.CASCADE)


class DebtsAndFuneralExpensesPayableInTheState(models.Model):
    desc = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=9, decimal_places=2)
    assets = models.ForeignKey(Asset, related_name='debts_and_funeral_expenses_payable_in_the_state',
                               on_delete=models.CASCADE)
# endregion

"""
Serializers for estate API
"""

from rest_framework import serializers
from core.models import Estate, Asset, Expense, Dispute

from core.helper_estate_models import (RealAndLeaseholdProperty,
                                       HouseholdContent,
                                       CarsAndBoats,
                                       BusinessAssetsNotIncludedElsewhere,
                                       AssetsWithFinancialInstitutions,
                                       FundsfromLifeInsurances,
                                       DebtsOwingToTheDeceased,
                                       StocksSharesSecurities,
                                       UnpaidPurchaseMoney,
                                       OtherPropertyNotIncluded,
                                       DebtsAndFuneralExpensesPayableInTheState,
                                       TaxLiability,
                                       SecuredMortgages,
                                       OtherExpenses, )


class TaxLiabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxLiability
        fields = ("id", 'description', 'value',)
        read_only_fields = ('id',)


class SecuredMortgagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecuredMortgages
        fields = ("id", 'description', 'value',)
        read_only_fields = ('id',)


class OtherExpensesSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherExpenses
        fields = ("id", 'description', 'value',)
        read_only_fields = ('id',)


class ExpenseSerializer(serializers.ModelSerializer):
    tax_liabilities = TaxLiabilitySerializer(many=True, read_only=True)
    secured_mortgages = SecuredMortgagesSerializer(many=True, read_only=True)
    other_expenses = OtherExpensesSerializer(many=True, read_only=True)

    class Meta:
        model = Expense
        fields = ('id', 'name', 'tax_liabilities', 'secured_mortgages', 'other_expenses',)
        read_only_fields = ('id', 'name')


class RealAndLeaseholdPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = RealAndLeaseholdProperty
        fields = ("id", 'description', 'value',)
        read_only_fields = ('id',)


class HouseholdContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseholdContent
        fields = ("id", 'description', 'value',)
        read_only_fields = ('id',)


class CarsAndBoatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarsAndBoats
        fields = ("id", 'description', 'value',)
        read_only_fields = ('id',)


class BusinessAssetsNotIncludedElsewhereSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessAssetsNotIncludedElsewhere
        fields = ("id", 'desc', 'value',)
        read_only_fields = ('id',)


class AssetsWithFinancialInstitutionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetsWithFinancialInstitutions
        fields = ("id", 'desc', 'value',)
        read_only_fields = ('id',)


class FundsFromLifeInsurancesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundsfromLifeInsurances
        fields = ("id", 'desc', 'value',)
        read_only_fields = ('id',)


class DebtsOwingToTheDeceasedSerializer(serializers.ModelSerializer):
    class Meta:
        model = DebtsOwingToTheDeceased
        fields = ("id", 'desc', 'value',)
        read_only_fields = ('id',)


class StocksSharesSecuritiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = StocksSharesSecurities
        fields = ("id", 'desc', 'value',)
        read_only_fields = ('id',)


class UnpaidPurchaseMoneySerializer(serializers.ModelSerializer):
    class Meta:
        model = UnpaidPurchaseMoney
        fields = ("id", 'desc', 'value',)
        read_only_fields = ('id',)


class OtherPropertyNotIncludedSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherPropertyNotIncluded
        fields = ("id", 'desc', 'value',)
        read_only_fields = ('id',)


class DebtsAndFuneralExpensesPayableInTheStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DebtsAndFuneralExpensesPayableInTheState
        fields = ("id", 'desc', 'value',)
        read_only_fields = ('id',)


class AssetSerializer(serializers.ModelSerializer):
    real_and_leaseholdProperties = RealAndLeaseholdPropertySerializer(many=True, read_only=True)
    household_contents = HouseholdContentSerializer(many=True, read_only=True)
    cars_and_boats = CarsAndBoatsSerializer(many=True, read_only=True)
    business_assets_not_included_elsewhere = BusinessAssetsNotIncludedElsewhereSerializer(many=True, read_only=True)
    assets_with_financial_institutions = AssetsWithFinancialInstitutionsSerializer(many=True, read_only=True)
    funds_from_life_insurances = FundsFromLifeInsurancesSerializer(many=True, read_only=True)
    debts_owing_to_the_deceased = DebtsOwingToTheDeceasedSerializer(many=True, read_only=True)
    stocks_shares_securities = StocksSharesSecuritiesSerializer(many=True, read_only=True)
    unpaid_purchase_money = UnpaidPurchaseMoneySerializer(many=True, read_only=True)
    other_property_not_included = OtherPropertyNotIncludedSerializer(many=True, read_only=True)
    debts_and_funeral_expenses_payable_in_the_state = DebtsAndFuneralExpensesPayableInTheStateSerializer(many=True,
                                                                                                         read_only=True)

    class Meta:
        model = Asset
        fields = ('id', 'name', 'real_and_leaseholdProperties', 'household_contents', 'cars_and_boats',
                  'business_assets_not_included_elsewhere', 'assets_with_financial_institutions',
                  'funds_from_life_insurances', 'debts_owing_to_the_deceased', 'stocks_shares_securities',
                  'unpaid_purchase_money', 'other_property_not_included',
                  'debts_and_funeral_expenses_payable_in_the_state')
        read_only_fields = ('id', 'name')


class DisputeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispute
        fields = ('id', 'description',)
        read_only_fields = ('id',)


class EstateSerializer(serializers.ModelSerializer):
    assets = AssetSerializer(many=True, read_only=True)
    expenses = ExpenseSerializer(many=True, read_only=True)
    disputes = DisputeSerializer(many=True, read_only=True)

    class Meta:
        model = Estate
        fields = ('id', 'assets', 'disputes', 'expenses')
        read_only_fields = ('id',)

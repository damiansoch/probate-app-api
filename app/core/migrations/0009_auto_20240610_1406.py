# Generated by Django 3.2.25 on 2024-06-10 14:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20240607_1148'),
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Estate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('estate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to='core.estate')),
            ],
        ),
        migrations.CreateModel(
            name='UnpaidPurchaseMoney',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.CharField(max_length=255)),
                ('value', models.DecimalField(decimal_places=2, max_digits=9)),
                ('assets', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='unpaid_purchase_money', to='core.asset')),
            ],
        ),
        migrations.CreateModel(
            name='TaxLiability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('value', models.DecimalField(decimal_places=2, max_digits=9)),
                ('expense', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tax_liabilities', to='core.expense')),
            ],
        ),
        migrations.CreateModel(
            name='StocksSharesSecurities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.CharField(max_length=255)),
                ('value', models.DecimalField(decimal_places=2, max_digits=9)),
                ('assets', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stocks_shares_securities', to='core.asset')),
            ],
        ),
        migrations.CreateModel(
            name='SecuredMortgages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('value', models.DecimalField(decimal_places=2, max_digits=9)),
                ('expense', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='secured_mortgages', to='core.expense')),
            ],
        ),
        migrations.CreateModel(
            name='RealAndLeaseholdProperty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('value', models.DecimalField(decimal_places=2, max_digits=9)),
                ('assets', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='real_and_leaseholdproperties', to='core.asset')),
            ],
        ),
        migrations.CreateModel(
            name='OtherPropertyNotIncluded',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.CharField(max_length=255)),
                ('value', models.DecimalField(decimal_places=2, max_digits=9)),
                ('assets', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='other_property_not_included', to='core.asset')),
            ],
        ),
        migrations.CreateModel(
            name='OtherExpenses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('value', models.DecimalField(decimal_places=2, max_digits=9)),
                ('expense', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='other_expenses', to='core.expense')),
            ],
        ),
        migrations.CreateModel(
            name='HouseholdContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('value', models.DecimalField(decimal_places=2, max_digits=9)),
                ('assets', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='household_contents', to='core.asset')),
            ],
        ),
        migrations.CreateModel(
            name='FundsfromLifeInsurances',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.CharField(max_length=255)),
                ('value', models.DecimalField(decimal_places=2, max_digits=9)),
                ('assets', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='funds_from_life_insurances', to='core.asset')),
            ],
        ),
        migrations.CreateModel(
            name='Dispute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('estate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disputes', to='core.estate')),
            ],
        ),
        migrations.CreateModel(
            name='DebtsOwingToTheDeceased',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.CharField(max_length=255)),
                ('value', models.DecimalField(decimal_places=2, max_digits=9)),
                ('assets', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='debts_owing_to_the_deceased', to='core.asset')),
            ],
        ),
        migrations.CreateModel(
            name='DebtsAndFuneralExpensesPayableInTheState',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.CharField(max_length=255)),
                ('value', models.DecimalField(decimal_places=2, max_digits=9)),
                ('assets', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='debts_and_funeral_expenses_payable_in_the_state', to='core.asset')),
            ],
        ),
        migrations.CreateModel(
            name='CarsAndBoats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('value', models.DecimalField(decimal_places=2, max_digits=9)),
                ('assets', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cars_and_boats', to='core.asset')),
            ],
        ),
        migrations.CreateModel(
            name='BusinessAssetsNotIncludedElsewhere',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.CharField(max_length=255)),
                ('value', models.DecimalField(decimal_places=2, max_digits=9)),
                ('assets', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='business_assets_not_included_elsewhere', to='core.asset')),
            ],
        ),
        migrations.CreateModel(
            name='AssetsWithFinancialInstitutions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.CharField(max_length=255)),
                ('value', models.DecimalField(decimal_places=2, max_digits=9)),
                ('assets', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assets_with_financial_institutions', to='core.asset')),
            ],
        ),
        migrations.AddField(
            model_name='asset',
            name='estate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assets', to='core.estate'),
        ),
    ]

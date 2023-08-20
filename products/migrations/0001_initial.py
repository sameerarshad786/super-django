# Generated by Django 4.2 on 2023-08-18 11:02

from decimal import Decimal
import django.contrib.postgres.fields.ranges
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductSource',
            fields=[
                ('uuid_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.uuid')),
                ('name', models.CharField(max_length=155)),
                ('domain', models.URLField(unique=True)),
                ('icon', models.URLField(unique=True)),
            ],
            bases=('core.uuid',),
        ),
        migrations.CreateModel(
            name='ProductTypes',
            fields=[
                ('uuid_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.uuid')),
                ('type', models.CharField(max_length=150, unique=True)),
                ('valid_name', models.BooleanField(default=False)),
            ],
            bases=('core.uuid',),
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('uuid_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.uuid')),
                ('name', models.CharField(max_length=500, unique=True)),
                ('description', models.TextField()),
                ('brand', models.CharField(choices=[('not defined', 'Not Defined'), ('apple', 'Apple'), ('samsung', 'Samsung'), ('google', 'Google'), ('lg', 'LG'), ('huawei', 'Huawei'), ('htc', 'HTC'), ('oneplus', 'OnePlus'), ('blackberry', 'BlackBerry'), ('motorola', 'Motorola'), ('nokia', 'Nokia'), ('redmi', 'Redmi'), ('oppo', 'Oppo'), ('vivo', 'Vivo'), ('itel', 'Itel'), ('infinix', 'Infinix'), ('sony', 'Sony'), ('realme', 'Realme'), ('tecno', 'Tecno')], default='not defined', max_length=11)),
                ('image', models.URLField()),
                ('url', models.URLField(max_length=500, unique=True)),
                ('items_sold', models.PositiveIntegerField(default=0)),
                ('ratings', models.PositiveIntegerField(default=0)),
                ('condition', models.CharField(choices=[('not defined', 'Not Defined'), ('new', 'New'), ('used', 'Used'), ('open box', 'Open Box'), ('refurbished', 'Refurbished'), ('dead', 'Dead')], default='not defined', max_length=11)),
                ('original_price', models.DecimalField(decimal_places=2, default=0, max_digits=7)),
                ('price', django.contrib.postgres.fields.ranges.DecimalRangeField(default=(Decimal('0.00'), Decimal('0.00')))),
                ('shipping_charges', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('source', models.CharField(choices=[('not defined', 'Not Defined'), ('amazon', 'Amazon'), ('ebay', 'Ebay'), ('daraz', 'Daraz'), ('ali express', 'Ali Express'), ('ali baba', 'Ali Baba'), ('olx', 'olx')], max_length=11)),
                ('discount', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(-100), django.core.validators.MaxValueValidator(0)])),
                ('product_source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.productsource')),
                ('type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.producttypes')),
            ],
            bases=('core.uuid',),
        ),
    ]
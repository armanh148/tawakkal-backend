from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_order_status_and_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.CharField(max_length=50, verbose_name='Retail Price'),
        ),
        migrations.AlterField(
            model_name='product',
            name='old_price',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Old Price'),
        ),
    ]

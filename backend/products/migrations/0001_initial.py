# Generated by Django 5.0.6 on 2025-02-01 19:33

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('setting', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, choices=[('Addis Ababa', 'Addis Ababa'), ('Diredawa', 'Diredawa'), ('Sheger', 'Sheger'), ('Amhara Region', 'Amhara Region'), ('Tigray Region', 'Tigray Region'), ('Oromia Region', 'Oromia Region'), ('Southern Ethiopia', 'Southern Ethiopia'), ('Afar Region', 'Afar Region'), ('Somali Region', 'Somali Region'), ('Gurage', 'Gurage'), ('Silte Zone', 'Silte Zone')], max_length=50, null=True)),
                ('approvalStatus', models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Approved', 'Approved')], default='Pending', max_length=50, null=True)),
                ('paymentStatus', models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Paid', 'Paid')], default='Pending', max_length=50, null=True)),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, help_text='Latitude of the location', max_digits=9, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, help_text='Longitude of the location', max_digits=9, null=True)),
                ('phonenumber', models.CharField(blank=True, max_length=50, null=True)),
                ('removed', models.BooleanField(default=False)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('sell_or_rent', models.CharField(blank=True, choices=[('Sale', 'Sale'), ('Rent', 'Rent')], max_length=50, null=True)),
                ('transmission', models.CharField(blank=True, choices=[('Automatic', 'Automatic'), ('Manual', 'Manual')], max_length=50, null=True)),
                ('fuelType', models.CharField(blank=True, choices=[('Benzin', 'Benzin'), ('Fuel', 'Fuel'), ('Electric', 'Electric')], max_length=50, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('license', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=50, null=True)),
                ('yearofMake', models.IntegerField(default=0)),
                ('model', models.CharField(blank=True, max_length=255, null=True)),
                ('mileage', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('carMake', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='car', to='setting.carmake')),
                ('carType', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='car', to='setting.cartype')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s', to='setting.category')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FreeStaffOrItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, choices=[('Addis Ababa', 'Addis Ababa'), ('Diredawa', 'Diredawa'), ('Sheger', 'Sheger'), ('Amhara Region', 'Amhara Region'), ('Tigray Region', 'Tigray Region'), ('Oromia Region', 'Oromia Region'), ('Southern Ethiopia', 'Southern Ethiopia'), ('Afar Region', 'Afar Region'), ('Somali Region', 'Somali Region'), ('Gurage', 'Gurage'), ('Silte Zone', 'Silte Zone')], max_length=50, null=True)),
                ('approvalStatus', models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Approved', 'Approved')], default='Pending', max_length=50, null=True)),
                ('paymentStatus', models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Paid', 'Paid')], default='Pending', max_length=50, null=True)),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, help_text='Latitude of the location', max_digits=9, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, help_text='Longitude of the location', max_digits=9, null=True)),
                ('phonenumber', models.CharField(blank=True, max_length=50, null=True)),
                ('removed', models.BooleanField(default=False)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('title', models.TextField(blank=True, max_length=500, null=True)),
                ('description', models.TextField(blank=True, max_length=2000, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s', to='setting.category')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='House',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, choices=[('Addis Ababa', 'Addis Ababa'), ('Diredawa', 'Diredawa'), ('Sheger', 'Sheger'), ('Amhara Region', 'Amhara Region'), ('Tigray Region', 'Tigray Region'), ('Oromia Region', 'Oromia Region'), ('Southern Ethiopia', 'Southern Ethiopia'), ('Afar Region', 'Afar Region'), ('Somali Region', 'Somali Region'), ('Gurage', 'Gurage'), ('Silte Zone', 'Silte Zone')], max_length=50, null=True)),
                ('approvalStatus', models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Approved', 'Approved')], default='Pending', max_length=50, null=True)),
                ('paymentStatus', models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Paid', 'Paid')], default='Pending', max_length=50, null=True)),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, help_text='Latitude of the location', max_digits=9, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, help_text='Longitude of the location', max_digits=9, null=True)),
                ('phonenumber', models.CharField(blank=True, max_length=50, null=True)),
                ('removed', models.BooleanField(default=False)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('sell_or_rent', models.CharField(blank=True, choices=[('Sale', 'Sale'), ('Rent', 'Rent')], max_length=50, null=True)),
                ('houseType', models.CharField(blank=True, choices=[('Condominium', 'Condominium'), ('Villa', 'Villa'), ('House G+', 'House G+'), ('Commercial', 'Commercial'), ('GuestHouse', 'GuestHouse'), ('Warehouse', 'Warehouse'), ('Land', 'Land')], max_length=50, null=True)),
                ('numberofBedrooms', models.IntegerField(default=0)),
                ('numberofBathrooms', models.IntegerField(default=0)),
                ('area', models.CharField(blank=True, max_length=255, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('license', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=50, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s', to='setting.category')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='JobVacancy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, choices=[('Addis Ababa', 'Addis Ababa'), ('Diredawa', 'Diredawa'), ('Sheger', 'Sheger'), ('Amhara Region', 'Amhara Region'), ('Tigray Region', 'Tigray Region'), ('Oromia Region', 'Oromia Region'), ('Southern Ethiopia', 'Southern Ethiopia'), ('Afar Region', 'Afar Region'), ('Somali Region', 'Somali Region'), ('Gurage', 'Gurage'), ('Silte Zone', 'Silte Zone')], max_length=50, null=True)),
                ('approvalStatus', models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Approved', 'Approved')], default='Pending', max_length=50, null=True)),
                ('paymentStatus', models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Paid', 'Paid')], default='Pending', max_length=50, null=True)),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, help_text='Latitude of the location', max_digits=9, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, help_text='Longitude of the location', max_digits=9, null=True)),
                ('phonenumber', models.CharField(blank=True, max_length=50, null=True)),
                ('removed', models.BooleanField(default=False)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('positionType', models.CharField(blank=True, choices=[('Fulltime', 'Fulltime'), ('Partimer', 'Partimer'), ('Contractual', 'Contractual')], max_length=50, null=True)),
                ('companyName', models.TextField(blank=True, max_length=500, null=True)),
                ('positionTitle', models.TextField(blank=True, max_length=500, null=True)),
                ('worklocation', models.TextField(blank=True, max_length=500, null=True)),
                ('experianceLevel', models.CharField(blank=True, choices=[('highLevel', 'highLevel'), ('mediumLevel', 'mediumLevel'), ('Senior', 'Senior'), ('junier', 'junier')], max_length=50, null=True)),
                ('salary', models.DecimalField(decimal_places=2, max_digits=10)),
                ('applicationDeadline', models.DateField(blank=True, null=True)),
                ('JobDescription', models.TextField(blank=True, max_length=2000, null=True)),
                ('JobRequirment', models.TextField(blank=True, max_length=2000, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s', to='setting.category')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ListingImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('image', models.ImageField(upload_to='listing_images/')),
                ('imagepath', models.CharField(blank=True, max_length=50, null=True)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
        ),
        migrations.CreateModel(
            name='LostOrFound',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, choices=[('Addis Ababa', 'Addis Ababa'), ('Diredawa', 'Diredawa'), ('Sheger', 'Sheger'), ('Amhara Region', 'Amhara Region'), ('Tigray Region', 'Tigray Region'), ('Oromia Region', 'Oromia Region'), ('Southern Ethiopia', 'Southern Ethiopia'), ('Afar Region', 'Afar Region'), ('Somali Region', 'Somali Region'), ('Gurage', 'Gurage'), ('Silte Zone', 'Silte Zone')], max_length=50, null=True)),
                ('approvalStatus', models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Approved', 'Approved')], default='Pending', max_length=50, null=True)),
                ('paymentStatus', models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Paid', 'Paid')], default='Pending', max_length=50, null=True)),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, help_text='Latitude of the location', max_digits=9, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, help_text='Longitude of the location', max_digits=9, null=True)),
                ('phonenumber', models.CharField(blank=True, max_length=50, null=True)),
                ('removed', models.BooleanField(default=False)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('typeofadd', models.CharField(choices=[('I need help looking for something I lost', 'I need help looking for something I lost'), ('Looking for the owner of something I found', 'Looking for the owner of something I found')], max_length=255)),
                ('Title', models.TextField(blank=True, max_length=500, null=True)),
                ('description', models.TextField(blank=True, max_length=2000, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s', to='setting.category')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='contenttypes.contenttype')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_messages', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OtherItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, choices=[('Addis Ababa', 'Addis Ababa'), ('Diredawa', 'Diredawa'), ('Sheger', 'Sheger'), ('Amhara Region', 'Amhara Region'), ('Tigray Region', 'Tigray Region'), ('Oromia Region', 'Oromia Region'), ('Southern Ethiopia', 'Southern Ethiopia'), ('Afar Region', 'Afar Region'), ('Somali Region', 'Somali Region'), ('Gurage', 'Gurage'), ('Silte Zone', 'Silte Zone')], max_length=50, null=True)),
                ('approvalStatus', models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Approved', 'Approved')], default='Pending', max_length=50, null=True)),
                ('paymentStatus', models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Paid', 'Paid')], default='Pending', max_length=50, null=True)),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, help_text='Latitude of the location', max_digits=9, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, help_text='Longitude of the location', max_digits=9, null=True)),
                ('phonenumber', models.CharField(blank=True, max_length=50, null=True)),
                ('removed', models.BooleanField(default=False)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('sell_or_rent', models.CharField(blank=True, choices=[('Sale', 'Sale'), ('Rent', 'Rent')], max_length=50, null=True)),
                ('title', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=50, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField(blank=True, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s', to='setting.category')),
                ('otherItemcategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='OtherItems', to='setting.otheritemcategory')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ServiceFee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('feeReciptImage', models.ImageField(blank=True, default='payment.jpg', null=True, upload_to='Servicefee_images/')),
                ('feeReciptRefnumber', models.CharField(blank=True, max_length=100, null=True)),
                ('contentType', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('servicefeeBank', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s', to='setting.customerbank')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceOrBusinessType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(blank=True, choices=[('Addis Ababa', 'Addis Ababa'), ('Diredawa', 'Diredawa'), ('Sheger', 'Sheger'), ('Amhara Region', 'Amhara Region'), ('Tigray Region', 'Tigray Region'), ('Oromia Region', 'Oromia Region'), ('Southern Ethiopia', 'Southern Ethiopia'), ('Afar Region', 'Afar Region'), ('Somali Region', 'Somali Region'), ('Gurage', 'Gurage'), ('Silte Zone', 'Silte Zone')], max_length=50, null=True)),
                ('approvalStatus', models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Approved', 'Approved')], default='Pending', max_length=50, null=True)),
                ('paymentStatus', models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Paid', 'Paid')], default='Pending', max_length=50, null=True)),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, help_text='Latitude of the location', max_digits=9, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, help_text='Longitude of the location', max_digits=9, null=True)),
                ('phonenumber', models.CharField(blank=True, max_length=50, null=True)),
                ('removed', models.BooleanField(default=False)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('businessLocation', models.TextField(blank=True, max_length=500, null=True)),
                ('Title', models.TextField(blank=True, max_length=500, null=True)),
                ('payment', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField(blank=True, max_length=2000, null=True)),
                ('busienssOrServiceType', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ServiceOrBusinesstype', to='setting.busienssorservicetype')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s', to='setting.category')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('objectId', models.PositiveIntegerField()),
                ('removed', models.BooleanField(default=False)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('contentType', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watchlists', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

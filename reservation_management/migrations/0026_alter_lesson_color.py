# Generated by Django 3.2.7 on 2021-11-20 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation_management', '0025_alter_lesson_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='color',
            field=models.CharField(choices=[('#FF5964', 'Red'), ('#69DC9E', 'Green'), ('#0075A2', 'Blue'), ('#333333', 'Black'), ('#FF9F1C', 'Orange'), ('#694F5D', 'Eggplant'), ('#3D3A4B', 'Grey'), ('#849483', 'Olive'), ('#B388EB', 'Purple'), ('#823329', 'Burnt umber')], default='#FF5964', max_length=7),
        ),
    ]

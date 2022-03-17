# Generated by Django 4.0.3 on 2022-03-15 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
        ('companies', '0002_tag_rename_name_company_title_company_creator_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='creator',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
        migrations.AddField(
            model_name='case',
            name='tags',
            field=models.ManyToManyField(related_name='case_tags', to='content.tag'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='likes',
            field=models.ManyToManyField(related_name='comment_likes', to='content.like'),
        ),
        migrations.DeleteModel(
            name='Like',
        ),
    ]
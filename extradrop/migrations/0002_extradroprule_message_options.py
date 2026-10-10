from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extradrop', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='extradroprule',
            options={'verbose_name': 'Extra drop', 'verbose_name_plural': 'Extra drops'},
        ),
        migrations.AddField(
            model_name='extradroprule',
            name='message_title',
            field=models.CharField(blank=True, default='{ball} dropped something!', help_text="Title of the announcement embed. Placeholders: {ball} = the caught ball, {drop} = the dropped ball, {user} = the player's name. Leave blank to use the default.", max_length=256),
        ),
        migrations.AddField(
            model_name='extradroprule',
            name='message_description',
            field=models.TextField(blank=True, default='You have obtained a {drop}.', help_text='Description of the announcement embed. Same placeholders as the title: {ball}, {drop}, {user}. Leave blank to use the default.', max_length=4096),
        ),
    ]
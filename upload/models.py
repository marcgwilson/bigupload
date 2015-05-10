from django.db import models
from os.path import relpath

# Create your models here.
class Item(models.Model):
    data = models.FileField(upload_to='data')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)

    def __unicode__(self):
        return 'item created on %s' % (self.created)

    def to_dict(self):
        return {'id': self.id, 'data': relpath(self.data.url, '/media/'), 'created': str(self.created) }

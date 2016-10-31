from django.contrib.contenttypes.fields import GenericRelation
from django.core.urlresolvers import reverse
from django.db import models

from extras.models import CustomFieldModel, CustomFieldValue
from utilities.models import CreatedUpdatedModel


class TenantGroup(models.Model):
    """
    An arbitrary collection of Tenants.
    """
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "{}?group={}".format(reverse('tenancy:tenant_list'), self.slug)


class Tenant(CreatedUpdatedModel, CustomFieldModel):
    """
    A Tenant represents an organization served by the NetBox owner. This is typically a customer or an internal
    department.
    """
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(unique=True)
    group = models.ForeignKey('TenantGroup', related_name='tenants', blank=True, null=True, on_delete=models.SET_NULL)
    description = models.CharField(max_length=100, blank=True, help_text="Long-form name (optional)")
    comments = models.TextField(blank=True)
    custom_field_values = GenericRelation(CustomFieldValue, content_type_field='obj_type', object_id_field='obj_id')

    class Meta:
        ordering = ['group', 'name']

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tenancy:tenant', args=[self.slug])

    def to_csv(self):
        return ','.join([
            self.name,
            self.slug,
            self.group.name,
            self.description,
        ])

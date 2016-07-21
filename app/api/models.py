from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from django.db import models
from django.contrib.auth.models import AbstractUser
from constants import *

class User(AbstractUser):
    container_limit = models.IntegerField(verbose_name=_("Container Limit"), help_text=_("The total number of containers the user may have"), default=10)
    floating_ip_limit = models.IntegerField(verbose_name=_("Floating IP Limit"), help_text=_("The total number of floating IPs the user may have"), default=3)

class Resource(models.Model):
    key = models.IntegerField(verbose_name=_("Key"), help_text=_("The key (id) of the resource."))
    value = models.CharField(verbose_name=_("Value"), help_text=_("The value for the resource (f.e. the type of the resource)"), max_length=80)

class Tag(models.Model):
    name = models.CharField(verbose_name=_("Name"), help_text=_("The name of the tag. The supported characters for names include alphanumeric characters, dashes, and underscores."), max_length=80)
    resources = models.ManyToManyField(Resource, verbose_name=_("Resources"), help_text=_("The resource associated with this tag."))

class Feature(models.Model):
    feature = models.CharField(verbose_name=_("Feature"), help_text=_("A feature (f.e. if a Container can be backed up)"), max_length=20)

class Size(models.Model):
    slug = models.CharField(verbose_name=_("Slug"), help_text=_("A human-readable string that is used to uniquely identify each size."), max_length=10)
    available = models.BooleanField(verbose_name=_("Available"), help_text=_("This is a boolean value that represents whether new Containers can be created with this size."))
    transfer = models.DecimalField(verbose_name=_("Bandwith"), help_text=_("The amount of transfer bandwidth that is available for Containers created in this size. This only counts traffic on the public interface. The value is given in terabytes."), decimal_places=1, max_digits=6)
    price_monthly = models.DecimalField(verbose_name=_("Price Monthly"), help_text=_("This attribute describes the monthly cost of this Container size if the Container is kept for an entire month."), decimal_places=1, max_digits=5)
    price_hourly = models.DecimalField(verbose_name=_("Price Hourly"), help_text=_("This describes the price of the Container size as measured hourly."), decimal_places=1, max_digits=8)
    memory = models.IntegerField(verbose_name=_("Memory"), help_text=_("The amount of RAM allocated to Containers created of this size. The value is represented in megabytes."))
    vcpus = models.IntegerField(verbose_name=_("CPUs"), help_text=_("The number of virtual CPUs allocated to Containers of this size."))
    disk = models.IntegerField(verbose_name=_("Disk"), help_text=_("The amount of disk space set aside for Containers of this size. The value is represented in gigabytes."))

class BackupWindow(models.Model):
    start = models.DateTimeField(verbose_name=_("Start"), help_text=_("A time value given in ISO8601 combined date and time format that represents when the backup will start."))
    end = models.DateTimeField(verbose_name=_("End"), help_text=_("A time value given in ISO8601 combined date and time format that represents when the backup will end."))

class Region(models.Model):
    name = models.CharField(verbose_name=_("Name"), help_text=_("The display name of the region. This will be a full name that is used in the control panel and other interfaces."), max_length=20)
    slug = models.CharField(verbose_name=_("Slug"), help_text=_("A human-readable string that is used as a unique identifier for each region."), max_length=4)
    sizes = models.ManyToManyField(Size, verbose_name=_("Sizes"), help_text=_("The sizes available in this region."))
    available = models.BooleanField(verbose_name=_("Available"), help_text=_("This is a boolean value that represents whether new Containers can be created in this region."))
    features = models.ManyToManyField(Feature, verbose_name=_("Features"), help_text=_("The features available in this region."))

class Action(models.Model):
    status = models.IntegerField(verbose_name=_("Status"), help_text=_("The current status of the action."))
    type = models.CharField(verbose_name=_("Type"), help_text=_("This is the type of action that the object represents. For example, this could be \"transfer\" to represent the state of an image transfer action."), max_length=20)
    started_at = models.DateTimeField(verbose_name=_("Started At"), help_text=_("A time value given in ISO8601 combined date and time format that represents when the action was initiated."))
    completed_at = models.DateTimeField(verbose_name=_("Completed At"), help_text=_("A time value given in ISO8601 combined date and time format that represents when the action was completed."))
    resource = models.OneToOneField(Resource, verbose_name=_("Resource"), help_text=_("The resource that the action is associated with."))
    region = models.ForeignKey(Region, verbose_name=_("Region"), help_text=_("The region where the action occurred."))

class Domain(models.Model):
    name = models.CharField(verbose_name=_("Name"), help_text=_("The name of the domain itself. This should follow the standard domain format of domain.TLD. For instance, example.com is a valid domain name."), max_length=60)
    ttl = models.IntegerField(verbose_name=_("TTL"), help_text=_("This value is the time to live for the records on this domain, in seconds. This defines the time frame that clients can cache queried information before a refresh should be requested."))
    zone_file = models.TextField(verbose_name=_("Zone File"), help_text=_("This attribute contains the complete contents of the zone file for the selected domain. Individual domain record resources should be used to get more granular control over records. However, this attribute can also be used to get information about the SOA record, which is created automatically and is not accessible as an individual record resource."))

class DomainRecord(models.Model):
    name = models.CharField(verbose_name=_("Name"), help_text=_("The name to use for the DNS record."), max_length=60)
    type = models.IntegerField(verbose_name=_("Type"), help_text=_("The type of the DNS record (ex: A, CNAME, TXT, ...)."), choices=DOMAIN_RECORD_TYPES)
    data = models.CharField(verbose_name=_("Value"), help_text=_("The value to use for the DNS record."), max_length=60)
    priority = models.IntegerField(verbose_name=_("Priority"), help_text=_("The priority for SRV and MX records."), null=True)
    port = models.IntegerField(verbose_name=_("Port"), help_text=_("The port for SRV records."), null=True)
    weight = models.IntegerField(verbose_name=_("Weight"), help_text=_("The weight for SRV records."), null=True)

class Network(models.Model):
    version = models.IntegerField(verbose_name=_("Version"), help_text=_("The version of the network (can be v4 or v6)"), choices=NETWORK_VERSIONS)
    netmask = models.CharField(verbose_name=_("Netmaks"), help_text=_("The netmask of the network."), max_length=45)
    gateway = models.CharField(verbose_name=_("Gateway"), help_text=_("The gateway of the network."), max_length=45)
    type = models.IntegerField(verbose_name=_("Type"), help_text=_("The type of the network (can be public or private)"), choices=NETWORK_TYPES)

class Kernel(models.Model):
    name = models.CharField(verbose_name=_("Name"), help_text=_("The name of the kernel."), max_length=100)
    version = models.CharField(verbose_name=_("Version"), help_text=_("The version of the kernel."), max_length=100)

class SSHKey(models.Model):
    name = models.CharField(verbose_name=_("Name"), help_text=_("This is the human-readable display name for the given SSH key. This is used to easily identify the SSH keys when they are displayed."), max_length=60)
    fingerprint = models.CharField(verbose_name=_("Fingerprint"), help_text=_("This attribute contains the fingerprint value that is generated from the public key. This is a unique identifier that will differentiate it from other keys using a format that SSH recognizes."), max_length=512)
    public_key = models.TextField(verbose_name=_("Public Key"), help_text=_("This attribute contains the entire public key string that was uploaded. This is what is embedded into the root user's authorized_keys file if you choose to include this SSH key during Container creation."))

class Image(models.Model):
    name = models.CharField(verbose_name=_("Name"), help_text=_("The display name that has been given to an image. This is what is shown in the control panel and is generally a descriptive title for the image in question."), max_length=60)
    type = models.IntegerField(verbose_name=_("Type"), help_text=_("The kind of image, describing the duration of how long the image is stored. This is either \"snapshot\" or \"backup\"."), choices=IMAGE_TYPES)
    distribution = models.CharField(verbose_name=_("Distribution"), help_text=_("This attribute describes the base distribution used for this image."), max_length=100)
    slug = models.CharField(verbose_name=_("Slug"), help_text=_("A uniquely identifying string that is associated with each of the provided public images. These can be used to reference a public image as an alternative to the numeric id."), max_length=100)
    public = models.BooleanField(verbose_name=_("Public"), help_text=_("This is a boolean value that indicates whether the image in question is public or not. An image that is public is available to all accounts. A non-public image is only accessible from your account."))
    regions = models.ManyToManyField(Region, verbose_name=_("Regions"), help_text=_("This attribute is an array of the regions that the image is available in."))
    min_disk_size = models.IntegerField(verbose_name=_("Minimum Disk Size"), help_text=_("The minimum 'disk' required for a size to use this image."))
    size_gigabytes = models.IntegerField(verbose_name=_("Size"), help_text=_("The size of the image in gigabytes."))
    created_at = models.DateTimeField(verbose_name=_("Created At"), help_text=_("A time value given in ISO8601 combined date and time format that represents when the Image was created."))

class Storage(models.Model):
    name = models.CharField(verbose_name=_("Name"), help_text=_("A human-readable name for the Storage volume. Must be lowercase and be composed only of numbers, letters and \"-\", up to a limit of 64 characters."), max_length=64)
    region = models.ForeignKey(Region, verbose_name=_("Region"), help_text=_("The region that the Storage volume is located in."))
    containers = models.ForeignKey('Container', verbose_name=_("Containers"), help_text=_("The Containers the volume is attached to."))
    description = models.CharField(verbose_name=_("Description"), help_text=_("An optional free-form text field to describe a Storage volume."), max_length=120)
    size_gigabytes = models.IntegerField(verbose_name=_("Size"), help_text=_("The size of the Storage volume in GiB (1024^3)."))
    created_at = models.DateTimeField(verbose_name=_("Created At"), help_text=_("A time value given in ISO8601 combined date and time format that represents when the Storage volume was created."))

class Container(models.Model):
    name = models.CharField(verbose_name=_("Name"), help_text=_("The human-readable name set for the Container instance."), max_length=60)
    memory = models.IntegerField(verbose_name=_("Memory"), help_text=_("Memory of the Container in megabytes."))
    vcpus = models.IntegerField(verbose_name=_("CPUs"), help_text=_("The number of virtual CPUs."))
    disk = models.IntegerField(verbose_name=_("Disk"), help_text=_("The size of the Container's disk in gigabytes."))
    locked = models.BooleanField(verbose_name=_("Locked"), help_text=_("A boolean value indicating whether the Container has been locked, preventing actions by users."))
    created_at = models.DateTimeField(verbose_name=_("Created At"), help_text=_("A time value given in ISO8601 combined date and time format that represents when the Container was created."))
    status = models.IntegerField(verbose_name=_("Status"), help_text=_("A status string indicating the state of the Droplet instance. This may be \"new\", \"active\", \"off\", or \"archive\"."), choices=CONTAINER_STATUSES)
    images = models.ManyToManyField(Image, verbose_name=_("Images"), help_text=_("A collection of the backups and shapshots associated with this Container."), related_name='images')
    features = models.ForeignKey(Feature, verbose_name=_("Features"), help_text=_("A collection of features enabled on this Container."))
    region = models.ForeignKey(Region, verbose_name=_("Region"), help_text=_("The region that the Container instance is deployed in."))
    base_image = models.ForeignKey(Image, verbose_name=_("Base Image"), help_text=_("The base image used to create the Container instance."), related_name='base_image')
    size = models.ForeignKey(Size, verbose_name=_("Size"), help_text=_("The current size object describing the Container."))
    networks = models.ManyToManyField(Network, verbose_name=_("Networks"), help_text=_("The details of the network that are configured for the Container instance."))
    kernel = models.ForeignKey(Kernel, verbose_name=_("Kernel"), help_text=_("The current kernel. This will initially be set to the kernel of the base image when the Container is created."), null=True)
    next_backup_window = models.OneToOneField(BackupWindow, verbose_name=_("Next Backup Window"), help_text=_("The details of the Container's backups feature, if backups are configured for the Container."), null=True)
    tags = models.ManyToManyField(Tag, verbose_name=_("Tags"), help_text=_("A collection of Tags the Container has been tagged with."))
    volumes = models.ManyToManyField(Storage, verbose_name=_("Volumes"), help_text=_("A collection containing each Storage volume attached to the Container."))

class FloatingIP(models.Model):
    ip = models.CharField(verbose_name=_("IP"), help_text=_("The public IP address of the Floating IP. It also serves as its identifier."), max_length=45)
    region = models.ForeignKey(Region, verbose_name=_("Region"), help_text=_("The region that the Floating IP is reserved to. When you query a Floating IP, the entire region object will be returned."))
    container = models.ForeignKey(Container, verbose_name=_("Container"), help_text=_("The Container that the Floating IP has been assigned to."))

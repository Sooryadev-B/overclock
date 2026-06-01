from django.conf import settings
from django.db import models
from django.urls import reverse


class Category(models.Model):
    """Product category (prebuilt, gpu, cpu, ram, storage, etc.)"""
    CATEGORY_CHOICES = [
        ('prebuilt', 'Prebuilt Gaming Rig'),
        ('gpu', 'Graphics Card (GPU)'),
        ('cpu', 'Processor (CPU)'),
        ('ram', 'System Memory (RAM)'),
        ('storage', 'Storage (SSD/HDD)'),
        ('cooler', 'CPU Cooler'),
        ('psu', 'Power Supply Unit'),
        ('case', 'PC Case'),
        ('mobo', 'Motherboard'),
        ('peripheral', 'Peripheral'),
    ]
    id_key = models.SlugField(
        max_length=50, unique=True, primary_key=True,
        help_text="Internal category key, e.g. 'gpu', 'cpu', 'prebuilt'"
    )
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    """A shop product — prebuilt system, GPU, CPU, RAM, etc."""

    # Core identity
    name = models.CharField(max_length=200, help_text="Full product name shown on the storefront")
    slug = models.SlugField(max_length=200, unique=True, help_text="URL-friendly identifier, e.g. nemesis-rtx-5090-edition")
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name='products',
        help_text="Select the product category"
    )
    description = models.TextField(help_text="Full product description shown on detail page")

    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Current selling price in USD")
    old_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
        help_text="Original price (leave blank if no discount)"
    )

    # Media
    image = models.CharField(
        max_length=100, blank=True,
        help_text="Static image filename without extension, e.g. 'nemesis_rtx_5090_edition'"
    )
    image_upload = models.ImageField(
        upload_to='products/', null=True, blank=True,
        help_text="Upload a product image (overrides the static image name above)"
    )

    # Badges & marketing
    badge = models.CharField(
        max_length=50, blank=True,
        help_text="Short badge label shown on the card, e.g. 'FLAGSHIP', 'NEW', 'HOT'"
    )

    # Ratings & reviews
    rating = models.DecimalField(
        max_digits=3, decimal_places=1, default=0.0,
        help_text="Average rating out of 5.0"
    )
    reviews_count = models.PositiveIntegerField(default=0)

    # Inventory
    stock = models.PositiveIntegerField(default=0, help_text="Current units in stock")
    in_stock = models.BooleanField(default=True, help_text="Toggle product availability")

    # Key hardware specs (used on product cards & detail page)
    cpu = models.CharField(max_length=200, blank=True, help_text="Processor / CPU spec line")
    gpu = models.CharField(max_length=200, blank=True, help_text="Graphics card / GPU spec line")
    ram = models.CharField(max_length=200, blank=True, help_text="Memory / RAM spec line")
    storage = models.CharField(max_length=200, blank=True, help_text="Storage spec line")
    mobo = models.CharField(max_length=200, blank=True, help_text="Motherboard spec line")
    psu = models.CharField(max_length=200, blank=True, help_text="Power supply spec line")
    cooler = models.CharField(max_length=200, blank=True, help_text="Cooler spec line")
    case = models.CharField(max_length=200, blank=True, help_text="Case spec line")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False, help_text="Show in homepage featured section")
    is_trending = models.BooleanField(default=False, help_text="Show in homepage trending section")

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-is_featured', '-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', kwargs={'slug': self.slug})


class Review(models.Model):
    """Customer product review."""

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='reviews'
    )
    author_name = models.CharField(max_length=100)
    rating = models.PositiveSmallIntegerField(help_text='Rating from 1 to 5')
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} — {self.product.name}'


class Feedback(models.Model):
    """General site feedback / support messages."""

    STATUS_CHOICES = [
        ('new', 'New'),
        ('read', 'Read'),
        ('resolved', 'Resolved'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='feedbacks'
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.subject} ({self.name})'

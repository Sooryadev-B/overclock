from django.contrib import admin
from .models import Category, Product, Review, Feedback


# ─── Category Admin ─────────────────────────────────────────────────────────

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id_key', 'name', 'product_count')
    search_fields = ('id_key', 'name')
    prepopulated_fields = {}

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Products'


# ─── Product Admin ────────────────────────────────────────────────────────────

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'category', 'price', 'old_price',
        'stock', 'in_stock', 'rating', 'is_featured', 'is_trending', 'updated_at'
    )
    list_filter = ('category', 'in_stock', 'is_featured', 'is_trending')
    search_fields = ('name', 'slug', 'description', 'cpu', 'gpu')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('price', 'stock', 'in_stock', 'is_featured', 'is_trending')
    list_per_page = 20
    save_on_top = True

    fieldsets = (
        ('🖥️ Core Info', {
            'fields': ('name', 'slug', 'category', 'description', 'badge'),
        }),
        ('💰 Pricing & Inventory', {
            'fields': ('price', 'old_price', 'stock', 'in_stock'),
        }),
        ('🖼️ Media', {
            'fields': ('image', 'image_upload'),
            'description': 'Use "image" to reference an existing static file by name, OR upload a new image.'
        }),
        ('⭐ Ratings', {
            'fields': ('rating', 'reviews_count'),
        }),
        ('🔧 Hardware Specifications', {
            'fields': ('cpu', 'gpu', 'ram', 'storage', 'mobo', 'psu', 'cooler', 'case'),
            'classes': ('collapse',),
        }),
        ('🏠 Homepage Display', {
            'fields': ('is_featured', 'is_trending'),
        }),
        ('📅 Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'product', 'author_name', 'rating', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'rating')
    search_fields = ('title', 'author_name', 'content')


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('subject', 'name', 'email', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('subject', 'name', 'email', 'message')

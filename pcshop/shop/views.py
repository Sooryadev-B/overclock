from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category, Review, Feedback

# Comprehensive Mock Database for the Gaming PC Store
PRODUCTS = {
    'nemesis-rtx-5090-edition': {
        'name': 'Nemesis RTX 5090 Edition',
        'slug': 'nemesis-rtx-5090-edition',
        'category': 'prebuilt',
        'price': 4999.99,
        'old_price': 5299.99,
        'image': 'nemesis_rtx_5090_edition', # image name for template
        'badge': 'FLAGSHIP',
        'rating': 4.9,
        'reviews_count': 142,
        'stock': 8,
        'in_stock': True,
        'description': 'The ultimate gaming powerhouse. Engineered for enthusiasts who demand the absolute best in rendering, ray tracing, and frame rates. Featuring custom hardline liquid cooling and premium components wrapped in a matte black glass chassis.',
        'cpu': 'Intel Core i9-14900KS (6.2 GHz 24-Core)',
        'gpu': 'NVIDIA GeForce RTX 5090 24GB GDDR7',
        'ram': '64GB Corsair Dominator Titanium DDR5 6400MHz',
        'storage': '4TB Crucial T700 Gen5 NVMe SSD (12,400 MB/s)',
        'mobo': 'ASUS ROG Maximus Z790 Hero',
        'psu': 'ASUS ROG Thor 1200W Platinum II OLED',
        'cooler': 'Custom Hardline Open Loop Liquid Cooling',
        'case': 'HYTE Y70 Touch Infinite (Integrated Screen)',
        'gallery': ['nemesis_rtx_5090_edition', 'pc_gallery_1', 'pc_gallery_2'],
        'specs_table': {
            'Processor': 'Intel Core i9-14900KS 24-Core / 32-Thread',
            'Graphics': 'NVIDIA GeForce RTX 5090 24GB GDDR7',
            'Memory': '64GB (2x32GB) DDR5 Corsair Dominator Titanium 6400MHz Cl32',
            'Storage': '4TB Crucial T700 Gen5 PCIe NVMe M.2 SSD',
            'Motherboard': 'ASUS ROG Maximus Z790 Hero WiFi',
            'Power Supply': '1200W ASUS ROG Thor Platinum II (ATX 3.0 Ready)',
            'Chassis': 'HYTE Y70 Touch Black Dual Chamber Glass Case',
            'Cooling': 'Full Custom Loop with EK Water Blocks & Corsair Fans',
            'OS': 'Windows 11 Pro (Activated & Optimized)'
        }
    },
    'apex-horizon-ryzen-9': {
        'name': 'Apex Horizon Ryzen 9',
        'slug': 'apex-horizon-ryzen-9',
        'category': 'prebuilt',
        'price': 3799.99,
        'old_price': None,
        'image': 'apex_horizon_ryzen_9',
        'badge': 'POPULAR',
        'rating': 4.8,
        'reviews_count': 98,
        'stock': 15,
        'in_stock': True,
        'description': 'Designed for elite gamers and streamers. Leveraging AMD\'s revolutionary 3D V-Cache technology to maximize gaming performance while keeping temperatures and power consumption balanced.',
        'cpu': 'AMD Ryzen 9 7950X3D (16-Core, 3D V-Cache)',
        'gpu': 'NVIDIA GeForce RTX 4090 24GB GDDR6X',
        'ram': '32GB G.Skill Trident Z5 Neo RGB DDR5 6000MHz',
        'storage': '2TB Samsung 990 Pro PCIe 4.0 NVMe SSD',
        'mobo': 'MSI MAG X670E Tomahawk WiFi',
        'psu': 'Corsair RM1000x 1000W 80+ Gold PCIe 5.0',
        'cooler': 'NZXT Kraken Elite 360 RGB AIO Cooler',
        'case': 'Lian Li O11 Dynamic EVO XL RGB Black',
        'gallery': ['apex_horizon_ryzen_9', 'pc_gallery_1', 'pc_gallery_2'],
        'specs_table': {
            'Processor': 'AMD Ryzen 9 7950X3D 16-Core / 32-Thread with 3D V-Cache',
            'Graphics': 'NVIDIA GeForce RTX 4090 24GB GDDR6X',
            'Memory': '32GB (2x16GB) G.Skill Trident Z5 Neo RGB DDR5 6000MHz CL30',
            'Storage': '2TB Samsung 990 Pro Gen4 PCIe NVMe M.2 SSD',
            'Motherboard': 'MSI MAG X670E Tomahawk WiFi',
            'Power Supply': '1000W Corsair RM1000x Shift ATX 3.0 Gold',
            'Chassis': 'Lian Li O11 Dynamic EVO XL Glass Mid-Tower Case',
            'Cooling': 'NZXT Kraken Elite 360mm LCD Liquid Cooler',
            'OS': 'Windows 11 Home (Optimized)'
        }
    },
    'valkyrie-whiteout-edition': {
        'name': 'Valkyrie Whiteout Edition',
        'slug': 'valkyrie-whiteout-edition',
        'category': 'prebuilt',
        'price': 2899.99,
        'old_price': 2999.99,
        'image': 'valkyrie_whiteout_edition',
        'badge': 'WHITE OUT',
        'rating': 4.7,
        'reviews_count': 64,
        'stock': 5,
        'in_stock': True,
        'description': 'A visually stunning all-white build with neon cyan aesthetics. Features elite-tier 1440p and 4K gaming power, customizable RGB lighting, and custom white braided cables.',
        'cpu': 'AMD Ryzen 7 7800X3D (8-Core 3D V-Cache)',
        'gpu': 'NVIDIA GeForce RTX 4080 Super 16GB White',
        'ram': '32GB Teamgroup T-Force Delta RGB DDR5 6000MHz White',
        'storage': '2TB WD Black SN850X NVMe M.2 SSD',
        'mobo': 'ASUS ROG Strix B650-A Gaming WiFi White',
        'psu': 'Seasonic Focus GX-850 850W White Gold',
        'cooler': 'Lian Li Galahad II LCD Trinity 360 White',
        'case': 'NZXT H9 Elite Flow White',
        'gallery': ['valkyrie_whiteout_edition', 'pc_gallery_3', 'pc_gallery_4'],
        'specs_table': {
            'Processor': 'AMD Ryzen 7 7800X3D 8-Core Gaming King',
            'Graphics': 'NVIDIA GeForce RTX 4080 Super 16GB GDDR6X White Edition',
            'Memory': '32GB (2x16GB) T-Force Delta RGB DDR5 6000MHz White CL30',
            'Storage': '2TB WD Black SN850X Gen4 PCIe NVMe SSD',
            'Motherboard': 'ASUS ROG Strix B650-A Gaming WiFi White',
            'Power Supply': '850W Seasonic Focus GX-850 White 80+ Gold',
            'Chassis': 'NZXT H9 Elite Dual-Chamber Glass Case White',
            'Cooling': 'Lian Li Galahad II LCD Trinity 360mm White AIO Cooler',
            'OS': 'Windows 11 Home'
        }
    },
    'rift-breaker-intel-i7': {
        'name': 'Rift Breaker Intel i7',
        'slug': 'rift-breaker-intel-i7',
        'category': 'prebuilt',
        'price': 1999.99,
        'old_price': None,
        'image': 'rift_breaker_intel_i7',
        'badge': 'VALUED VALUE',
        'rating': 4.6,
        'reviews_count': 112,
        'stock': 0,
        'in_stock': False,
        'description': 'The sweet-spot gaming rig. Ready to tear through AAA titles at high settings. Perfect entry into professional ray tracing and gaming at 1440p high frame-rates.',
        'cpu': 'Intel Core i7-14700K (5.6 GHz 20-Core)',
        'gpu': 'NVIDIA GeForce RTX 4070 Ti Super 16GB',
        'ram': '32GB G.Skill Ripjaws S5 DDR5 5600MHz',
        'storage': '1TB Kingston KC3000 PCIe 4.0 NVMe SSD',
        'mobo': 'ASRock Z790 Pro RS WiFi',
        'psu': 'Corsair RM850e 850W Gold ATX 3.0',
        'cooler': 'DeepCool LT720 360mm Liquid Cooler',
        'case': 'Phanteks NV5 Mid-Tower Black',
        'gallery': ['rift_breaker_intel_i7', 'pc_gallery_1', 'pc_gallery_2'],
        'specs_table': {
            'Processor': 'Intel Core i7-14700K 20-Core / 28-Thread',
            'Graphics': 'NVIDIA GeForce RTX 4070 Ti Super 16GB GDDR6X',
            'Memory': '32GB (2x16GB) G.Skill Ripjaws S5 DDR5 5600MHz',
            'Storage': '1TB Kingston KC3000 Gen4 PCIe M.2 SSD',
            'Motherboard': 'ASRock Z790 Pro RS WiFi',
            'Power Supply': '850W Corsair RM850e 80+ Gold Modular',
            'Chassis': 'Phanteks NV5 Panoramic Glass Case Black',
            'Cooling': 'DeepCool LT720 360mm AIO Liquid Cooler',
            'OS': 'Windows 11 Home'
        }
    },
    'nvidia-rtx-5090-gpu': {
        'name': 'NVIDIA GeForce RTX 5090 Founders Edition',
        'slug': 'nvidia-rtx-5090-gpu',
        'category': 'gpu',
        'price': 1999.99,
        'old_price': None,
        'image': 'nvidia_rtx_5090_gpu',
        'badge': 'NEW',
        'rating': 5.0,
        'reviews_count': 18,
        'stock': 3,
        'in_stock': True,
        'description': 'The next frontier of GPU hardware. Utilizing the Blackwell architecture, featuring 24GB GDDR7 VRAM, and AI-accelerated DLSS 4 frame generation. The fastest graphics card on earth.',
        'cpu': 'Compatible with PCIe Gen 5.0 Slots',
        'gpu': '24GB GDDR7, Blackwell GPU Architecture',
        'ram': 'Recommends 850W+ ATX 3.0 PSU',
        'storage': 'DirectStorage 1.2 Compatible',
        'mobo': 'PCI Express 5.0 x16 interface',
        'psu': 'Requires 16-pin 12V2x6 Cable',
        'cooler': 'Founders Edition Tri-Slot Dual Axial Fan',
        'case': 'Length: 336mm, Width: 142mm',
        'gallery': ['nvidia_rtx_5090_gpu'],
        'specs_table': {
            'GPU Architecture': 'NVIDIA Blackwell',
            'VRAM Capacity': '24GB GDDR7',
            'Memory Interface': '512-bit',
            'CUDA Cores': '21,760',
            'Interface': 'PCI Express 5.0 x16',
            'Recommended PSU': '850W Minimum (ATX 3.0)',
            'Power Connector': '1x 16-pin (12V2x6)'
        }
    },
    'intel-i9-14900ks-cpu': {
        'name': 'Intel Core i9-14900KS Processor',
        'slug': 'intel-i9-14900ks-cpu',
        'category': 'cpu',
        'price': 689.99,
        'old_price': 729.99,
        'image': 'intel_i9_14900ks_cpu',
        'badge': 'HOT',
        'rating': 4.7,
        'reviews_count': 53,
        'stock': 12,
        'in_stock': True,
        'description': 'Unleash extreme speeds with the special edition desktop processor reaching up to 6.2 GHz out of the box. Featuring 24 cores and 32 threads, it is optimized for high-end desktop workflows.',
        'cpu': 'LGA 1700 Socket Compatibility',
        'gpu': 'Intel UHD Graphics 770 Integrated',
        'ram': 'Supports DDR5 (5600+) & DDR4',
        'storage': 'Up to 20 PCIe Lanes',
        'mobo': 'Z790 / Z690 Intel Motherboards',
        'psu': 'Base Power: 150W, Turbo: 253W+',
        'cooler': 'High-performance AIO or custom loop required',
        'case': 'Compatible with standard socket coolers',
        'gallery': ['intel_i9_14900ks_cpu'],
        'specs_table': {
            'Socket': 'LGA1700',
            'P-Cores': '8 (Base 3.2GHz, Turbo 6.2GHz)',
            'E-Cores': '16 (Base 2.4GHz, Turbo 4.5GHz)',
            'Total Cores / Threads': '24 Cores / 32 Threads',
            'L3 Cache': '36MB Intel Smart Cache',
            'TDP': '150W Base / 253W Max'
        }
    },
    'corsair-dominator-titanium-ram': {
        'name': 'Corsair Dominator Titanium 64GB DDR5 6400MHz',
        'slug': 'corsair-dominator-titanium-ram',
        'category': 'ram',
        'price': 299.99,
        'old_price': None,
        'image': 'corsair_dominator_titanium_ram',
        'badge': 'PREMIUM',
        'rating': 4.9,
        'reviews_count': 32,
        'stock': 24,
        'in_stock': True,
        'description': 'Elite DDR5 memory combining clean style, advanced forged aluminum construction, and glowing custom RGB lighting. Tuned for extreme Intel and AMD overclocking profile optimizations.',
        'cpu': 'XMP 3.0 & EXPO Ready',
        'gpu': 'N/A',
        'ram': '2x32GB modules, CL32 latency, 1.4V',
        'storage': 'DHX Cooling Technology',
        'mobo': 'DDR5 Supporting Motherboards',
        'psu': 'N/A',
        'cooler': 'Low profile modules compatibility',
        'case': 'Height: 55mm with lightbars',
        'gallery': ['corsair_dominator_titanium_ram'],
        'specs_table': {
            'Memory Type': 'DDR5 SDRAM',
            'Total Capacity': '64GB (2 x 32GB)',
            'Tested Speed': '6400 MHz',
            'Tested Latency': '32-40-40-84 (CL32)',
            'Tested Voltage': '1.40V',
            'RGB Lighting': 'Customizable via Corsair iCUE'
        }
    }
}

CATEGORIES = [
    {'id': 'all', 'name': 'All Products', 'count': len(PRODUCTS)},
    {'id': 'prebuilt', 'name': 'Prebuilt Rigs', 'count': 4},
    {'id': 'gpu', 'name': 'Graphics Cards', 'count': 1},
    {'id': 'cpu', 'name': 'Processors (CPU)', 'count': 1},
    {'id': 'ram', 'name': 'System Memory (RAM)', 'count': 1},
]

# PC Builder parts database for JSON-like configurations
BUILDER_PARTS = {
    'cpu': [
        {'id': 'cpu1', 'name': 'Intel Core i9-14900KS', 'price': 689.99, 'wattage': 150, 'socket': 'LGA1700', 'badge': 'Extreme'},
        {'id': 'cpu2', 'name': 'AMD Ryzen 7 7800X3D', 'price': 399.99, 'wattage': 120, 'socket': 'AM5', 'badge': 'Gaming King'},
        {'id': 'cpu3', 'name': 'Intel Core i7-14700K', 'price': 369.99, 'wattage': 125, 'socket': 'LGA1700', 'badge': 'Sweet Spot'},
        {'id': 'cpu4', 'name': 'AMD Ryzen 9 7950X3D', 'price': 599.99, 'wattage': 120, 'socket': 'AM5', 'badge': 'Productivity'}
    ],
    'mobo': [
        {'id': 'mobo1', 'name': 'ASUS ROG Maximus Z790 Hero', 'price': 629.99, 'wattage': 60, 'socket': 'LGA1700', 'badge': 'Enthusiast'},
        {'id': 'mobo2', 'name': 'MSI MAG X670E Tomahawk WiFi', 'price': 289.99, 'wattage': 50, 'socket': 'AM5', 'badge': 'Value X670'},
        {'id': 'mobo3', 'name': 'ASUS ROG Strix B650-A White', 'price': 239.99, 'wattage': 45, 'socket': 'AM5', 'badge': 'White Theme'},
        {'id': 'mobo4', 'name': 'ASRock Z790 Pro RS WiFi', 'price': 199.99, 'wattage': 45, 'socket': 'LGA1700', 'badge': 'Budget Z790'}
    ],
    'gpu': [
        {'id': 'gpu1', 'name': 'NVIDIA GeForce RTX 5090 24GB', 'price': 1999.99, 'wattage': 450, 'socket': 'PCIe', 'badge': 'Ultra Spec'},
        {'id': 'gpu2', 'name': 'NVIDIA GeForce RTX 4090 24GB', 'price': 1699.99, 'wattage': 450, 'socket': 'PCIe', 'badge': 'Powerhouse'},
        {'id': 'gpu3', 'name': 'NVIDIA GeForce RTX 4080 Super 16GB', 'price': 999.99, 'wattage': 320, 'socket': 'PCIe', 'badge': 'High Tier'},
        {'id': 'gpu4', 'name': 'NVIDIA GeForce RTX 4070 Ti Super 16GB', 'price': 799.99, 'wattage': 285, 'socket': 'PCIe', 'badge': '1440p King'}
    ],
    'ram': [
        {'id': 'ram1', 'name': '64GB Corsair Dominator Titanium DDR5 6400', 'price': 299.99, 'wattage': 15, 'socket': 'DDR5', 'badge': 'Corsair'},
        {'id': 'ram2', 'name': '32GB G.Skill Trident Z5 RGB DDR5 6000', 'price': 139.99, 'wattage': 10, 'socket': 'DDR5', 'badge': 'RGB'},
        {'id': 'ram3', 'name': '32GB Teamgroup T-Force Delta White DDR5 6000', 'price': 119.99, 'wattage': 10, 'socket': 'DDR5', 'badge': 'White Build'},
        {'id': 'ram4', 'name': '16GB Kingston Fury Beast DDR5 5200', 'price': 69.99, 'wattage': 8, 'socket': 'DDR5', 'badge': 'Budget'}
    ],
    'storage': [
        {'id': 'ssd1', 'name': '2TB Samsung 990 Pro PCIe 4.0 NVMe', 'price': 179.99, 'wattage': 8, 'socket': 'M.2', 'badge': 'Reliable'},
        {'id': 'ssd2', 'name': '4TB Crucial T700 Gen5 NVMe SSD', 'price': 499.99, 'wattage': 12, 'socket': 'M.2', 'badge': 'Extreme Gen5'},
        {'id': 'ssd3', 'name': '2TB WD Black SN850X Gen4 NVMe', 'price': 149.99, 'wattage': 8, 'socket': 'M.2', 'badge': 'Gamers Pick'},
        {'id': 'ssd4', 'name': '1TB Kingston KC3000 NVMe SSD', 'price': 84.99, 'wattage': 6, 'socket': 'M.2', 'badge': 'Budget'}
    ],
    'psu': [
        {'id': 'psu1', 'name': 'ASUS ROG Thor 1200W Platinum II', 'price': 359.99, 'wattage': 1200, 'socket': 'ATX', 'badge': 'Thor OLED'},
        {'id': 'psu2', 'name': 'Corsair RM1000x 1000W 80+ Gold', 'price': 189.99, 'wattage': 1000, 'socket': 'ATX', 'badge': 'Solid Modular'},
        {'id': 'psu3', 'name': 'Seasonic Focus GX-850 White 850W', 'price': 149.99, 'wattage': 850, 'socket': 'ATX', 'badge': 'White Edition'},
        {'id': 'psu4', 'name': 'Corsair RM750e 750W Gold ATX 3.0', 'price': 99.99, 'wattage': 750, 'socket': 'ATX', 'badge': 'Budget'}
    ],
    'cooler': [
        {'id': 'cool1', 'name': 'NZXT Kraken Elite 360 RGB LCD', 'price': 279.99, 'wattage': 15, 'socket': 'Multi', 'badge': 'LCD Display'},
        {'id': 'cool2', 'name': 'Lian Li Galahad II LCD 360 White', 'price': 249.99, 'wattage': 12, 'socket': 'Multi', 'badge': 'White AIO'},
        {'id': 'cool3', 'name': 'DeepCool LT720 360mm AIO Cooler', 'price': 139.99, 'wattage': 12, 'socket': 'Multi', 'badge': 'Premium Block'},
        {'id': 'cool4', 'name': 'Noctua NH-D15 chromax.black Dual-Tower', 'price': 119.99, 'wattage': 5, 'socket': 'Multi', 'badge': 'Air Cooler'}
    ],
    'case': [
        {'id': 'case1', 'name': 'HYTE Y70 Touch Infinite Black', 'price': 359.99, 'wattage': 0, 'socket': 'ATX', 'badge': 'Built-in LCD'},
        {'id': 'case2', 'name': 'Lian Li O11 Dynamic EVO XL RGB', 'price': 229.99, 'wattage': 0, 'socket': 'ATX', 'badge': 'Enthusiast Case'},
        {'id': 'case3', 'name': 'NZXT H9 Elite Flow White', 'price': 239.99, 'wattage': 0, 'socket': 'ATX', 'badge': 'All Glass White'},
        {'id': 'case4', 'name': 'Phanteks NV5 Panoramic Glass Black', 'price': 99.99, 'wattage': 0, 'socket': 'ATX', 'badge': 'Budget Glass'}
    ]
}

# 1. Homepage View
def home(request):
    featured_pcs = Product.objects.filter(is_featured=True).select_related('category')[:3]
    trending_components = Product.objects.filter(is_trending=True).select_related('category')[:3]

    context = {
        'title': 'Overclock PC Shop | Premium Gaming Desktops & Hardware',
        'featured_pcs': featured_pcs,
        'trending_components': trending_components,
    }
    return render(request, 'shop/home.html', context)

# 2. Product Catalog View
def catalog(request):
    selected_category = request.GET.get('category', 'all')
    search_query = request.GET.get('q', '')

    products_qs = Product.objects.select_related('category')

    if selected_category != 'all':
        products_qs = products_qs.filter(category__id_key=selected_category)

    if search_query:
        products_qs = products_qs.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(cpu__icontains=search_query) |
            Q(gpu__icontains=search_query)
        )

    # Build dynamic category list with live counts
    all_categories = [{'id': 'all', 'name': 'All Products', 'count': Product.objects.count()}]
    for cat in Category.objects.all():
        all_categories.append({
            'id': cat.id_key,
            'name': cat.name,
            'count': cat.products.count()
        })

    context = {
        'title': 'High-End Catalog | Overclock PC Shop',
        'products': products_qs,
        'categories': all_categories,
        'selected_category': selected_category,
        'search_query': search_query,
    }
    return render(request, 'shop/catalog.html', context)

# 3. Product Detail View
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)

    if request.method == 'POST':
        author_name = request.POST.get('author_name', '').strip()
        rating_val = request.POST.get('rating', '').strip()
        title = request.POST.get('title', '').strip()
        category = request.POST.get('category', 'other').strip()
        content = request.POST.get('content', '').strip()

        if not author_name or not rating_val or not title or not content:
            messages.error(request, 'Please fill in all required fields.')
        else:
            try:
                rating = int(rating_val)
                if 1 <= rating <= 5:
                    # Create review (auto-approved by default)
                    Review.objects.create(
                        product=product,
                        user=request.user if request.user.is_authenticated else None,
                        author_name=author_name,
                        rating=rating,
                        title=title,
                        category=category,
                        content=content,
                        source='storefront',
                        is_approved=True
                    )
                    
                    # Recalculate average rating and reviews count
                    approved = product.reviews.filter(is_approved=True)
                    count = approved.count()
                    if count:
                        avg = sum(r.rating for r in approved) / count
                        product.rating = round(avg, 1)
                        product.reviews_count = count
                    else:
                        product.rating = 0.0
                        product.reviews_count = 0
                    product.save(update_fields=['rating', 'reviews_count'])

                    messages.success(request, 'Review published successfully!')
                    return redirect('shop:product_detail', slug=product.slug)
                else:
                    messages.error(request, 'Rating must be between 1 and 5.')
            except ValueError:
                messages.error(request, 'Invalid rating format.')

    # Related: same category, exclude current
    related = Product.objects.filter(
        category=product.category
    ).exclude(slug=slug).select_related('category')[:3]

    # If not enough in-category, fill from all products
    if related.count() < 3:
        extra = Product.objects.exclude(slug=slug).select_related('category')[:3 - related.count()]
        related = list(related) + list(extra)

    reviews = product.reviews.filter(is_approved=True)

    context = {
        'title': f"{product.name} | Overclock PC Shop",
        'product': product,
        'related_products': related,
        'reviews': reviews,
    }
    return render(request, 'shop/detail.html', context)

# 4. Custom PC Builder View
def builder(request):
    context = {
        'title': 'Elite Custom PC Builder | Overclock PC Shop',
        'parts': BUILDER_PARTS,
    }
    return render(request, 'shop/builder.html', context)

# 5. Shopping Cart View
def cart(request):
    # Dynamic items in session or just mock default
    cart_items = [
        {
            'product': PRODUCTS['apex-horizon-ryzen-9'],
            'quantity': 1,
            'upgrades': ['64GB DDR5 Memory Upgrade (+$150)', 'Dual 2TB Gen4 SSD Raid (+$179)']
        },
        {
            'product': PRODUCTS['intel-i9-14900ks-cpu'],
            'quantity': 1,
            'upgrades': []
        }
    ]
    
    subtotal = sum(item['product']['price'] * item['quantity'] for item in cart_items)
    # Add upgrades pricing if applicable
    subtotal += 150.00 + 179.00
    shipping = 49.99
    total = subtotal + shipping
    
    # Recommended accessories (upsell)
    addons = [
        {'name': 'ASUS ROG Swift OLED PG32UCDM Monitor', 'price': 1299.99, 'image': 'monitor_upsell', 'slug': 'nvidia-rtx-5090-gpu'},
        {'name': 'Razer BlackWidow V4 Pro Keyboard', 'price': 229.99, 'image': 'keyboard_upsell', 'slug': 'corsair-dominator-titanium-ram'},
        {'name': 'Lian Li Uni Fan TL120 3-Pack RGB', 'price': 109.99, 'image': 'fans_upsell', 'slug': 'corsair-dominator-titanium-ram'}
    ]
    
    context = {
        'title': 'Shopping Cart | Overclock PC Shop',
        'cart_items': cart_items,
        'subtotal': round(subtotal, 2),
        'shipping': shipping,
        'total': round(total, 2),
        'addons': addons,
    }
    return render(request, 'shop/cart.html', context)

# 6. Checkout View
def checkout(request):
    # Default order subtotal
    subtotal = 4129.98
    shipping = 49.99
    total = subtotal + shipping
    
    context = {
        'title': 'Secure Checkout | Overclock PC Shop',
        'subtotal': round(subtotal, 2),
        'shipping': shipping,
        'total': round(total, 2),
    }
    return render(request, 'shop/checkout.html', context)

# 7. User Dashboard View
def dashboard(request):
    order_history = [
        {
            'id': 'OC-98472',
            'date': 'May 14, 2026',
            'total': 5149.98,
            'status': 'Delivered',
            'badge_color': 'bg-success text-dark fw-bold',
            'items': 'Nemesis RTX 5090 Edition (x1), Thermal Paste Tube (x1)'
        },
        {
            'id': 'OC-96541',
            'date': 'April 02, 2026',
            'total': 689.99,
            'status': 'Returned',
            'badge_color': 'bg-danger text-light fw-bold',
            'items': 'Intel Core i9-14900KS Processor (x1)'
        }
    ]
    
    saved_builds = [
        {
            'name': 'Project Neon Shadow',
            'date': 'May 27, 2026',
            'price': 3420.93,
            'wattage': 710,
            'specs': 'Intel i7-14700K | RTX 4080 Super | 32GB RAM | NZXT H9 Flow'
        },
        {
            'name': 'White Knight 5090',
            'date': 'May 18, 2026',
            'price': 4899.91,
            'wattage': 840,
            'specs': 'AMD Ryzen 7 7800X3D | RTX 5090 | 64GB RAM | Lian Li O11 Dynamic'
        }
    ]
    
    wishlist = [
        PRODUCTS['valkyrie-whiteout-edition'],
        PRODUCTS['corsair-dominator-titanium-ram']
    ]
    
    context = {
        'title': 'User Cyber Station | Overclock PC Shop',
        'order_history': order_history,
        'saved_builds': saved_builds,
        'wishlist': wishlist,
    }
    return render(request, 'shop/dashboard.html', context)

# 8. Admin Dashboard View
def admin_dashboard(request):
    # Statistics
    sales_total = 142589.90
    orders_count = 38
    avg_order_val = 3752.36
    low_stock_count = 3
    
    recent_orders = [
        {'id': 'OC-98475', 'customer': 'Alex Mercer', 'date': 'Today, 4:12 PM', 'total': 4999.99, 'status': 'Processing', 'color': 'text-info'},
        {'id': 'OC-98474', 'customer': 'Sarah Connor', 'date': 'Today, 2:40 PM', 'total': 2899.99, 'status': 'Shipped', 'color': 'text-primary'},
        {'id': 'OC-98473', 'customer': 'Neo Anderson', 'date': 'Yesterday', 'total': 3799.99, 'status': 'Processing', 'color': 'text-info'},
        {'id': 'OC-98472', 'customer': 'Bruce Wayne', 'date': 'Yesterday', 'total': 5149.98, 'status': 'Delivered', 'color': 'text-success'},
        {'id': 'OC-98471', 'customer': 'Tony Stark', 'date': 'May 25, 2026', 'total': 9999.98, 'status': 'Delivered', 'color': 'text-success'}
    ]
    
    low_stock_items = [
        {'name': 'NVIDIA GeForce RTX 5090 Founders Edition', 'sku': 'GPU-NV-5090-FE', 'stock': 3, 'status': 'Low Stock', 'color': 'badge bg-warning text-dark'},
        {'name': 'Valkyrie Whiteout Edition Prebuilt', 'sku': 'SYS-VALK-WHITE', 'stock': 5, 'status': 'Low Stock', 'color': 'badge bg-warning text-dark'},
        {'name': 'Intel Core i9-14900KS Processor', 'sku': 'CPU-INT-14900KS', 'stock': 12, 'status': 'In Stock', 'color': 'badge bg-success text-dark'}
    ]
    
    context = {
        'title': 'Cyber Control Center | Admin Dashboard',
        'sales_total': sales_total,
        'orders_count': orders_count,
        'avg_order_val': avg_order_val,
        'low_stock_count': low_stock_count,
        'recent_orders': recent_orders,
        'low_stock_items': low_stock_items,
    }
    return render(request, 'shop/admin.html', context)

# 9. Feedback View
def feedback(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        if not name or not email or not subject or not message:
            messages.error(request, 'Please fill in all telemetry transmission fields.')
        else:
            Feedback.objects.create(
                user=request.user if request.user.is_authenticated else None,
                name=name,
                email=email,
                subject=subject,
                message=message,
                status='new'
            )
            messages.success(request, 'Feedback broadcast successful! Our dev team has received your telemetry log.')
            return redirect('shop:feedback')

    context = {
        'title': 'Telemetry Broadcast | Submit Feedback',
    }
    return render(request, 'shop/feedback.html', context)

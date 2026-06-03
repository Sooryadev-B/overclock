"""
Management command: seed_db
Seeds the database with the initial Overclock PC Shop product catalog.
Usage: python manage.py seed_db
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from shop.models import Category, Product, Review, Feedback
from decimal import Decimal


CATEGORIES_DATA = [
    {'id_key': 'prebuilt', 'name': 'Prebuilt Gaming Rig'},
    {'id_key': 'gpu',      'name': 'Graphics Card (GPU)'},
    {'id_key': 'cpu',      'name': 'Processor (CPU)'},
    {'id_key': 'ram',      'name': 'System Memory (RAM)'},
    {'id_key': 'storage',  'name': 'Storage (SSD/HDD)'},
]

PRODUCTS_DATA = [
    {
        'name': 'Nemesis RTX 5090 Edition',
        'slug': 'nemesis-rtx-5090-edition',
        'category': 'prebuilt',
        'price': Decimal('4999.99'),
        'old_price': Decimal('5299.99'),
        'image': 'nemesis_rtx_5090_edition',
        'badge': 'FLAGSHIP',
        'rating': Decimal('4.9'),
        'reviews_count': 142,
        'stock': 8,
        'in_stock': True,
        'is_featured': True,
        'is_trending': False,
        'description': 'The ultimate gaming powerhouse. Engineered for enthusiasts who demand the absolute best in rendering, ray tracing, and frame rates. Featuring custom hardline liquid cooling and premium components wrapped in a matte black glass chassis.',
        'cpu': 'Intel Core i9-14900KS (6.2 GHz 24-Core)',
        'gpu': 'NVIDIA GeForce RTX 5090 24GB GDDR7',
        'ram': '64GB Corsair Dominator Titanium DDR5 6400MHz',
        'storage': '4TB Crucial T700 Gen5 NVMe SSD (12,400 MB/s)',
        'mobo': 'ASUS ROG Maximus Z790 Hero',
        'psu': 'ASUS ROG Thor 1200W Platinum II OLED',
        'cooler': 'Custom Hardline Open Loop Liquid Cooling',
        'case': 'HYTE Y70 Touch Infinite (Integrated Screen)',
    },
    {
        'name': 'Apex Horizon Ryzen 9',
        'slug': 'apex-horizon-ryzen-9',
        'category': 'prebuilt',
        'price': Decimal('3799.99'),
        'old_price': None,
        'image': 'apex_horizon_ryzen_9',
        'badge': 'POPULAR',
        'rating': Decimal('4.8'),
        'reviews_count': 98,
        'stock': 15,
        'in_stock': True,
        'is_featured': True,
        'is_trending': False,
        'description': "Designed for elite gamers and streamers. Leveraging AMD's revolutionary 3D V-Cache technology to maximize gaming performance while keeping temperatures and power consumption balanced.",
        'cpu': 'AMD Ryzen 9 7950X3D (16-Core, 3D V-Cache)',
        'gpu': 'NVIDIA GeForce RTX 4090 24GB GDDR6X',
        'ram': '32GB G.Skill Trident Z5 Neo RGB DDR5 6000MHz',
        'storage': '2TB Samsung 990 Pro PCIe 4.0 NVMe SSD',
        'mobo': 'MSI MAG X670E Tomahawk WiFi',
        'psu': 'Corsair RM1000x 1000W 80+ Gold PCIe 5.0',
        'cooler': 'NZXT Kraken Elite 360 RGB AIO Cooler',
        'case': 'Lian Li O11 Dynamic EVO XL RGB Black',
    },
    {
        'name': 'Valkyrie Whiteout Edition',
        'slug': 'valkyrie-whiteout-edition',
        'category': 'prebuilt',
        'price': Decimal('2899.99'),
        'old_price': Decimal('2999.99'),
        'image': 'valkyrie_whiteout_edition',
        'badge': 'WHITE OUT',
        'rating': Decimal('4.7'),
        'reviews_count': 64,
        'stock': 5,
        'in_stock': True,
        'is_featured': True,
        'is_trending': False,
        'description': 'A visually stunning all-white build with neon cyan aesthetics. Features elite-tier 1440p and 4K gaming power, customizable RGB lighting, and custom white braided cables.',
        'cpu': 'AMD Ryzen 7 7800X3D (8-Core 3D V-Cache)',
        'gpu': 'NVIDIA GeForce RTX 4080 Super 16GB White',
        'ram': '32GB Teamgroup T-Force Delta RGB DDR5 6000MHz White',
        'storage': '2TB WD Black SN850X NVMe M.2 SSD',
        'mobo': 'ASUS ROG Strix B650-A Gaming WiFi White',
        'psu': 'Seasonic Focus GX-850 850W White Gold',
        'cooler': 'Lian Li Galahad II LCD Trinity 360 White',
        'case': 'NZXT H9 Elite Flow White',
    },
    {
        'name': 'Rift Breaker Intel i7',
        'slug': 'rift-breaker-intel-i7',
        'category': 'prebuilt',
        'price': Decimal('1999.99'),
        'old_price': None,
        'image': 'rift_breaker_intel_i7',
        'badge': 'VALUE',
        'rating': Decimal('4.6'),
        'reviews_count': 112,
        'stock': 0,
        'in_stock': False,
        'is_featured': False,
        'is_trending': False,
        'description': 'The sweet-spot gaming rig. Ready to tear through AAA titles at high settings. Perfect entry into professional ray tracing and gaming at 1440p high frame-rates.',
        'cpu': 'Intel Core i7-14700K (5.6 GHz 20-Core)',
        'gpu': 'NVIDIA GeForce RTX 4070 Ti Super 16GB',
        'ram': '32GB G.Skill Ripjaws S5 DDR5 5600MHz',
        'storage': '1TB Kingston KC3000 PCIe 4.0 NVMe SSD',
        'mobo': 'ASRock Z790 Pro RS WiFi',
        'psu': 'Corsair RM850e 850W Gold ATX 3.0',
        'cooler': 'DeepCool LT720 360mm Liquid Cooler',
        'case': 'Phanteks NV5 Mid-Tower Black',
    },
    {
        'name': 'NVIDIA GeForce RTX 5090 Founders Edition',
        'slug': 'nvidia-rtx-5090-gpu',
        'category': 'gpu',
        'price': Decimal('1999.99'),
        'old_price': None,
        'image': 'nvidia_rtx_5090_gpu',
        'badge': 'NEW',
        'rating': Decimal('5.0'),
        'reviews_count': 18,
        'stock': 3,
        'in_stock': True,
        'is_featured': False,
        'is_trending': True,
        'description': 'The next frontier of GPU hardware. Utilizing the Blackwell architecture, featuring 24GB GDDR7 VRAM, and AI-accelerated DLSS 4 frame generation. The fastest graphics card on earth.',
        'cpu': 'Compatible with PCIe Gen 5.0 Slots',
        'gpu': '24GB GDDR7, Blackwell GPU Architecture',
        'ram': 'Recommends 850W+ ATX 3.0 PSU',
        'storage': 'DirectStorage 1.2 Compatible',
        'mobo': 'PCI Express 5.0 x16 interface',
        'psu': 'Requires 16-pin 12V2x6 Cable',
        'cooler': 'Founders Edition Tri-Slot Dual Axial Fan',
        'case': 'Length: 336mm, Width: 142mm',
    },
    {
        'name': 'Intel Core i9-14900KS Processor',
        'slug': 'intel-i9-14900ks-cpu',
        'category': 'cpu',
        'price': Decimal('689.99'),
        'old_price': Decimal('729.99'),
        'image': 'intel_i9_14900ks_cpu',
        'badge': 'HOT',
        'rating': Decimal('4.7'),
        'reviews_count': 53,
        'stock': 12,
        'in_stock': True,
        'is_featured': False,
        'is_trending': True,
        'description': 'Unleash extreme speeds with the special edition desktop processor reaching up to 6.2 GHz out of the box. Featuring 24 cores and 32 threads, optimized for high-end desktop workflows.',
        'cpu': 'LGA 1700 Socket Compatibility',
        'gpu': 'Intel UHD Graphics 770 Integrated',
        'ram': 'Supports DDR5 (5600+) & DDR4',
        'storage': 'Up to 20 PCIe Lanes',
        'mobo': 'Z790 / Z690 Intel Motherboards',
        'psu': 'Base Power: 150W, Turbo: 253W+',
        'cooler': 'High-performance AIO or custom loop required',
        'case': 'Compatible with standard socket coolers',
    },
    {
        'name': 'Corsair Dominator Titanium 64GB DDR5 6400MHz',
        'slug': 'corsair-dominator-titanium-ram',
        'category': 'ram',
        'price': Decimal('299.99'),
        'old_price': None,
        'image': 'corsair_dominator_titanium_ram',
        'badge': 'PREMIUM',
        'rating': Decimal('4.9'),
        'reviews_count': 32,
        'stock': 24,
        'in_stock': True,
        'is_featured': False,
        'is_trending': True,
        'description': 'Elite DDR5 memory combining clean style, advanced forged aluminum construction, and glowing custom RGB lighting. Tuned for extreme Intel and AMD overclocking profile optimizations.',
        'cpu': 'XMP 3.0 & EXPO Ready',
        'gpu': 'N/A',
        'ram': '2x32GB modules, CL32 latency, 1.4V',
        'storage': 'DHX Cooling Technology',
        'mobo': 'DDR5 Supporting Motherboards',
        'psu': 'N/A',
        'cooler': 'Low profile modules compatibility',
        'case': 'Height: 55mm with lightbars',
    },
]


class Command(BaseCommand):
    help = 'Seeds the database with the initial Overclock PC Shop product catalog'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear', action='store_true',
            help='Delete all existing products and categories before seeding'
        )

    def handle(self, *args, **options):
        if options['clear']:
            Product.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write(self.style.WARNING('🗑️  Cleared all existing products and categories.'))

        # Create categories
        self.stdout.write('📂 Creating categories...')
        for cat_data in CATEGORIES_DATA:
            cat, created = Category.objects.get_or_create(
                id_key=cat_data['id_key'],
                defaults={'name': cat_data['name']}
            )
            status = '✅ Created' if created else '⏭️  Exists'
            self.stdout.write(f'  {status}: {cat.name}')

        # Create products
        self.stdout.write('\n🛒 Seeding products...')
        created_count = 0
        skipped_count = 0

        for prod_data in PRODUCTS_DATA:
            category = Category.objects.get(id_key=prod_data.pop('category'))
            slug = prod_data.pop('slug')

            product, created = Product.objects.update_or_create(
                slug=slug,
                defaults={**prod_data, 'category': category}
            )

            if created:
                created_count += 1
                self.stdout.write(f'  ✅ Created: {product.name}')
            else:
                skipped_count += 1
                self.stdout.write(f'  🔄 Updated: {product.name}')

        self.stdout.write(self.style.SUCCESS(
            f'\n🚀 Seeding complete! {created_count} created, {skipped_count} updated.'
        ))

        self._seed_admin_user()
        self._seed_reviews()
        self._seed_feedback()

    def _seed_admin_user(self):
        self.stdout.write('\n👤 Creating admin user...')
        username = 'soorya'
        password = 'soorya2006'
        email = 'soorya@overclock.local'

        user, created = User.objects.get_or_create(username=username, defaults={'email': email})
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f'  ✅ Created admin user ({username} / {password})'))
        else:
            self.stdout.write(self.style.SUCCESS(f'  ✅ Updated admin user ({username} / {password})'))

    def _seed_reviews(self):
        if Review.objects.exists():
            self.stdout.write('\n⭐ Reviews already seeded, skipping.')
            return

        self.stdout.write('\n⭐ Seeding sample reviews...')
        product = Product.objects.filter(slug='nemesis-rtx-5090-edition').first()
        if not product:
            return

        samples = [
            {'author_name': 'Alex Mercer', 'rating': 5, 'title': 'Absolute beast of a machine', 'content': 'Runs every game at max settings. The liquid cooling is whisper quiet.', 'is_approved': True, 'source': 'storefront', 'category': 'performance'},
            {'author_name': 'Sarah Connor', 'rating': 4, 'title': 'Worth every penny', 'content': 'Delivery was fast, setup was plug and play. Minor RGB software quirks.', 'is_approved': True, 'source': 'storefront', 'category': 'shipping'},
            {'author_name': 'Neo Anderson', 'rating': 5, 'title': 'Best prebuilt I have owned', 'content': 'Premium build quality throughout. Cable management is flawless.', 'is_approved': True, 'source': 'admin', 'category': 'build'},
        ]
        for data in samples:
            Review.objects.create(product=product, **data)
        self.stdout.write(self.style.SUCCESS(f'  ✅ Created {len(samples)} reviews'))

    def _seed_feedback(self):
        if Feedback.objects.exists():
            self.stdout.write('\n💬 Feedback already seeded, skipping.')
            return

        self.stdout.write('\n💬 Seeding sample feedback...')
        samples = [
            {'name': 'Tony Stark', 'email': 'tony@example.com', 'subject': 'Custom build inquiry', 'message': 'Can you build a white-themed RTX 5090 rig with custom water cooling?', 'status': 'new'},
            {'name': 'Bruce Wayne', 'email': 'bruce@example.com', 'subject': 'Shipping delay', 'message': 'My order OC-98472 arrived damaged. Need replacement options.', 'status': 'read'},
            {'name': 'Diana Prince', 'email': 'diana@example.com', 'subject': 'Great experience', 'message': 'Thank you for the excellent customer support on my recent purchase!', 'status': 'resolved'},
        ]
        for data in samples:
            Feedback.objects.create(**data)
        self.stdout.write(self.style.SUCCESS(f'  ✅ Created {len(samples)} feedback entries'))

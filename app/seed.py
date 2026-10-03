import sys
from pathlib import Path

# Add project root directory to Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.database import Base, engine, SessionLocal
from app.models import Product, Customer

def init_db():
    """Create all database tables if they do not exist."""
    Base.metadata.create_all(bind=engine)
    print("Database tables initialized successfully.")

def seed_sample_products():
    """Populate default products if table is empty."""
    db = SessionLocal()
    try:
        count = db.query(Product).count()
        if count > 0:
            print(f"Products table already has {count} items. Skipping seed.")
            return

        sample_products = [
            Product(
                code="P101",
                name_sd="اصل سنڌي اجرڪ شال",
                name_ur="اصلی سندھی اجرک شال",
                name_en="Authentic Sindhi Ajrak Shawl",
                description_sd="قدرتي رنگن ۽ بلاڪ پرنٽ سان ٺهيل اصل سنڌي اجرڪ",
                description_ur="روایتی قدرتی بلاک پرنٹ سے تیار کردہ خوبصورت اجرک",
                description_en="Handcrafted traditional natural block-printed Ajrak cotton shawl",
                price=2500.0,
                category="Handicrafts",
                is_available=True
            ),
            Product(
                code="P102",
                name_sd="سنڌي ٽوپي (شيشي واري)",
                name_ur="روایتی سندھی ٹوپی (شیشہ دار)",
                name_en="Handcrafted Sindhi Cap with Mirrors",
                description_sd="نفيس ڌاڳي ۽ شيشن جي چمڪدار ڪم سان ڀريل شاندار سنڌي ٽوپي",
                description_ur="ہاتھ کی باریک کڑھائی اور خوبصورت شیشے والی سندھی ٹوپی",
                description_en="Premium handcrafted embroidered traditional Sindhi cap",
                price=1200.0,
                category="Handicrafts",
                is_available=True
            ),
            Product(
                code="P103",
                name_sd="سکر جون اعليٰ کجورون (1 ڪلو)",
                name_ur="سکھر کی اعلیٰ کھجوریں (1 کلو)",
                name_en="Premium Sukkur Organic Dates (1 KG)",
                description_sd="اصل سنڌ جي باغن مان تازيون، نرم ۽ مٺيون کجورون",
                description_ur="سندھ کے زرخیز باغات کی خالص اور لذیذ تازہ کھجوریں",
                description_en="Fresh organic natural sweet dates harvested in Sukkur",
                price=950.0,
                category="Food & Organic",
                is_available=True
            ),
            Product(
                code="P104",
                name_sd="ٻير جو خالص قدرتي ماکي (1 ڪلو)",
                name_ur="خالص بیری کا جنگلی شہد (1 کلو)",
                name_en="100% Pure Organic Sidr Honey (1 KG)",
                description_sd="سنڌ جي جنگلي ٻيرن مان نڪتل 100 سيڪڙو خالص ۽ شفا بخش ماکي",
                description_ur="جنگلی بیری کے پھولوں کا 100 فیصد خالص اور قدرتی شہد",
                description_en="Pure raw unpasteurized Sidr honey collected from wild flora",
                price=3200.0,
                category="Food & Organic",
                is_available=True
            ),
            Product(
                code="P105",
                name_sd="سنڌي هٿ جي ڀرت واري رلي",
                name_ur="ہاتھ کی بنی خوبصورت سندھی رلی",
                name_en="Traditional Heritage Sindhi Quilt (Rilli)",
                description_sd="سنڌي عورتن جي هٿن سان ٺهيل دلڪش ۽ رنگين روايتي رلي",
                description_ur="سندھی ثقافت کا شاہکار رنگ برنگی روایتی رلی",
                description_en="Heritage geometric hand-stitched traditional cotton quilt",
                price=4500.0,
                category="Home & Living",
                is_available=True
            ),
        ]

        db.add_all(sample_products)
        db.commit()
        print(f"Successfully seeded {len(sample_products)} sample products.")
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
    seed_sample_products()

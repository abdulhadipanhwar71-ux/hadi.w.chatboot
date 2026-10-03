"""
Internationalization (i18n) module supporting Urdu (ur), Sindhi (sd), and English (en).
All code and comments are strictly in English.
Clean corporate messaging with no robotic filler.
"""

TRANSLATIONS = {
    "ur": {
        "main_menu": (
            "🌸 *ہمارے واٹس ایپ اسٹور میں خوش آمدید*\n\n"
            "1️⃣ ہماری پروڈکٹس اور قیمتیں 🛍️\n"
            "2️⃣ نیا آرڈر بک کریں 🛒\n"
            "3️⃣ اپنا آرڈر ٹریک کریں 🔍\n"
            "4️⃣ کاروباری معلومات و طریقہ ادائیگی 💳\n"
            "5️⃣ ہمارے نمائندے سے رابطہ کریں 👨‍💼\n"
            "6️⃣ زبان / Language 🌐\n\n"
            "براہ کرم مطلوبہ آپشن کا نمبر (1 تا 6) درج کریں:"
        ),
        "select_language_prompt": (
            "🌐 *زبان منتخب کریں / Select Language / ٻولي چونڊيو:*\n\n"
            "1️⃣ اردو (Urdu)\n"
            "2️⃣ English\n"
            "3️⃣ سنڌي (Sindhi)\n\n"
            "براہ کرم 1، 2 یا 3 درج کریں:"
        ),
        "catalog_header": "🛍️ *ہماری دستیاب پروڈکٹس اور قیمتیں:*\n━━━━━━━━━━━━━━━━━━━━━━━\n",
        "catalog_item": "{index}️⃣ *{name}*\n• کوڈ: `{code}` | قیمت: *Rs {price:,.0f}*\n• تفصیل: {desc}\n\n",
        "catalog_footer": (
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "🛒 آرڈر کرنے کے لیے مطلوبہ کوڈ (مثلاً `{sample_code}`) یا *2* لکھیں\n"
            "📋 مین مینیو کے لیے *0* لکھیں"
        ),
        "order_select_product_prompt": (
            "🛒 *نیا آرڈر بک کریں (Place Order)*\n\n"
            "براہ کرم جس پروڈکٹ کا آرڈر کرنا چاہتے ہیں، اس کا نمبر (1 تا 5) یا کوڈ درج کریں:\n\n"
            "{product_list}\n\n"
            "(واپسی یا کینسل کرنے کے لیے *0* لکھیں)"
        ),
        "product_not_found": "معذرت! یہ پروڈکٹ موجود نہیں ہے۔ براہ کرم فہرست میں سے درست نمبر (1 تا 5) یا کوڈ لکھیں (یا مینیو کے لیے *0* لکھیں):",
        "ask_quantity": (
            "آپ نے منتخب کیا ہے: *{name}*\n"
            "فی یونٹ قیمت: *Rs {price:,.0f}*\n\n"
            "کتنی تعداد درکار ہے؟ (مثال: 1، 2، 5 لکھیں):\n"
            "(آرڈر منسوخ کرنے کے لیے *0* لکھیں)"
        ),
        "invalid_quantity": "براہ کرم درست تعداد (1، 2، یا زائد) درج کریں، یا منسوخ کرنے کے لیے *0* لکھیں:",
        "ask_name": (
            "بہترین! {quantity} عدد (کل رقم: *Rs {total:,.0f}*)۔\n\n"
            "پارسل اور رسید کے لیے خریدار کا *پورا نام* درج فرمائیں:\n"
            "(منسوخ کرنے کے لیے *0* لکھیں)"
        ),
        "ask_address": (
            "شکریہ {customer_name} صاحب!\n\n"
            "براہ کرم پارسل کی ترسیل کے لیے *مکمل پتہ اور شہر کا نام* درج فرمائیں (مثلاً: مکان نمبر، گلی، علاقہ، شہر):\n"
            "(منسوخ کرنے کے لیے *0* لکھیں)"
        ),
        "ask_payment_method": (
            "💳 *طریقہ ادائیگی منتخب کریں (Select Payment Method):*\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "1️⃣ کیش آن ڈیلیوری (Cash on Delivery - COD)\n"
            "2️⃣ ایزی پیسہ یا جاز کیش (EasyPaisa / JazzCash)\n"
            "3️⃣ آن لائن بینک ٹرانسفر (Direct Bank Transfer)\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "براہ کرم مطلوبہ آپشن کا نمبر (*1*، *2* یا *3*) درج کریں:\n"
            "(منسوخ کرنے کے لیے *0* لکھیں)"
        ),
        "order_invoice": (
            "🧾 *آرڈر کی حتمی رسید (Order Invoice Summary)*\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "📦 پروڈکٹ: *{product_name}*\n"
            "🔢 تعداد: *{quantity}*\n"
            "💵 فی یونٹ قیمت: Rs {unit_price:,.0f}\n"
            "🚚 ڈیلیوری چارجز: *بالکل مفت (Free)*\n"
            "💰 کل واجب الادا رقم: *Rs {total:,.0f}*\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "👤 خریدار کا نام: {customer_name}\n"
            "📞 رابطہ فون: {phone}\n"
            "📍 ترسیلی پتہ: {address}\n"
            "💳 طریقہ ادائیگی: *{payment_method}*\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "کیا آپ اس آرڈر کی تصدیق کرتے ہیں؟\n"
            "1️⃣ جی ہاں، آرڈر بک کریں ✅\n"
            "2️⃣ نہیں، آرڈر منسوخ کریں ❌"
        ),
        "order_success_cod": (
            "🎉 *مبارک ہو! آپ کا آرڈر کامیابی سے بک ہو گیا ہے۔*\n\n"
            "📦 آرڈر ٹریکنگ نمبر: *{order_number}*\n"
            "💰 کل وصولی رقم: *Rs {total:,.0f}*\n"
            "🚚 طریقہ ادائیگی: *کیش آن ڈیلیوری (COD)*\n\n"
            "🛵 *پیسے وصولی کی معلومات:*\n"
            "ہمارا کوریئر رائیڈر 2 سے 3 دنوں میں آپ کے پتے پر پارسل پہنچائے گا۔ آپ پارسل چیک کر کے موقع پر رائیڈر کو *Rs {total:,.0f}* نقد ادا کریں گے۔\n\n"
            "🔍 اپنا آرڈر ٹریک کرنے کے لیے کسی بھی وقت اپنا آرڈر نمبر لکھیں۔\n"
            "مین مینیو کے لیے *0* درج کریں۔"
        ),
        "order_success_jazzcash": (
            "🎉 *مبارک ہو! آپ کا آرڈر کامیابی سے بک ہو گیا ہے۔*\n\n"
            "📦 آرڈر ٹریکنگ نمبر: *{order_number}*\n"
            "💰 کل واجب الادا رقم: *Rs {total:,.0f}*\n\n"
            "📱 *JazzCash / EasyPaisa ادائیگی تفصیلات:*\n"
            "• موبائل اکاؤنٹ نمبر: *0300-1234567*\n"
            "• اکاؤنٹ ٹائٹل: *CTrend Business Store*\n\n"
            "⚠️ *پیسے ادا کرنے کے بعد:*\n"
            "براہ کرم رقم ٹرانسفر کر کے ٹرانزیکشن آئی ڈی (TID) یا سلپ کا اسکرین شاٹ یہاں واٹس ایپ پر ارسال کریں تاکہ آپ کا پارسل فوری روانہ کیا جا سکے۔\n\n"
            "مین مینیو کے لیے *0* درج کریں۔"
        ),
        "order_success_bank": (
            "🎉 *مبارک ہو! آپ کا آرڈر کامیابی سے بک ہو گیا ہے۔*\n\n"
            "📦 آرڈر ٹریکنگ نمبر: *{order_number}*\n"
            "💰 کل واجب الادا رقم: *Rs {total:,.0f}*\n\n"
            "🏦 *آفیشل بینک تفصیلات:*\n"
            "• بینک کا نام: *Meezan Bank Ltd*\n"
            "• اکاؤنٹ ٹائٹل: *CTrend Pvt Ltd*\n"
            "• اکاؤنٹ نمبر: *01020304050607*\n"
            "• IBAN: *PK99MEZN0001020304050607*\n\n"
            "⚠️ *پیسے جمع کروانے کے بعد:*\n"
            "رقم آن لائن ٹرانسفر یا بینک میں جمع کروا کے رسید یہاں واٹس ایپ پر شیئر فرمائیں۔ رسید کی تصدیق کے بعد پارسل فوری ڈسپیچ کر دیا جائے گا۔\n\n"
            "مین مینیو کے لیے *0* درج کریں۔"
        ),
        "order_cancelled": "❌ آپ کا آرڈر منسوخ کر دیا گیا ہے۔\nمین مینیو کے لیے *0* درج کریں۔",
        "ask_tracking_id": "براہ کرم اپنا آرڈر نمبر درج کریں (مثال: ORD-2026-1001 یا صرف نمبر لکھیں):\n(واپسی کے لیے *0* لکھیں)",
        "order_status_result": (
            "🔍 *آرڈر کی تفصیلات و موجودہ کیفیت:*\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "• آرڈر نمبر: *{order_number}*\n"
            "• خریدار کا نام: {customer_name}\n"
            "• تاریخ: {date}\n"
            "• پروڈکٹس: {items}\n"
            "• کل رقم: *Rs {total:,.0f}*\n"
            "• طریقہ ادائیگی: {payment_method}\n"
            "• موجودہ کیفیت: *{status}*\n"
            "• ترسیلی پتہ: {address}\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "مین مینیو کے لیے *0* درج کریں۔"
        ),
        "order_not_found": "معذرت! اس نمبر سے کوئی آرڈر ریکارڈ نہیں ملا۔ براہ کرم نمبر کی تصدیق کر کے دوبارہ کوشش کریں، یا مینیو کے لیے *0* لکھیں۔",
        "business_info": (
            "🏢 *کاروباری معلومات و ادائیگی کے ذرائع:*\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "⏰ دفتری اوقات: صبح 09:00 تا رات 10:00 (روزانہ)\n"
            "🚚 ڈیلیوری سروس: ملک بھر میں 2 سے 3 کاروباری ایام کے اندر (مفت ڈیلیوری)\n"
            "💳 ادائیگی کے منظور شدہ ذرائع:\n"
            "   • کیش آن ڈیلیوری (COD - رقم بوقت وصولی)\n"
            "   • ایزی پیسہ / جاز کیش: 0300-1234567 (ٹائٹل: CTrend Store)\n"
            "   • بینک اکاؤنٹ: میزان بینک (Meezan Bank Ltd)\n"
            "📍 ہیڈ آفس: سندھ ٹریڈ سینٹر، کراچی، پاکستان\n"
            "📞 ہیلپ لائن و واٹس ایپ: +92 300 1234567\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "مین مینیو کے لیے *0* درج کریں۔"
        ),
        "my_orders_header": (
            "📦 *آپ کے سابقہ اور منظور شدہ آرڈرز کی تفصیل:*\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
        ),
        "my_orders_item": (
            "{idx}️⃣ *آرڈر نمبر:* `{order_number}`\n"
            "• کیفیت: *{status}*\n"
            "• آئٹمز: {items}\n"
            "• کل رقم: *Rs {total:,.0f}* ({payment_method})\n"
            "• تاریخ: {date}\n\n"
        ),
        "my_orders_footer": (
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "کسی مخصوص آرڈر کی تفصیلی ٹریکنگ کے لیے اس کا آرڈر نمبر لکھیں۔\n"
            "مین مینیو کے لیے *0* درج کریں۔"
        ),
        "no_orders_found": "آپ کے اس فون نمبر پر ابھی تک کوئی آرڈر موصول نہیں ہوا۔ نیا آرڈر دینے کے لیے *2* درج کریں، یا مینیو کے لیے *0* لکھیں۔",
        "agent_handoff": (
            "👨‍💼 آپ کی درخواست کسٹمر کیئر ٹیم کو موصول ہو گئی ہے۔\n"
            "ہمارا سینئر نمائندہ جلد ہی یہاں واٹس ایپ پر آپ سے رابطہ کرے گا۔\n\n"
            "مین مینیو کے لیے *0* درج کریں۔"
        ),
        "fallback_unknown": (
            "براہ کرم دیے گئے آپشنز میں سے درست نمبر (1 تا 6) منتخب کریں، یا مین مینیو کے لیے *0* لکھیں۔"
        ),
        "status_labels": {
            "PENDING": "⏳ موصول شدہ / زیرِ تصدیق (Received/Pending)",
            "CONFIRMED": "✅ منظور شدہ اور تصدیق شدہ (Approved/Confirmed)",
            "SHIPPED": "🚚 روانہ کر دیا گیا (Shipped)",
            "DELIVERED": "🎉 پہنچا دیا گیا اور پیسے وصول (Delivered)",
            "CANCELLED": "❌ منسوخ شدہ (Cancelled)"
        }
    },

    "sd": {
        "main_menu": (
            "🌸 *اسان جي واٽس ايپ اسٽور ۾ ڀلي ڪري آيا*\n\n"
            "1️⃣ اسان جون پروڊڪٽس ۽ قيمتون 🛍️\n"
            "2️⃣ نئون آرڊر ڪريو 🛒\n"
            "3️⃣ پنهنجو آرڊر ٽريڪ ڪريو 🔍\n"
            "4️⃣ ڪاروبار ۽ ادائگي جا تفصيل 💳\n"
            "5️⃣ اسان جي نمائندي سان ڳالهايو 👨‍💼\n"
            "6️⃣ ٻولي / Language 🌐\n\n"
            "مهرباني ڪري گهربل آپشن جو نمبر (1 کان 6) لکو:"
        ),
        "select_language_prompt": (
            "🌐 *ٻولي چونڊيو / Select Language / زبان منتخب کریں:*\n\n"
            "1️⃣ سنڌي (Sindhi)\n"
            "2️⃣ اردو (Urdu)\n"
            "3️⃣ English\n\n"
            "مهرباني ڪري 1، 2 يا 3 لکو:"
        ),
        "catalog_header": "🛍️ *اسان جون دستياب پروڊڪٽس ۽ قيمتون:*\n━━━━━━━━━━━━━━━━━━━━━━━\n",
        "catalog_item": "{index}️⃣ *{name}*\n• ڪوڊ: `{code}` | قيمت: *Rs {price:,.0f}*\n• تفصيل: {desc}\n\n",
        "catalog_footer": (
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "🛒 آرڊر ڪرڻ لاءِ پراڊڪٽ ڪوڊ (مثال `{sample_code}`) يا *2* لکو\n"
            "📋 مينيو ڏسڻ لاءِ *0* لکو"
        ),
        "order_select_product_prompt": (
            "🛒 *نئون آرڊر لکايو (Place Order)*\n\n"
            "مهرباني ڪري جنهن پراڊڪٽ جو آرڊر ڪرڻ چاهيو ٿا، ان جو نمبر يا ڪوڊ لکو:\n\n"
            "{product_list}\n\n"
            "(واپس وڃڻ لاءِ *0* لکو)"
        ),
        "product_not_found": "معاف ڪجو! هي پراڊڪٽ موجود ناهي. مهرباني ڪري ڏنل لسٽ مان صحيح نمبر (1 کان 5) يا ڪوڊ لکو (يا مينيو لاءِ *0* لکو):",
        "ask_quantity": (
            "توهان چونڊيو آهي: *{name}*\n"
            "في يونٽ قيمت: *Rs {price:,.0f}*\n\n"
            "مهرباني ڪري گهربل تعداد (Quantity) لکو (مثال: 1، 2، 5):\n"
            "(رد ڪرڻ لاءِ *0* لکو)"
        ),
        "invalid_quantity": "مهرباني ڪري صحيح انگ (1، 2، يا وڌيڪ) لکو، يا منسوخ ڪرڻ لاءِ *0* لکو:",
        "ask_name": (
            "بهترين! {quantity} عدد (ڪل رقم: *Rs {total:,.0f}*)۔\n\n"
            "مهرباني ڪري پارسل ۽ رسيد لاءِ پنهنجو *پورو نالو* لکو:\n"
            "(رد ڪرڻ لاءِ *0* لکو)"
        ),
        "ask_address": (
            "مهرباني! پنهنجو مڪمل *ترسيل پتو ۽ شهر جو نالو* لکو (گهر نمبر، گهٽي، شهر):\n"
            "(رد ڪرڻ لاءِ *0* لکو)"
        ),
        "ask_payment_method": (
            "💳 *ادائگي جو طريقو چونڊيو (Payment Method):*\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "1️⃣ ڪيش آن ڊليوري (Cash on Delivery - COD)\n"
            "2️⃣ ايزي پئسا يا جاز ڪيش (EasyPaisa / JazzCash)\n"
            "3️⃣ بينڪ اڪائونٽ ٽرانسفر (Bank Transfer)\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "مهرباني ڪري *1*، *2* يا *3* لکو:\n"
            "(رد ڪرڻ لاءِ *0* لکو)"
        ),
        "order_invoice": (
            "🧾 *آرڊر جي رسيد ۽ تفصيل (Order Invoice)*\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "📦 پراڊڪٽ: *{product_name}*\n"
            "🔢 تعداد: *{quantity}*\n"
            "💵 في يونٽ اگهه: Rs {unit_price:,.0f}\n"
            "🚚 ڊليوري چارجز: *مفت (Free)*\n"
            "💰 ڪل ادا ڪرڻ واري رقم: *Rs {total:,.0f}*\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "👤 خريدار جو نالو: {customer_name}\n"
            "📞 رابطو فون: {phone}\n"
            "📍 ترسيل جو پتو: {address}\n"
            "💳 ادائگي جو طريقو: *{payment_method}*\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "ڇا توهان هن آرڊر جي تصديق ڪريو ٿا؟\n"
            "1️⃣ ها، آرڊر ڪنفرم ڪريو ✅\n"
            "2️⃣ نه، آرڊر رد ڪريو ❌"
        ),
        "order_success_cod": (
            "🎉 *مبارڪ هجي! اوهان جو آرڊر ڪاميابيءَ سان منظور ٿي ويو آهي.*\n\n"
            "📦 آرڊر ٽريڪنگ نمبر: *{order_number}*\n"
            "💰 ڪل رقم: *Rs {total:,.0f}*\n"
            "🚚 ادائگي جو طريقو: *ڪيش آن ڊليوري (COD)*\n\n"
            "🛵 *رقم وصولي بابت معلومات:*\n"
            "اسان جو رائيڊر 2 کان 3 ڏينهن اندر پارسل کڻي ايندو ۽ توهان پارسل وصول وقت رقم ادا ڪندا.\n\n"
            "🔍 پنهنجو آرڊر چيڪ ڪرڻ لاءِ ڪنهن به وقت هي آرڊر نمبر هتي لکو.\n"
            "مينيو لاءِ *0* لکو."
        ),
        "order_success_jazzcash": (
            "🎉 *مبارڪ هجي! اوهان جو آرڊر بڪ ٿي ويو آهي.*\n\n"
            "📦 آرڊر ٽريڪنگ نمبر: *{order_number}*\n"
            "💰 ادا ڪرڻ واري رقم: *Rs {total:,.0f}*\n\n"
            "📱 *JazzCash / EasyPaisa کاتي جا تفصيل:*\n"
            "• موبائل نمبر: *0300-1234567*\n"
            "• اڪائونٽ جو نالو: *CTrend Business Store*\n\n"
            "⚠️ *رقم موڪلڻ بعد:*\n"
            "مهرباني ڪري رقم موڪلي ٽرانزيڪشن آئي ڊي (TID) يا اسڪرين شاٽ هتي واٽس ايپ تي اماڻيو ته جيئن فوري پارسل روانو ڪجي.\n\n"
            "مينيو لاءِ *0* لکو."
        ),
        "order_success_bank": (
            "🎉 *مبارڪ هجي! اوهان جو آرڊر بڪ ٿي ويو آهي.*\n\n"
            "📦 آرڊر ٽريڪنگ نمبر: *{order_number}*\n"
            "💰 ادا ڪرڻ واري رقم: *Rs {total:,.0f}*\n\n"
            "🏦 *بئنڪ ٽرانسفر تفصيل:*\n"
            "• بئنڪ جو نالو: *Meezan Bank Ltd*\n"
            "• کاتي جو نالو (Title): *CTrend Pvt Ltd*\n"
            "• کاتو نمبر: *01020304050607*\n"
            "• IBAN: *PK99MEZN0001020304050607*\n\n"
            "⚠️ *رقم جمع ڪرڻ بعد:*\n"
            "رقم منتقل ڪري بئنڪ رسيد هتي واٽس ايپ تي شيئر ڪريو ته جيئن آرڊر تصديق کان پوءِ پارسل اماڻيو وڃي.\n\n"
            "مينيو لاءِ *0* لکو."
        ),
        "order_cancelled": "❌ آرڊر منسوخ ڪيو ويو آهي.\nمينيو ڏسڻ لاءِ *0* لکو.",
        "ask_tracking_id": "مهرباني ڪري پنهنجو آرڊر نمبر لکو (مثال: ORD-2026-1001 يا رڳو نمبر):\n(واپس وڃڻ لاءِ *0* لکو)",
        "order_status_result": (
            "🔍 *آرڊر جي معلومات ۽ اسٽيٽس:*\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "• آرڊر نمبر: *{order_number}*\n"
            "• خريدار: {customer_name}\n"
            "• تاريخ: {date}\n"
            "• پراڊڪٽس: {items}\n"
            "• ڪل رقم: *Rs {total:,.0f}*\n"
            "• ادائگي جو طريقو: {payment_method}\n"
            "• موجوده حالت: *{status}*\n"
            "• ترسيل پتو: {address}\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "مکيه مينيو لاءِ *0* لکو."
        ),
        "order_not_found": "معاف ڪجو! هن نمبر سان ڪو به آرڊر رڪارڊ نه مليو. مهرباني ڪري نمبر جي چڪاس ڪري ٻيهر ڪوشش ڪريو، يا مينيو لاءِ *0* لکو.",
        "business_info": (
            "🏢 *ڪاروبار ۽ پئسن جي ادائگي بابت معلومات:*\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "⏰ ڪم جا ڪلاڪ: صبح 09:00 کان رات 10:00 تائين (روزانو)\n"
            "🚚 ڊليوري سروس: پوري سنڌ ۽ پاڪستان ۾ (مفت ڊليوري 2 کان 3 ڏينهن اندر)\n"
            "💳 ادائگي جا طريقا:\n"
            "   • ڪيش آن ڊليوري (Cash on Delivery)\n"
            "   • جاز ڪيش / ايزي پئسا: 0300-1234567\n"
            "   • بئنڪ اڪائونٽ: ميزان بئنڪ (Meezan Bank Ltd)\n"
            "📍 آفيس/دڪان جو پتو: سنڌ ٽريڊ سينٽر، ڪراچي، سنڌ\n"
            "📞 هيلپ لائن ۽ واٽس ايپ: +92 300 1234567\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "مين مينيو ڏسڻ لاءِ *0* لکو."
        ),
        "my_orders_header": (
            "📦 *اوهان جا اڳوڻا ۽ منظور ٿيل آرڊر:*\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
        ),
        "my_orders_item": (
            "{idx}️⃣ *آرڊر نمبر:* `{order_number}`\n"
            "• حالت: *{status}*\n"
            "• سامان: {items}\n"
            "• ڪل رقم: *Rs {total:,.0f}* ({payment_method})\n"
            "• تاريخ: {date}\n\n"
        ),
        "my_orders_footer": (
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "مڪمل تفصيل ڏسڻ لاءِ آرڊر نمبر لکو.\n"
            "مينيو لاءِ *0* لکو."
        ),
        "no_orders_found": "هن نمبر تي اڃا تائين ڪو به آرڊر ملي نه سگهيو آهي. نئين آرڊر لاءِ *2* لکو، يا مينيو لاءِ *0* لکو.",
        "agent_handoff": (
            "👨‍💼 توهان جي درخواست سيلز ٽيم ڏانهن اماڻي وئي آهي.\n"
            "اسان جو نمائندو ٿوري ئي دير ۾ هتي اوهان سان رابطو ڪندو.\n\n"
            "مينيو تي واپس وڃڻ لاءِ *0* لکو."
        ),
        "fallback_unknown": (
            "مهرباني ڪري ڏنل آپشنز مان صحيح نمبر (1 کان 6) چونڊيو، يا مکيه مينيو لاءِ *0* لکو."
        ),
        "status_labels": {
            "PENDING": "⏳ انتظار ۾ (Pending)",
            "CONFIRMED": "✅ منظور ٿيل ۽ تصديق ٿيل (Confirmed)",
            "SHIPPED": "🚚 روانو ڪيل (Shipped)",
            "DELIVERED": "🎉 پهچائي ڏنو ويو ۽ ادائگي مڪمل (Delivered)",
            "CANCELLED": "❌ منسوخ ٿيل (Cancelled)"
        }
    },

    "en": {
        "main_menu": (
            "🌸 *Welcome to our WhatsApp Store*\n\n"
            "1️⃣ Products & Pricing 🛍️\n"
            "2️⃣ Place a New Order 🛒\n"
            "3️⃣ Track Your Order 🔍\n"
            "4️⃣ Business & Payment Details 💳\n"
            "5️⃣ Connect with Human Agent 👨‍💼\n"
            "6️⃣ Language / ٻولي / زبان 🌐\n\n"
            "Please reply with an option number (1-6):"
        ),
        "select_language_prompt": (
            "🌐 *Select Language / زبان منتخب کریں / ٻولي چونڊيو:*\n\n"
            "1️⃣ English\n"
            "2️⃣ اردو (Urdu)\n"
            "3️⃣ سنڌي (Sindhi)\n\n"
            "Please reply 1, 2, or 3:"
        ),
        "catalog_header": "🛍️ *Our Available Products & Pricing:*\n━━━━━━━━━━━━━━━━━━━━━━━\n",
        "catalog_item": "{index}️⃣ *{name}*\n• Code: `{code}` | Price: *Rs {price:,.0f}*\n• Details: {desc}\n\n",
        "catalog_footer": (
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "🛒 To order, reply with code (e.g. `{sample_code}`) or reply *2*\n"
            "📋 For Main Menu, reply *0*"
        ),
        "order_select_product_prompt": (
            "🛒 *Place a New Order*\n\n"
            "Please reply with the product number (1 to 5) or product code:\n\n"
            "{product_list}\n\n"
            "(Reply *0* to cancel)"
        ),
        "product_not_found": "Sorry! That item is not available. Please enter a valid number (1 to 5) or code from the list (or reply *0* for menu):",
        "ask_quantity": (
            "You selected: *{name}*\n"
            "Unit Price: *Rs {price:,.0f}*\n\n"
            "Please enter the quantity you wish to order (e.g. 1, 2, 5):\n"
            "(Reply *0* to cancel)"
        ),
        "invalid_quantity": "Please enter a valid numeric quantity (1, 2, or more), or reply *0* to cancel:",
        "ask_name": (
            "Great! {quantity} unit(s) (Total: *Rs {total:,.0f}*).\n\n"
            "Please enter your *full name* for shipping and invoice:\n"
            "(Reply *0* to cancel)"
        ),
        "ask_address": (
            "Thank you {customer_name}!\n\n"
            "Please enter your complete *delivery address and city* (House, Street, Area, City):\n"
            "(Reply *0* to cancel)"
        ),
        "ask_payment_method": (
            "💳 *Select Payment Method:*\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "1️⃣ Cash on Delivery (COD)\n"
            "2️⃣ EasyPaisa / JazzCash\n"
            "3️⃣ Direct Bank Transfer\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "Please reply with *1*, *2*, or *3*:\n"
            "(Reply *0* to cancel)"
        ),
        "order_invoice": (
            "🧾 *Order Invoice & Details*\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "📦 Product: *{product_name}*\n"
            "🔢 Quantity: *{quantity}*\n"
            "💵 Unit Price: Rs {unit_price:,.0f}\n"
            "🚚 Delivery: *Free*\n"
            "💰 Total Payable: *Rs {total:,.0f}*\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "👤 Customer Name: {customer_name}\n"
            "📞 Contact Phone: {phone}\n"
            "📍 Delivery Address: {address}\n"
            "💳 Payment Method: *{payment_method}*\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Would you like to confirm this order?\n"
            "1️⃣ Yes, confirm order ✅\n"
            "2️⃣ No, cancel order ❌"
        ),
        "order_success_cod": (
            "🎉 *Congratulations! Your order has been placed successfully.*\n\n"
            "📦 Order Tracking ID: *{order_number}*\n"
            "💰 Total Payable: *Rs {total:,.0f}*\n"
            "🚚 Payment Method: *Cash on Delivery (COD)*\n\n"
            "🛵 *Cash Collection Details:*\n"
            "Our courier rider will deliver your parcel within 2-3 business days. You will pay *Rs {total:,.0f}* in cash upon arrival.\n\n"
            "🔍 You can track your order status anytime by sending this order ID.\n"
            "Reply *0* for Main Menu."
        ),
        "order_success_jazzcash": (
            "🎉 *Congratulations! Your order has been registered.*\n\n"
            "📦 Order Tracking ID: *{order_number}*\n"
            "💰 Total Payable: *Rs {total:,.0f}*\n\n"
            "📱 *JazzCash / EasyPaisa Payment Account:*\n"
            "• Mobile Number: *0300-1234567*\n"
            "• Account Title: *CTrend Business Store*\n\n"
            "⚠️ *Payment Verification:*\n"
            "Please transfer the amount and share the transaction ID (TID) or payment screenshot here on WhatsApp for instant dispatch.\n\n"
            "Reply *0* for Main Menu."
        ),
        "order_success_bank": (
            "🎉 *Congratulations! Your order has been registered.*\n\n"
            "📦 Order Tracking ID: *{order_number}*\n"
            "💰 Total Payable: *Rs {total:,.0f}*\n\n"
            "🏦 *Bank Account Details:*\n"
            "• Bank Name: *Meezan Bank Ltd*\n"
            "• Account Title: *CTrend Pvt Ltd*\n"
            "• Account Number: *01020304050607*\n"
            "• IBAN: *PK99MEZN0001020304050607*\n\n"
            "⚠️ *Payment Verification:*\n"
            "After transferring funds, kindly share the deposit receipt here on WhatsApp. Once verified, your order will be dispatched immediately.\n\n"
            "Reply *0* for Main Menu."
        ),
        "order_cancelled": "❌ Your order has been cancelled.\nReply *0* for Main Menu.",
        "ask_tracking_id": "Please enter your Order ID to track (e.g. ORD-2026-1001 or just the number):\n(Reply *0* to cancel)",
        "order_status_result": (
            "🔍 *Order Details & Status:*\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "• Order ID: *{order_number}*\n"
            "• Customer: {customer_name}\n"
            "• Date: {date}\n"
            "• Items: {items}\n"
            "• Total: *Rs {total:,.0f}*\n"
            "• Payment Method: {payment_method}\n"
            "• Status: *{status}*\n"
            "• Delivery Address: {address}\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Reply *0* for Main Menu."
        ),
        "order_not_found": "Sorry! No order record found with this ID. Please double check and try again, or reply *0* for Main Menu.",
        "business_info": (
            "🏢 *Business Information & Payment Accounts:*\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "⏰ Working Hours: 09:00 AM - 10:00 PM (Daily)\n"
            "🚚 Nationwide Delivery: 2-3 business days across Pakistan (Free Delivery)\n"
            "💳 Accepted Payment Options:\n"
            "   • Cash on Delivery (COD - Pay when rider arrives)\n"
            "   • EasyPaisa / JazzCash: 0300-1234567\n"
            "   • Direct Bank Transfer: Meezan Bank Ltd\n"
            "📍 Head Office: Sindh Trade Center, Karachi, Pakistan\n"
            "📞 Helpline / WhatsApp: +92 300 1234567\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Reply *0* for Main Menu."
        ),
        "my_orders_header": (
            "📦 *Your Previous & Approved Orders:*\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
        ),
        "my_orders_item": (
            "{idx}️⃣ *Order ID:* `{order_number}`\n"
            "• Status: *{status}*\n"
            "• Items: {items}\n"
            "• Total: *Rs {total:,.0f}* ({payment_method})\n"
            "• Date: {date}\n\n"
        ),
        "my_orders_footer": (
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "Reply with any Order ID to view complete tracking details.\n"
            "Reply *0* for Main Menu."
        ),
        "no_orders_found": "No previous orders found for this phone number. Reply *2* to place a new order, or *0* for Main Menu.",
        "agent_handoff": (
            "👨‍💼 Your request has been forwarded to our support representative.\n"
            "An agent will message you back shortly.\n\n"
            "Reply *0* to return to Main Menu."
        ),
        "fallback_unknown": (
            "Please select a valid option number (1-6) from the menu, or reply *0* for Main Menu."
        ),
        "status_labels": {
            "PENDING": "⏳ Pending Confirmation",
            "CONFIRMED": "✅ Approved / Confirmed",
            "SHIPPED": "🚚 Shipped / In Transit",
            "DELIVERED": "🎉 Delivered & Paid",
            "CANCELLED": "❌ Cancelled"
        }
    }
}


def get_text(key: str, lang: str = "ur", **kwargs) -> str:
    """Retrieve localized string by key and language code, formatting with kwargs."""
    lang_dict = TRANSLATIONS.get(lang, TRANSLATIONS.get("ur", {}))
    template = lang_dict.get(key, TRANSLATIONS["en"].get(key, ""))
    if kwargs:
        try:
            return template.format(**kwargs)
        except Exception:
            return template
    return template


def get_status_label(status: str, lang: str = "ur") -> str:
    """Retrieve human-friendly localized order status label."""
    lang_dict = TRANSLATIONS.get(lang, TRANSLATIONS.get("ur", {}))
    status_map = lang_dict.get("status_labels", {})
    return status_map.get(status.upper(), status)

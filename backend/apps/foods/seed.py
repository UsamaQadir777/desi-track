from .models import FoodCategory, FoodItem


SEED_FOODS = {
    "Roti / Naan": {
        "icon": "bread-slice",
        "items": [
            {"name": "Chapati", "serving_type": FoodItem.SERVING_QUANTITY, "quantity_label": "1 medium roti", "serving_size_grams": 45, "calories": 120, "protein": 3.6, "carbs": 23.0, "fat": 2.0, "icon": "chapati"},
            {"name": "Tandoori Naan", "serving_type": FoodItem.SERVING_QUANTITY, "quantity_label": "1 naan", "serving_size_grams": 120, "calories": 310, "protein": 9.0, "carbs": 58.0, "fat": 5.0, "icon": "naan"},
            {"name": "Paratha", "serving_type": FoodItem.SERVING_QUANTITY, "quantity_label": "1 medium paratha", "serving_size_grams": 80, "calories": 260, "protein": 5.0, "carbs": 34.0, "fat": 12.0, "icon": "paratha"},
        ],
    },
    "Rice / Biryani": {
        "icon": "rice-bowl",
        "items": [
            {"name": "Chicken Biryani", "calories": 180, "protein": 8.5, "carbs": 24.0, "fat": 5.2, "icon": "biryani"},
            {"name": "Plain Boiled Rice", "calories": 130, "protein": 2.7, "carbs": 28.0, "fat": 0.3, "icon": "rice"},
            {"name": "Pulao", "calories": 165, "protein": 5.0, "carbs": 25.0, "fat": 5.0, "icon": "pulao"},
        ],
    },
    "Daal": {
        "icon": "bowl-food",
        "items": [
            {"name": "Daal Chana", "calories": 145, "protein": 8.2, "carbs": 19.0, "fat": 4.0, "icon": "daal"},
            {"name": "Masoor Daal", "calories": 116, "protein": 7.8, "carbs": 17.0, "fat": 2.8, "icon": "daal"},
        ],
    },
    "Karahi / Curry": {
        "icon": "cooking-pot",
        "items": [
            {"name": "Chicken Karahi", "calories": 190, "protein": 17.0, "carbs": 4.0, "fat": 12.0, "icon": "karahi"},
            {"name": "Beef Nihari", "calories": 210, "protein": 14.0, "carbs": 7.0, "fat": 14.0, "icon": "nihari"},
            {"name": "Chicken Korma", "calories": 215, "protein": 15.0, "carbs": 6.0, "fat": 15.0, "icon": "korma"},
        ],
    },
    "Sabzi": {
        "icon": "leaf",
        "items": [
            {"name": "Aloo Gobhi", "calories": 95, "protein": 2.4, "carbs": 12.0, "fat": 4.5, "icon": "sabzi"},
            {"name": "Bhindi Masala", "calories": 105, "protein": 2.0, "carbs": 9.0, "fat": 7.0, "icon": "bhindi"},
        ],
    },
    "Snacks": {
        "icon": "snack",
        "items": [
            {"name": "Samosa", "serving_type": FoodItem.SERVING_QUANTITY, "quantity_label": "1 medium samosa", "serving_size_grams": 70, "calories": 185, "protein": 4.0, "carbs": 21.0, "fat": 10.0, "icon": "samosa"},
            {"name": "Pakora", "serving_type": FoodItem.SERVING_QUANTITY, "quantity_label": "1 piece", "serving_size_grams": 25, "calories": 75, "protein": 2.0, "carbs": 8.0, "fat": 4.0, "icon": "pakora"},
            {"name": "Chana Chaat", "calories": 135, "protein": 6.0, "carbs": 22.0, "fat": 3.0, "icon": "chaat"},
        ],
    },
    "Drinks / Desserts": {
        "icon": "glass-water",
        "items": [
            {"name": "Sweet Lassi", "calories": 95, "protein": 3.2, "carbs": 15.0, "fat": 2.5, "icon": "lassi"},
            {"name": "Kheer", "calories": 135, "protein": 4.0, "carbs": 22.0, "fat": 4.0, "icon": "kheer"},
        ],
    },
}


def seed_foods():
    created = 0
    updated = 0

    for category_name, category_payload in SEED_FOODS.items():
        category, _ = FoodCategory.objects.update_or_create(
            name=category_name,
            defaults={"icon": category_payload.get("icon", "")},
        )
        for item_payload in category_payload["items"]:
            _, was_created = FoodItem.objects.update_or_create(
                category=category,
                name=item_payload["name"],
                defaults={
                    "serving_type": item_payload.get("serving_type", FoodItem.SERVING_GRAMS),
                    "quantity_label": item_payload.get("quantity_label", ""),
                    "serving_size_grams": item_payload.get("serving_size_grams", 100),
                    "icon": item_payload.get("icon", ""),
                    "calories": item_payload["calories"],
                    "protein": item_payload["protein"],
                    "carbs": item_payload["carbs"],
                    "fat": item_payload["fat"],
                    "is_active": True,
                },
            )
            created += int(was_created)
            updated += int(not was_created)

    return {"created": created, "updated": updated}

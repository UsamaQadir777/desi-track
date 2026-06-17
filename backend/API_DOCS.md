# Desi Track API Docs

Base URL: `/api/`

Authentication uses JWT bearer tokens:

```http
Authorization: Bearer <access_token>
```

Errors use a consistent shape:

```json
{
  "error": {
    "code": "validation_error",
    "message": "Validation failed.",
    "details": {}
  }
}
```

## Health

### GET `/api/health/`

Auth: No

Response:

```json
{ "status": "ok" }
```

## Auth

### POST `/api/auth/signup/`

Auth: No

Body:

```json
{
  "name": "Ayesha Khan",
  "email": "ayesha@example.com",
  "password": "StrongPass123"
}
```

Response `201`:

```json
{
  "refresh": "<refresh_token>",
  "access": "<access_token>",
  "user": {
    "id": 1,
    "username": "ayesha@example.com",
    "email": "ayesha@example.com",
    "profile": {
      "name": "Ayesha Khan",
      "goal": "maintain",
      "age": null,
      "gender": "other",
      "height": null,
      "current_weight": null,
      "activity_level": "normal_walk",
      "daily_calorie_goal": 0,
      "protein_goal": 0,
      "carbs_goal": 0,
      "fat_goal": 0,
      "onboarding_completed": false
    }
  }
}
```

### POST `/api/auth/login/`

Auth: No

Body:

```json
{ "email": "ayesha@example.com", "password": "StrongPass123" }
```

Response `200`: same token shape as signup.

### POST `/api/auth/refresh/`

Auth: No

Body:

```json
{ "refresh": "<refresh_token>" }
```

Response `200`:

```json
{ "access": "<new_access_token>", "refresh": "<new_refresh_token>" }
```

### POST `/api/auth/logout/`

Auth: Yes

Body:

```json
{ "refresh": "<refresh_token>" }
```

Response: `204 No Content`

### GET `/api/auth/me/`

Auth: Yes

Response `200`: current user and profile.

## Profile

### GET `/api/profile/`

Auth: Yes

Response `200`: current user's profile.

### PATCH `/api/profile/`

Auth: Yes

Body fields:

```json
{
  "name": "Ayesha Khan",
  "goal": "lose",
  "age": 30,
  "gender": "female",
  "height": "165.00",
  "current_weight": "70.00",
  "activity_level": "light_active"
}
```

Valid values:

- `goal`: `lose`, `gain`, `maintain`
- `gender`: `male`, `female`, `other`
- `activity_level`: `no_activity`, `normal_walk`, `light_active`, `very_active`

Updating goal calculation fields requires all onboarding inputs. The response includes recalculated calorie and macro goals.

## Foods

### GET `/api/foods/`

Auth: Yes

Query params:

- `search`: optional name/category search
- `category`: optional category id, slug, or exact category name
- `page`: optional page number

Response `200`:

```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "category": 1,
      "category_name": "Roti / Naan",
      "category_icon": "bread-slice",
      "name": "Chapati",
      "slug": "chapati",
      "icon": "chapati",
      "serving_type": "quantity",
      "quantity_label": "1 medium roti",
      "serving_size_grams": "45.00",
      "calories": "120.00",
      "protein": "3.60",
      "carbs": "23.00",
      "fat": "2.00"
    }
  ]
}
```

### GET `/api/foods/categories/`

Auth: Yes

Response `200`: categories with icons and active item lists.

### GET `/api/foods/<id>/`

Auth: Yes

Response `200`: one food item.

## Meals

### GET `/api/meals/`

Auth: Yes

Query params:

- `date`: optional `YYYY-MM-DD`
- `meal_type`: optional `breakfast`, `lunch`, `snacks`, `dinner`
- `page`: optional page number

Response `200`: paginated meal entries scoped to the current user.

### POST `/api/meals/`

Auth: Yes

Body:

```json
{
  "food": 1,
  "meal_type": "lunch",
  "date": "2026-06-11",
  "amount": "150.00",
  "amount_type": "grams"
}
```

Response `201`: created meal entry with computed `calories`, `protein`, `carbs`, and `fat`.

### GET `/api/meals/<id>/`

Auth: Yes

Response `200`: one meal entry owned by the current user.

### PATCH `/api/meals/<id>/`

Auth: Yes

Body: any editable meal fields. Nutrition is recalculated after updates.

### DELETE `/api/meals/<id>/`

Auth: Yes

Response: `204 No Content`

## Water

### GET `/api/water/`

Auth: Yes

Query params:

- `date`: optional `YYYY-MM-DD`; returns or creates one day
- `start` and `end`: optional `YYYY-MM-DD`; returns records in range

Response `200`:

```json
{
  "id": 1,
  "date": "2026-06-11",
  "amount_ml": 750,
  "goal_ml": 2000,
  "remaining_ml": 1250,
  "progress_percent": 38,
  "updated_at": "2026-06-11T12:00:00Z"
}
```

### POST `/api/water/`

Auth: Yes

Body:

```json
{ "date": "2026-06-11", "amount_ml": 1200, "goal_ml": 2000 }
```

Response `200`: created or updated daily water record.

### PATCH `/api/water/`

Auth: Yes

Body: same as POST, partial fields allowed.

## Dashboard

### GET `/api/dashboard/`

Auth: Yes

Query params:

- `date`: optional `YYYY-MM-DD`, defaults to today

Response `200`:

```json
{
  "date": "2026-06-11",
  "daily_goal": { "calories": 2000, "protein": 120, "carbs": 220, "fat": 65 },
  "consumed": { "calories": 300.0, "protein": 30.0, "carbs": 45.0, "fat": 6.0 },
  "remaining_calories": 1700.0,
  "water": { "amount_ml": 2000, "goal_ml": 2000, "remaining_ml": 0, "progress_percent": 100 },
  "tasks": [
    { "id": "water", "label": "Drink water", "done": true },
    { "id": "breakfast", "label": "Log breakfast", "done": true },
    { "id": "all_meals", "label": "Log at least three meals", "done": true }
  ],
  "meal_summary": []
}
```

## Progress

### GET `/api/progress/`

Auth: Yes

Query params:

- `start`: optional `YYYY-MM-DD`, defaults to six days before end
- `end`: optional `YYYY-MM-DD`, defaults to today

Response `200`:

```json
{
  "range": { "start": "2026-06-05", "end": "2026-06-11" },
  "daily": [],
  "weekly_progress": [],
  "totals": { "calories": 300.0, "protein": 30.0, "carbs": 45.0, "fat": 6.0 },
  "pie_chart": [
    { "macro": "protein", "grams": 30.0, "calories": 120.0, "percent": 28.6 },
    { "macro": "carbs", "grams": 45.0, "calories": 180.0, "percent": 42.9 },
    { "macro": "fat", "grams": 6.0, "calories": 54.0, "percent": 12.9 }
  ]
}
```

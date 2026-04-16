TEMPLATE_LIST = [
    {"id": 1, "name": "Classic Professional", "category": "Professional"},
    {"id": 2, "name": "Modern Blue", "category": "Modern"},
    {"id": 3, "name": "Minimal Clean", "category": "Minimal"},
    {"id": 4, "name": "Corporate Gray", "category": "Corporate"},
    {"id": 5, "name": "Elegant Sidebar", "category": "Creative"},
]

# Auto-generate up to 100+ designs
for i in range(6, 121):
    TEMPLATE_LIST.append({
        "id": i,
        "name": f"Resume Design {i}",
        "category": "Custom"
    })

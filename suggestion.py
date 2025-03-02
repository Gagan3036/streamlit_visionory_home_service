from transformers import pipeline

pipe = pipeline("image-classification", model="sharmajai901/UL_interior_classification")

all_class = {
    "bicycle_storage" : {0: 'Tables', 1: 'Chairs', 2: 'Lamps', 3: 'Photo Frames'},
    "building_interiors" : {0: 'Chairs', 1: 'Beds', 2: 'Cupboards', 3: 'Tables', 4: 'Lamps', 5: 'Photo Frames', 6: 'Sofas', 7: 'Mirrors', 8: 'Dinning Tables', 9: 'Flower Pots', 10: 'Windows'},
    "cinema_room" : {0: 'Chairs', 1: 'Sofas'},
    "communal_lounge" : {0: 'Chairs', 1: 'Sofas', 2: 'Tables', 3: 'Lamps', 4: 'Photo Frames', 5: 'Mirrors', 6: 'Dinning Tables', 7: 'Flower Pots'},
    "dining_area" : {0: 'Chairs', 1: 'Tables', 2: 'Lamps', 3: 'Photo Frames', 5: 'Dinning Tables', 6: 'Flower Pots'},
    "entertainment_area" : {0: 'Chairs', 1: 'Sofas', 2: 'Tables', 3: 'Lamps', 4: 'Photo Frames', 5: 'Mirrors', 6: 'Flower Pots'},
    "fitness_room" : {0: 'Chairs', 1: 'Sofas', 2: 'Tables', 3: 'Lamps', 4: 'Photo Frames', 5: 'Mirrors'},
    "games_area" : {0: 'Chairs', 1: 'Sofas', 2: 'Tables', 3: 'Lamps', 4: 'Photo Frames', 5: 'Mirrors', 6: 'Flower Pots'},
    "gym" : {0: 'Chairs', 1: 'Sofas', 2: 'Tables', 3: 'Lamps', 4: 'Photo Frames', 5: 'Mirrors'},
    "laundry_area" : {0: 'Chairs', 1: 'Sofas', 2: 'Tables', 3: 'Lamps', 4: 'Photo Frames', 5: 'Mirrors', 6: 'Dinning Tables', 7: 'Flower Pots'},
    "living_area" : {0: 'Chairs', 1: 'Beds', 2: 'Cupboards', 3: 'Tables', 4: 'Lamps', 5: 'Photo Frames', 6: 'Sofas', 7: 'Mirrors', 8: 'Dinning Tables', 9: 'Flower Pots', 10: 'Windows'},
    "living_area_shared_kitchen" : {0: 'Chairs', 1: 'Sofas', 2: 'Tables', 3: 'Lamps', 4: 'Photo Frames', 5: 'Mirrors', 6: 'Dinning Tables'},
    "meeting_room" : {0: 'Chairs', 1: 'Sofas', 2: 'Tables', 3: 'Lamps', 4: 'Photo Frames', 5: 'Flower Pots'},
    "parking" : {0: 'Chairs', 1: 'Tables', 2: 'Lamps', 3: 'Mirrors', 4: 'Flower Pots'},
    "reception" : {0: 'Chairs', 1: 'Sofas', 2: 'Tables', 3: 'Lamps', 4: 'Photo Frames', 5: 'Flower Pots'},
    "rooftoop_area" : {0: 'Chairs', 1: 'Sofas', 2: 'Tables', 3: 'Lamps', 4: 'Photo Frames', 5: 'Mirrors', 6: 'Dinning Tables', 7: 'Flower Pots'},
    "storage_lockers" : {0: 'Chairs', 1: 'Tables', 2: 'Lamps', 3: 'Mirrors', 4: 'Flower Pots'},
    "study_area" : {0: 'Chairs', 1: 'Tables', 2: 'Lamps', 3: 'Photo Frames', 4: 'Mirrors', 5: 'Flower Pots'},
    "swimming_pool" : {0: 'Chairs', 1: 'Sofas', 2: 'Tables', 3: 'Lamps', 4: 'Photo Frames', 5: 'Mirrors', 6: 'Dinning Tables', 7: 'Flower Pots'}
}


def get_furniture_category_suggestion(image_path: str) -> str:
    results = pipe(image_path)
    top_label = max(results, key=lambda x: x['score'])['label']
    return all_class[top_label]


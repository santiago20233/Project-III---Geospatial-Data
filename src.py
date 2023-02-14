def get_offices_location (data):
    nested_data = []
    for item in data:
        name = item['name']
        for office in item['offices']:
            nested_data.append({
                'name': name,
                'office description': office['description'],
                'office latitude': office['latitude'],
                'office longitude': office['longitude']
            })
    df = pd.DataFrame(nested_data)
    return df
    

import csv
import json


def convert_file(csv_file, json_file, model):

    '''Преобразование из JSON в CSV'''

    result = []
    with open(csv_file, 'r', encoding='utf-8') as csv_f:
        csv_reade = csv.DictReader(csv_f)
        for row in csv_reade:
            record = {"model": model, "pk": row["id"]}
            del row["id"]
            if 'price' in row:
                row['price'] = int(row['price'])
            if 'is_published' in row:
                if row['is_published'] == "TRUE":
                    row['is_published'] = True
                else:
                    row['is_published'] = False
            record["fields"] = row
            result.append(record)

    with open(json_file, 'w', encoding='utf-8') as json_f:
        json_f.write(json.dumps(result, ensure_ascii=False))


convert_file('../data/ads.csv', '../data/ads.json', 'ads.ads')
convert_file('../data/categories.csv', '../data/categories.json', 'ads.categories')


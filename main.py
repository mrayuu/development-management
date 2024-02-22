import requests
import json
import base64


# Ваши данные для добавления новых объектов

new_data = [
    {"id": "4", "name": "Apple iPhone 11, 64GB", "data": {"price": 389.99, "color": "Purple"}},
    {"id": "5", "name": "Samsung Galaxy Z Fold2", "data": {"price": 689.99, "color": "Brown"}},
    {"id": "6", "name": "Apple AirPods", "data": {"generation": "3rd", "price": 120}},
    {"id": "10", "name": "Apple iPad Mini 5th Gen", "data": {"Capacity": "64 GB", "Screen size": 7.9}},
    {"id": "12", "name": "Apple iPad Air", "data": {"Generation": "4th", "Price": "419.99", "Capacity": "64 GB"}},
    {"id": "13", "name": "Apple iPad Air", "data": {"Generation": "4th", "Price": "519.99", "Capacity": "256 GB"}}
]

additional_data = [
    {"id": "16", "name": "Logitech MX Master 3", "data": {"type": "Wireless", "price": 99.99}},
    {"id": "17", "name": "Dell XPS 13", "data": {"Processor": "Intel Core i7", "price": 1299.99}}
]

# Ваш персональный токен доступа
token = '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'

# URL для обновления (PUT) файла products.json
url = 'https://api.github.com/repos/mrayuu/development-management/contents/products.json'

headers = {
    'Authorization': f'Token {token}',
    'Accept': 'application/vnd.github.v3+json'
}


# Получение текущего содержимого файла
response_get = requests.get(url, headers=headers)
data_get = response_get.json()
current_sha = data_get['sha']

# Кодирование нового текста в Base64
encoded_content = base64.b64encode(json.dumps(new_data, ensure_ascii=False).encode()).decode()

data = {
    'message': 'Обновление файла products.json',
    'content': encoded_content,
    'sha': current_sha
}

# PUT-запрос для обновления файла с новым содержимым
response_put = requests.put(url, headers=headers, json=data)

if response_put.status_code == 200:
    print(f"Данные успешно обновлены в файле products.json.")
else:
   print(f"Ошибка {response_put.status_code}: {response_put.text}")


# Затем делаем GET-запрос для получения содержимого файла
response_get = requests.get(url, headers=headers)
data_get = response_get.json()

if response_get.status_code == 200:
    # Декодируем содержимое из Base64
    decoded_content = base64.b64decode(data_get['content']).decode('utf-8')
    print(f"Содержимое products.json перед удалением:\n{decoded_content}")

    # Прочитаем данные и удалим два элемента
    products_data = json.loads(decoded_content)
    products_data = products_data[2:]  # Удалим два элемента (например, первые два)

    # Кодируем обновленные данные в формат JSON с ensure_ascii=False
    updated_json_data = json.dumps(products_data, ensure_ascii=False)

    # Создаем DELETE-запрос для удаления файла
    data_delete = {
        'message': 'Удаление двух элементов из файла products.json',
        'sha': data_get['sha']
    }

    response_delete = requests.delete(url, headers=headers, json=data_delete)

    if response_delete.status_code == 200:
        print(f"Два элемента успешно удалены из файла products.json.")

        # Создаем POST-запрос для создания файла с обновленными данными
        data_post = {
            'message': 'Добавление файла products.json',
            'content': base64.b64encode(updated_json_data.encode()).decode()
        }

        response_post = requests.put(url, headers=headers, json=data_post)

        if response_post.status_code == 200:
            print(f"Обновленные данные успешно записаны в файл products.json.")
        else:
            print(f"Ошибка {response_post.status_code}: {response_post.text}")

            # В случае ошибки при записи, попробуем восстановить предыдущие данные
            restore_data = {
                'message': 'Восстановление предыдущих данных в файл products.json',
                'content': data_get['content'],
                'sha': data_get['sha']
            }

            requests.put(url, headers=headers, json=restore_data)

    else:
        print(f"Ошибка {response_delete.status_code}: {response_delete.text}")

else:
    print(f"Ошибка {response_get.status_code}: {response_get.text}")

# Затем делаем GET-запрос для получения содержимого обновленного файла
response_get_updated = requests.get(url, headers=headers)
data_get_updated = response_get_updated.json()

if response_get_updated.status_code == 200:
    # Декодируем содержимое из Base64
    decoded_content_updated = base64.b64decode(data_get_updated['content']).decode('utf-8')
    print(f"\nОбновленное содержимое products.json:\n{decoded_content_updated}")
else:
    print(f"Ошибка {response_get_updated.status_code}: {response_get_updated.text}")

# Чтение текущего содержимого из Base64
decoded_content_before = base64.b64decode(data_get['content']).decode('utf-8')
print(f"\nСодержимое products.json перед добавлением новых данных:\n{decoded_content_before}")

# Добавление новых данных к текущему списку
products_data_additional = json.loads(decoded_content_before)
products_data_additional.extend(additional_data)

# Кодирование обновленных данных в формат JSON с ensure_ascii=False
updated_json_data_additional = json.dumps(products_data_additional, ensure_ascii=False)

# Создаем PUT-запрос для обновления файла с новыми данными
data_additional = {
    'message': 'Добавление новых данных в файл products.json',
    'content': base64.b64encode(updated_json_data_additional.encode()).decode(),
    'sha': data_get['sha']
}

response_put_additional = requests.put(url, headers=headers, json=data_additional)

if response_put_additional.status_code == 200:
    print(f"Новые данные успешно добавлены в файл products.json.")
else:
    print(f"Ошибка {response_put_additional.status_code}: {response_put_additional.text}")

# Затем делаем GET-запрос для получения содержимого обновленного файла
response_get_updated_additional = requests.get(url, headers=headers)
data_get_updated_additional = response_get_updated_additional.json()

if response_get_updated_additional.status_code == 200:
    # Декодируем содержимое из Base64
    decoded_content_updated_additional = base64.b64decode(data_get_updated_additional['content']).decode('utf-8')
    print(f"\nОбновленное содержимое products.json после добавления новых данных:\n{decoded_content_updated_additional}")
else:
    print(f"Ошибка {response_get_updated_additional.status_code}: {response_get_updated_additional.text}")

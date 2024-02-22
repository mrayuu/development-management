import requests
import json
import base64

# Ваш URL и токен
url = 'https://api.github.com/repos/mrayuu/development-management/contents/products.json'
token = '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'

headers = {
    'Authorization': f'Token {token}',
    'Accept': 'application/vnd.github.v3+json'
}

def test_api_connection():
    # Тестирование подключения к API (GET)
    response = requests.get(url, headers=headers)
    assert response.status_code == 200, f"Ошибка при подключении к API. Код: {response.status_code}"

def test_post_data():
    # Тестирование добавления данных (POST)
    new_data = [
        {"id": "4", "name": "Apple iPhone 11, 64GB", "data": {"price": 389.99, "color": "Purple"}},
        {"id": "5", "name": "Samsung Galaxy Z Fold2", "data": {"price": 689.99, "color": "Brown"}},
        {"id": "6", "name": "Apple AirPods", "data": {"generation": "3rd", "price": 120}},
        {"id": "10", "name": "Apple iPad Mini 5th Gen", "data": {"Capacity": "64 GB", "Screen size": 7.9}},
        {"id": "12", "name": "Apple iPad Air", "data": {"Generation": "4th", "Price": "419.99", "Capacity": "64 GB"}},
        {"id": "13", "name": "Apple iPad Air", "data": {"Generation": "4th", "Price": "519.99", "Capacity": "256 GB"}}
    ]

    # Кодирование нового текста в Base64
    encoded_content = base64.b64encode(json.dumps(new_data, ensure_ascii=False).encode()).decode()

    data = {
        'message': 'Добавление тестовых данных в файл products.json',
        'content': encoded_content
    }

    response_post = requests.put(url, headers=headers, data=json.dumps(data))
    assert response_post.status_code == 200, f"Ошибка при добавлении данных. Код: {response_post.status_code}"

def test_get_data():
    # Тестирование получения данных (GET)
    response_get = requests.get(url, headers=headers)
    assert response_get.status_code == 200, f"Ошибка при получении данных. Код: {response_get.status_code}"

def test_delete_data():
    # Тестирование удаления данных (DELETE)
    response_get = requests.get(url, headers=headers)
    assert response_get.status_code == 200, f"Ошибка при получении данных перед удалением. Код: {response_get.status_code}"

    # Декодируем содержимое из Base64
    decoded_content = base64.b64decode(response_get.content).decode('utf-8', errors='replace')

    try:
        products_data = json.loads(decoded_content)
    except json.JSONDecodeError:
        assert False, "Ошибка при декодировании JSON."

    # Удаляем первые два элемента (например)
    products_data = products_data[2:]

    # Кодируем обновленные данные в формат JSON с ensure_ascii=False
    updated_json_data = json.dumps(products_data, ensure_ascii=False)

    # Получаем SHA текущего файла
    sha = response_get.json()['sha']

    # Создаем PUT-запрос для обновления файла с обновленными данными
    data_put = {
        'message': 'Обновление файла products.json после удаления данных',
        'content': base64.b64encode(updated_json_data.encode()).decode(),
        'sha': sha
    }

    response_put = requests.put(url, headers=headers, data=json.dumps(data_put))
    assert response_put.status_code == 200, f"Ошибка при обновлении файла после удаления данных. Код: {response_put.status_code}"

def test_get_data_after_delete():
    # Тестирование получения данных после удаления (GET)
    response_get_after_delete = requests.get(url, headers=headers)
    assert response_get_after_delete.status_code == 200, f"Ошибка при получении данных после удаления. Код: {response_get_after_delete.status_code}"

    # Декодируем содержимое из Base64 с явным указанием кодировки
    decoded_content_after_delete = base64.b64decode(response_get_after_delete.content).decode('utf-8', errors='replace')

    try:
        products_data_after_delete = json.loads(decoded_content_after_delete)
    except json.JSONDecodeError:
        assert False, "Ошибка при декодировании JSON."

    # Добавьте проверку, что элементы действительно удалены (например, длина списка)
    assert len(products_data_after_delete) == len(products_data) - 2, "Элементы не были удалены успешно."

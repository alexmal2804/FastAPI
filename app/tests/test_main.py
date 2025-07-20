import pytest


"""
def test_calculate_sum(client):
    # Тест 1: валидные входные данные
    response = client.get("/sum/", params={"a": 5, "b": 10})
    assert response.status_code == 200
    assert response.json() == {"result": 15}

    # Тест 2: отрицательные числа
    response = client.get("/sum/", params={"a": -8, "b": -3})
    assert response.status_code == 200
    assert response.json() == {"result": -11}

    # Тест 3: ноль и положительное число
    response = client.get("/sum/", params={"a": 0, "b": 7})
    assert response.status_code == 200
    assert response.json() == {"result": 7}

    # Тест 4: одно число не введено
    response = client.get("/sum/", params={"a": 3})
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["query", "b"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }

"""


@pytest.mark.parametrize(
    "a, b, expected_status, expected_result",
    [
        (5, 10, 200, 15),
        (-8, -3, 200, -11),
        (0, 7, 200, 7),
        ("a", 10, 422, None),  # Ошибка валидации: строка вместо числа
        (3, None, 422, None),  # Отсутствует параметр b
    ],
)
def test_calculate_sum_params(a, b, expected_status, expected_result, client):
    params = {"a": a}
    if b is not None:
        params["b"] = b

    response = client.get("/sum/", params=params)
    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.json() == {"result": expected_result}


def test_calculate_sum_error(client):
    try:
        response = client.get("/sum/", params={"a": 10, "b": 10})
        response.raise_for_status()
    except Exception as e:
        pytest.fail(f"Тест не прошел: {e}")

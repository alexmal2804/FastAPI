from typing import Annotated

from fastapi import FastAPI, Path, Query


app = FastAPI()

sample_product_1 = {
    "product_id": 123,
    "name": "Smartphone",
    "category": "Electronics",
    "price": 599.99,
}

sample_product_2 = {
    "product_id": 456,
    "name": "Phone Case",
    "category": "Accessories",
    "price": 19.99,
}

sample_product_3 = {
    "product_id": 789,
    "name": "Iphone",
    "category": "Electronics",
    "price": 1299.99,
}

sample_product_4 = {
    "product_id": 101,
    "name": "Headphones",
    "category": "Accessories",
    "price": 99.99,
}

sample_product_5 = {
    "product_id": 202,
    "name": "Smartwatch",
    "category": "Electronics",
    "price": 299.99,
}

sample_products = [
    sample_product_1,
    sample_product_2,
    sample_product_3,
    sample_product_4,
    sample_product_5,
]


@app.get("/product/{product_id}")
def get_product(product_id: Annotated[int, Path(ge=1)]):  # type: ignore
    return [product for product in sample_products if product["product_id"] == product_id]


@app.get("/products/search")
def search_product(
    keyword: Annotated[str, Query()],
    category: Annotated[str, Query()] | None = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
):
    # Начинаем с копии полного списка продуктов
    results = sample_products[:]

    # Фильтруем по ключевому слову (поиск подстроки без учета регистра)
    results = [product for product in results if keyword.lower() in product["name"].lower()]

    # Если категория указана, дополнительно фильтруем по ней
    if category:
        results = [product for product in results if product["category"].lower() == category.lower()]
    # Применяем лимит к финальному списку
    return results[:limit]

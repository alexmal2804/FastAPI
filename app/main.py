from fastapi import FastAPI


app = FastAPI()


@app.get("/sum/")
async def calculate_sum(a: int, b: int):
    """
    Calculate the sum of two numbers.
    """
    return {"result": a + b}

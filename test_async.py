import pytest
import aiohttp
import aiosqlite
import asyncio

# Тест 1: Проверка значения
@pytest.mark.asyncio
async def test_resolves_expected_value():
    async def async_function():
        return 42
    result = await async_function()
    assert result == 42

# Тест 2: Проверка исключения
@pytest.mark.asyncio
async def test_rejects_with_expected_exception():
    async def async_function():
        raise ValueError("Expected error")
    with pytest.raises(ValueError, match="Expected error"):
        await async_function()

# Тест 3: HTTP запрос
@pytest.mark.asyncio
async def test_http_request_to_api():
    async def fetch_data():
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.github.com") as response:
                return await response.json()
    data = await fetch_data()
    assert "current_user_url" in data

# Тест 4: Работа с базой данных
@pytest.mark.asyncio
async def test_database_insert():
    async with aiosqlite.connect(":memory:") as db:
        await db.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, value TEXT)")
        await db.execute("INSERT INTO test (value) VALUES (?)", ("TestValue",))
        await db.commit()
        async with db.execute("SELECT value FROM test WHERE id = 1") as cursor:
            row = await cursor.fetchone()
            assert row[0] == "TestValue"

# Тест 5: Асинхронная функция в потоке
@pytest.mark.asyncio
async def test_async_function_in_thread():
    async def async_task():
        await asyncio.sleep(1)
        return "Completed"
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, asyncio.run, async_task())
    assert result == "Completed"

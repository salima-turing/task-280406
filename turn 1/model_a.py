import asyncio
import unittest
from unittest import IsolatedAsyncioTestCase


class AsyncDataAccessLayer:
    async def has_access(self, user_id, resource_id):
        # Simulate asynchronous data access logic
        access_grants = {
            "user1": ["resource1", "resource2"],
            "user2": ["resource3"],
        }

        await asyncio.sleep(0.1)  # Simulate delay
        return resource_id in access_grants.get(user_id, [])


class TestDataAccessRights(IsolatedAsyncioTestCase):
    async def test_has_access_positive(self):
        layer = AsyncDataAccessLayer()
        result = await layer.has_access("user1", "resource1")
        self.assertTrue(result)

    async def test_has_access_negative(self):
        layer = AsyncDataAccessLayer()
        result = await layer.has_access("user1", "resource3")
        self.assertFalse(result)

    async def test_has_access_non_existent_user(self):
        layer = AsyncDataAccessLayer()
        result = await layer.has_access("user3", "resource1")
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()

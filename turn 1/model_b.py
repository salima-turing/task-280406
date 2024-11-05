import asyncio
import pytest


class ReactiveDataStore:
    def __init__(self):
        self.data = {}
        self.access_control = {}

    async def set_data(self, key, value, user_id):
        # Simulate asynchronous operation
        await asyncio.sleep(0.1)
        if user_id in self.access_control[key]:
            self.data[key] = value
            return True
        else:
            return False

    async def get_data(self, key, user_id):
        # Simulate asynchronous operation
        await asyncio.sleep(0.1)
        if user_id in self.access_control[key]:
            return self.data[key]
        else:
            return None

    def add_user_access(self, key, user_id):
        if key not in self.access_control:
            self.access_control[key] = set()
        self.access_control[key].add(user_id)

    def remove_user_access(self, key, user_id):
        if key in self.access_control and user_id in self.access_control[key]:
            self.access_control[key].remove(user_id)


@pytest.mark.asyncio
async def test_real_time_access_control():
    store = ReactiveDataStore()
    user1_id = 1
    user2_id = 2
    data_key = "secret_data"

    # Add user access
    store.add_user_access(data_key, user1_id)

    # Test set_data access (positive)
    assert await store.set_data(data_key, "Top secret!", user1_id) == True

    # Test set_data access (negative)
    assert await store.set_data(data_key, "Top secret!", user2_id) == False

    # Test get_data access (positive)
    data = await store.get_data(data_key, user1_id)
    assert data == "Top secret!"

    # Test get_data access (negative)
    data = await store.get_data(data_key, user2_id)
    assert data is None

    # Add user access and test again
    store.add_user_access(data_key, user2_id)
    assert await store.get_data(data_key, user2_id) == "Top secret!"

    # Remove user access and test again
    store.remove_user_access(data_key, user2_id)
    assert await store.get_data(data_key, user2_id) is None


if __name__ == "__main__":
    pytest.main()

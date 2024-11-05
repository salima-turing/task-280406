import asyncio
import aiostream

# Event stream of user login events
user_login_events = aiostream.stream.Stream()

# Event stream of data access events
data_access_events = aiostream.stream.Stream()

# Access control rules stream
access_rules_stream = aiostream.stream.Stream()


async def apply_access_control():
    async for event in user_login_events:
        user_id = event['user_id']
        rules = await access_rules_stream.filter(lambda rule: rule['user_id'] == user_id).collect()
        print(f"User {user_id} has access rights: {rules}")

    async for event in data_access_events:
        data_key = event['data_key']
        user_id = event['user_id']
        rules = await access_rules_stream.filter(lambda rule: rule['data_key'] == data_key).collect()
        for rule in rules:
            if user_id in rule['allowed_users']:
                print(f"Access granted to User {user_id} for Data {data_key}")
                break
        else:
            print(f"Access denied to User {user_id} for Data {data_key}")


async def main():
    await asyncio.gather(
        apply_access_control(),
        user_login_events.send({'user_id': 1}),
        access_rules_stream.send({'user_id': 1, 'data_key': 'secret_data', 'allowed_users': [1, 3]}),
        data_access_events.send({'data_key': 'secret_data', 'user_id': 1}),
        data_access_events.send({'data_key': 'secret_data', 'user_id': 2}),
    )


asyncio.run(main())

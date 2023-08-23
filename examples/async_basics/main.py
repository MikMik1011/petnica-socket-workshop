import asyncio

async def printTimeout(text, timeout):
    await asyncio.sleep(timeout)
    print(text)

async def main():
    print(1)
    asyncio.create_task(printTimeout(2, 2))
    print(3)
    await printTimeout(4, 3)
    # tweak the timeout values to see how the output changes

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(main())
import aiofiles


class GPIO:
    @classmethod
    async def read(cls, gpio_num):
        async with aiofiles.open(
            f"/sys/class/gpio/gpio{gpio_num}/value", 'r'
        ) as f:
            return await f.read()

    @classmethod
    async def write(cls, command, value):
        async with aiofiles.open(f"/sys/class/gpio/{command}", 'w') as f:
            await f.write(value)

    @classmethod
    async def export(cls, gpio_num):
        await cls.write('export', gpio_num)

    @classmethod
    async def unexport(cls, gpio_num):
        await cls.write('unexport', gpio_num)


class Pin:
    def __init__(self, number):
        self.number = number

    async def as_input(self):
        self._direction = 'in'
        await GPIO.export(self.number)
        await GPIO.write(f"gpio{self.number}/direction", self._direction)

    async def as_output(self):
        self._direction = 'out'
        await GPIO.export(self.number)
        await GPIO.write(f"gpio{self.number}/direction", self._direction)

    async def on(self):
        await GPIO.write(f"gpio{self.number}/value", 1)

    async def off(self):
        await GPIO.write(f"gpio{self.number}/value", 0)

    async def read(self):
        return await GPIO.read(self.number)

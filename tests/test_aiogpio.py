
import sys
import os
import pytest
import aiofiles
from asynctest import patch, CoroutineMock

from aiogpio import GPIO, Pin

# Path config
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

aiofiles.threadpool.wrap.register(CoroutineMock)(
    lambda *x, **y: aiofiles.threadpool.AsyncBufferedIOBase(*x, **y)
)


class TestGPIO:
    @pytest.mark.asyncio
    async def test_read(self):
        mock = CoroutineMock()
        with patch(
            'aiofiles.threadpool.sync_open', return_value=mock
        ) as open_mock:
            await GPIO.read(1)
            open_mock.assert_called_once_with(
                '/sys/class/gpio/gpio1/value', mode='r', buffering=-1,
                closefd=True, encoding=None, errors=None,
                newline=None, opener=None
            )
            mock.read.assert_called_once()

    @pytest.mark.asyncio
    async def test_write(self):
        mock = CoroutineMock()
        with patch(
            'aiofiles.threadpool.sync_open', return_value=mock
        ) as open_mock:
            await GPIO.write('command', 'value')
            open_mock.assert_called_once_with(
                '/sys/class/gpio/command', mode='w', buffering=-1,
                closefd=True, encoding=None, errors=None,
                newline=None, opener=None
            )
            mock.write.assert_called_once_with('value')

    @pytest.mark.asyncio
    async def test_export(self):
        with patch('aiogpio.GPIO.write') as write_mock:
            await GPIO.export('gpio_num')
            write_mock.assert_called_once_with('export', 'gpio_num')

    @pytest.mark.asyncio
    async def test_unexport(self):
        with patch('aiogpio.GPIO.write') as write_mock:
            await GPIO.unexport('gpio_num')
            write_mock.assert_called_once_with('unexport', 'gpio_num')


class TestPin:
    @pytest.mark.asyncio
    async def test_as_input(self):
        with patch('aiogpio.GPIO.export') as export_mock:
            with patch('aiogpio.GPIO.write') as write_mock:
                test_pin = Pin(1)
                await test_pin.as_input()
                export_mock.assert_called_once_with(1)
                write_mock.assert_called_once_with('gpio1/direction', 'in')
                assert test_pin._direction == 'in'

    @pytest.mark.asyncio
    async def test_as_output(self):
        with patch('aiogpio.GPIO.export') as export_mock:
            with patch('aiogpio.GPIO.write') as write_mock:
                test_pin = Pin(1)
                await test_pin.as_output()
                export_mock.assert_called_once_with(1)
                write_mock.assert_called_once_with('gpio1/direction', 'out')
                assert test_pin._direction == 'out'

    @pytest.mark.asyncio
    async def test_on(self):
        with patch('aiogpio.GPIO.write') as write_mock:
            test_pin = Pin(1)
            await test_pin.on()
            write_mock.assert_called_once_with('gpio1/value', 1)

    @pytest.mark.asyncio
    async def test_off(self):
        with patch('aiogpio.GPIO.write') as write_mock:
            test_pin = Pin(1)
            await test_pin.off()
            write_mock.assert_called_once_with('gpio1/value', 0)

    @pytest.mark.asyncio
    async def test_read(self):
        with patch('aiogpio.GPIO.read') as read_mock:
            test_pin = Pin(1)
            await test_pin.read()
            read_mock.assert_called_once_with(1)

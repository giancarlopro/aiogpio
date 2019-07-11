# Path config
import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

import pytest
from asynctest import patch, CoroutineMock
import asyncio
import aiofiles

aiofiles.threadpool.wrap.register(CoroutineMock)(
    lambda *args, **kwargs: aiofiles.threadpool.AsyncBufferedIOBase(*args, **kwargs))

from aiogpio import GPIO


class TestGPIO:
    @pytest.mark.asyncio
    async def test_read(self):
        mock = CoroutineMock()
        with patch('aiofiles.threadpool.sync_open', return_value=mock) as open_mock:
            await GPIO.read(1)
            open_mock.assert_called_once_with(
                '/sys/class/gpio/gpio1/value', mode='r', buffering=-1,
                closefd=True, encoding=None, errors=None, newline=None, opener=None
            )
            mock.read.assert_called_once()

    @pytest.mark.asyncio
    async def test_write(self):
        mock = CoroutineMock()
        with patch('aiofiles.threadpool.sync_open', return_value=mock) as open_mock:
            await GPIO.write('command', 'value')
            open_mock.assert_called_once_with(
                '/sys/class/gpio/command', mode='w', buffering=-1,
                closefd=True, encoding=None, errors=None, newline=None, opener=None
            )
            mock.write.assert_called_once_with('value')

    @pytest.mark.asyncio
    async def test_export(self):
        # with patch('aiogpio.GPIO.write', new=CoroutineMock) as write_mock:
        #     GPIO.export('gpio_num')
        #     write_mock.assert_called_once_with('export', 'gpio_num')
        pass

    @pytest.mark.asyncio
    async def test_unexport(self):
        pass

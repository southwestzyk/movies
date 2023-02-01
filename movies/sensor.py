# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from requests import request
import re
import asyncio
import logging
import voluptuous as vol
from datetime import timedelta
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import (PLATFORM_SCHEMA)
from homeassistant.const import (CONF_NAME)

__version__ = '0.1.0'
_LOGGER = logging.getLogger(__name__)

REQUIREMENTS = ['requests', 'beautifulsoup4']
SCAN_INTERVAL = timedelta(hours=8)
ICON = 'mdi:movie-roll'


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_NAME): cv.string,
})


async def async_setup_platform(hass, config, async_add_devices, discovery_info=None):
    _LOGGER.info("async_setup_platform sensor MoviesSensor")
    async_add_devices([MoviesSensor(name=config[CONF_NAME])], True)

class MoviesSensor(Entity):
    def __init__(self, name: str):
        self._name = name
        self._state = None
        self._entries = {}

    def update(self):
        _LOGGER.info("get info from https://m.maoyan.com/asgard/board/1")
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36'
        }
        response = request('GET', 'https://m.maoyan.com/asgard/board/1', headers=header)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, "lxml")
        date = soup.select('div[class="date"] > div[class="number"]')
        self._entries["update_time"] = date[0].text
        trs = soup.select('div[class="board-card clearfix"]')
        self._state = len(trs)
        rank_num = 1
        for tr in trs:
            self._entries[str(rank_num)] = tr.select('h3[class = "title"]')[0].text
            rank_num = rank_num + 1
            #entryValue = {}
            #name = tr.select('h3[class = "title"]')[0].text
            #entryValue["name"] = name
            #actors = tr.select('div[class = "actors"]')[0].text
            #entryValue["actors"] = actors
            #date = tr.select('div[class = "date"]')[0].text
            #entryValue["date"] = date
            #lastNum = tr.select('span[class = "number"]')[0].text + "万"
            #entryValue["lastNum"] = lastNum
            #self._entries.append(entryValue)

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def icon(self):
        return ICON

    @property
    def extra_state_attributes(self):
        return self._entries

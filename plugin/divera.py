#!/usr/bin/python
# -*- coding: utf-8 -*-
"""!
    ____  ____  ______       __      __       __       _____
   / __ )/ __ \/ ___/ |     / /___ _/ /______/ /_     |__  /
  / __  / / / /\__ \| | /| / / __ `/ __/ ___/ __ \     /_ <
 / /_/ / /_/ /___/ /| |/ |/ / /_/ / /_/ /__/ / / /   ___/ /
/_____/\____//____/ |__/|__/\__,_/\__/\___/_/ /_/   /____/
                German BOS Information Script
                     by Bastian Schroll

@file:        divera.py
@date:        16.01.2022
@author:      Lars Gremme
@description: Divera247 Plugin
"""
import logging
from plugin.pluginBase import PluginBase

# ###################### #
# Custom plugin includes #
import asyncio
from aiohttp import ClientSession
import urllib
# ###################### #

logging.debug("- %s loaded", __name__)


class BoswatchPlugin(PluginBase):
    """!Description of the Plugin"""
    def __init__(self, config):
        """!Do not change anything here!"""
        super().__init__(__name__, config)  # you can access the config class on 'self.config'

    def fms(self, bwPacket):
        """!Called on FMS alarm

        @param bwPacket: bwPacket instance
        Remove if not implemented"""
        apicall = urllib.parse.urlencode({
                                "accesskey": self.config.get("accesskey", default=""),
                                "vehicle_ric": self.parseWildcards(self.config.get("vehicle", default="")),
                                "status_id": bwPacket.get("status"),
                                "status_note": bwPacket.get("directionText"),
                                "title": self.parseWildcards(self.config.get("title_fms", default="{FMS}")),
                                "text": self.parseWildcards(self.config.get("message_fms", default="{FMS}")),
                                "priority": self.config.get("priority", default="FALSE"),
                            })
        apipath = "/api/fms"
        self.makeRequests(self, apipath, apicall)

    def pocsag(self, bwPacket):
        """!Called on POCSAG alarm

        @param bwPacket: bwPacket instance
        Remove if not implemented"""
        apicall = urllib.parse.urlencode({
                                "accesskey": self.config.get("accesskey", default=""),
                                "title": self.parseWildcards(self.config.get("title_pocsag", default="{RIC}({SRIC})\n{MSG}")),
                                "ric": self.parseWildcards(self.config.get("ric_pocsag", default="")),
                                "text": self.parseWildcards(self.config.get("message_pocsag", default="{MSG}")),
                                "priority": self.config.get("priority", default="FALSE"),
                            })
        apipath = "/api/alarm"
        self.makeRequests(self, apipath, apicall)

    def zvei(self, bwPacket):
        """!Called on ZVEI alarm

        @param bwPacket: bwPacket instance
        Remove if not implemented"""
        apicall = urllib.parse.urlencode({
                                "accesskey": self.config.get("accesskey", default=""),
                                "title": self.parseWildcards(self.config.get("title_zvei", default="{TONE}")),
                                "ric": self.parseWildcards(self.config.get("ric_zvei", default="{TONE}")),
                                "text": self.parseWildcards(self.config.get("message_zvei", default="{TONE}")),
                                "priority": self.config.get("priority", default="FALSE"),
                            })
        apipath = "/api/alarm"
        self.makeRequests(self, apipath, apicall)

    def msg(self, bwPacket):
        """!Called on MSG packet

        @param bwPacket: bwPacket instance
        Remove if not implemented"""
        apicall = urllib.parse.urlencode({
                                "accesskey": self.config.get("accesskey", default=""),
                                "title": self.parseWildcards(self.config.get("title_msg", default="{MSG}")),
                                "ric": self.parseWildcards(self.config.get("ric_msg", default="")),
                                "text": self.parseWildcards(self.config.get("message_msg", default="{MSG}")),
                                "priority": self.config.get("priority", default="FALSE"),
                            })
        apipath = "/api/alarm"
        self.makeRequests(self, apipath, apicall)

    def makeRequests(self, apipath, apicall):
        """Parses wildcard urls and handles asynchronus requests

        @param urls: array of urls"""
        url = "https://www.divera247.com"
        request = url + apipath + "?" + apicall

        loop = asyncio.get_event_loop()

        future = asyncio.ensure_future(self.asyncRequests(request))
        loop.run_until_complete(future)

    async def asyncRequests(self, urls):
        """Handles asynchronus requests

        @param urls: array of urls to send requests to"""
        tasks = []

        async with ClientSession() as session:
            for url in urls:
                task = asyncio.ensure_future(self.fetch(url, session))
                tasks.append(task)

            responses = asyncio.gather(*tasks)
            await responses

    async def fetch(self, url, session):
        """Fetches requests

        @param url: url

        @param session: Clientsession instance"""
        async with session.get(url) as response:
            logging.info("{} returned [{}]".format(response.url, response.status))
            return await response.read()

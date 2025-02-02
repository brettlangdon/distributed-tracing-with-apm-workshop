#!/usr/local/bin/python
from ddtrace import tracer, patch, Pin
tracer.configure(hostname='agent')
patch(futures=True, asyncio=True)

import asyncio
import argparse
from requests_threads import AsyncSession

import logging
logger = logging.getLogger()

parser = argparse.ArgumentParser(description='Concurrent Traffic Generator')
parser.add_argument('concurrent', type=int, help='Number of Concurrent Requests')
parser.add_argument('total', type=int, help='Total number of Requests to Make')
parser.add_argument('url', type=str, help='URL to fetch')
args = parser.parse_args()

asyncio.set_event_loop(asyncio.new_event_loop())

session = AsyncSession(n=args.concurrent)
Pin.override(session, service='concurrent-requests-generator')


async def generate_requests():
    with tracer.trace('flask.request', service='concurrent-requests-generator'):
        rs = []
        for _ in range(args.total):
            rs.append(session.get(args.url))
        for i in range(args.total):
            rs[i] = await rs[i]
        print(rs)


session.run(generate_requests)
session.close()

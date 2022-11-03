import asyncio
from json import JSONDecodeError

from fastapi import WebSocket
from pydantic import ValidationError

from .schemas import ErrorResponse, HouseRequest, HouseBase, HouseAnalogAdjustments
from .internal.errors import ParseError
from .internal.house_processing import calculate_adjustments
from .parsers.avito import AvitoParser
from app import config

async def searcher_endpoint(ws: WebSocket):
    await ws.accept()

    houses: list[tuple[HouseBase, HouseAnalogAdjustments]] = []

    try:
        req_json = await asyncio.wait_for(
            ws.receive_json(),
            config.SEARCHER_QUERY_TIMEOUT
        )
    except TimeoutError:
        await ws.send_json(
            ErrorResponse(error='Request wait timeout').dict(exclude_none=True)
        )
        await ws.close()
        return
    except JSONDecodeError:
        await ws.send_json(
            ErrorResponse(error='JSON parse error').dict(exclude_none=True)
        )
        await ws.close()
        return
    except Exception:
        await ws.send_json(
            ErrorResponse(error='Unresolved error').dict(exclude_none=True)
        )
        await ws.close()
        return
    
    try:
        req = HouseRequest.parse_obj(req_json)
    except ValidationError:
        await ws.send_json(
            ErrorResponse(error='Invalid request').dict(exclude_none=True)
        )
        await ws.close()
        return
    
    id_counter = 0
    async with AvitoParser(req.house.location) as parser:
        while len(houses) < req.max_house_count:
            try:
                house = await parser.parse_next()
            except ParseError:
                continue
        
            if house is None:
                break

            house.id = id_counter
            id_counter += 1

            houses.append((
                house,
                calculate_adjustments(req.house, house, req.adjustments)
            ))
            houses.sort(key=lambda t: t[1].calc_size())

            await ws.send_json(list(map(lambda t: t[0].dict(), houses)))

    await ws.close()

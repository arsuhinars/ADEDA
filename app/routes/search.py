from fastapi import APIRouter

from ..parsers.avito import AvitoParser
from ..schemas import House

router = APIRouter(
    prefix='',
    tags=['search']
)

@router.get('/start_searching', response_model=House, summary='Начать поиск квартир')
async def start_searching():
    async with AvitoParser() as parser:
        house = await parser.parse_next()
        return house

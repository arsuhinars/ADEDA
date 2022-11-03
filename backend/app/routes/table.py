from io import BytesIO
from fastapi import APIRouter, File, Depends
from fastapi.responses import StreamingResponse
from pydantic import ValidationError
from openpyxl import load_workbook

from ..internal.errors import ParseError
from ..schemas import HouseBase, HouseBrief, \
    HouseSegment, HouseMaterial, HouseState
from ..dependencies import check_authorization

router = APIRouter(
    prefix='/table',
    tags=['table']
)

@router.post(
    '/parse',
    response_model=list[HouseBrief],
    response_model_exclude_none=True,
    dependencies=[Depends(check_authorization)]
    )
def parse_house_table(file: bytes = File()):
    try:
        with BytesIO(file) as stream:
            wb = load_workbook(stream)
    except Exception as err:
        raise ParseError('Unable to load table')
    ws = wb[wb.sheetnames[0]]

    houses: list[HouseBrief] = []

    for row in ws.iter_rows(2, max_col=11):
        # Сегмент дома
        if type(row[2].value) is not str:
            raise ParseError(
                f'Unable to parse house segment at {row[2].coordinate}'
            )

        match row[2].value.strip().lower():
            case 'новостройка':
                segment = HouseSegment.NEW
            case 'современное жилье':
                segment = HouseSegment.MODERN
            case 'старый жилой фонд':
                segment = HouseSegment.OLD
            case _:
                raise ParseError(
                    f'Unable to parse house segment at {row[2].coordinate}'
                )
        
        # Материал стен
        if type(row[4].value) is not str:
            raise ParseError(
                f'Unable to parse wall material at {row[4].coordinate}'
            )
        
        match row[4].value.strip().lower():
            case 'кирпич':
                material = HouseMaterial.BRICK
            case 'панель':
                material = HouseMaterial.PANEL
            case 'монолит':
                material = HouseMaterial.MONOLIT
            case _:
                raise ParseError(
                    f'Unable to parse wall material at {row[4].coordinate}'
                )
        
        # Наличие балкона/лоджии
        if type(row[8].value) is not str:
            raise ParseError(
                f'Unable to parse balcony at {row[8].coordinate}'
            )
        
        match row[8].value.strip().lower():
            case 'да':
                has_balcony = True
            case 'нет':
                has_balcony = False
            case _:
                raise ParseError(
                    f'Unable to parse balcony at {row[8].coordinate}'
                )
        
        # Состояние дома
        if type(row[10].value) is not str:
            raise ParseError(
                f'Unable to parse house state at {row[10].coordinate}'
            )
        
        match row[10].value.strip().lower():
            case 'без отделки':
                state = HouseState.NO_DECORATION
            case 'муниципальный ремонт':
                state = HouseState.STATE_DECORATION
            case 'современная отделка':
                state = HouseState.MODERN_DECORATION
            case _:
                raise ParseError(
                    f'Unable to parse house state at {row[10].coordinate}'
                )
        
        try:
            houses.append(HouseBrief(
                location=row[0].value,
                rooms_count=row[1].value,
                segment=segment,
                floors_count=row[3].value,
                material=material,
                floor=row[5].value,
                flat_area=row[6].value,
                kitchen_area=row[7].value,
                has_balcony=has_balcony,
                metro_distance=row[9].value,
                state=state
            ))
        except ValidationError as err:
            raise ParseError(str(err))

    return houses


@router.post('/create', dependencies=[Depends(check_authorization)])
def create_house_table(houses: list[HouseBase]):
    # wb = Workbook()

    return StreamingResponse()

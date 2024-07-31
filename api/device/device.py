import logging

from fastapi import APIRouter, Depends, Request, status, Response, FastAPI
from psycopg.rows import dict_row

from api.device.model import Device
from utils.user_permissions import CheckUserPermissions
from utils.model import UserID

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

router = APIRouter()
app = FastAPI()
@router.get('/device/{device_id}', status_code=status.HTTP_200_OK, name="Get device by device_id", response_model=list[Device])
async def get_device(device_id, request: Request):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT * 
                FROM device.devices WHERE device_id = %s""", (device_id,)
                              )
            results = await cur.fetchall()
            logger.info(results)
            return results


@router.post('/devices', status_code=status.HTTP_200_OK, name="Get all devices", response_model=list[Device])
async def get_devices(
        user: UserID,
        request: Request,
        authorize: bool = Depends(CheckUserPermissions(required_permissions='get_devices'))                  
    ):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT * 
                FROM device.devices"""
                              )
            results = await cur.fetchall()
            logger.info(results)
            return results

@router.post('/device', status_code=status.HTTP_201_CREATED, name="create a device")
async def create_device(device: Device, request: Request):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                INSERT INTO
                device.devices (device_name, device_id)
                VALUES (%s, %s)""", (device.device_name, device.device_id)
            )

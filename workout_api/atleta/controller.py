from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter, Body, status
from workout_api.atleta.models import AtletaModel
from workout_api.atleta.schemas import AtletaIn, AtletaOut
from workout_api.contrib.dependencies import DatabaseDependecy

router = APIRouter()

@router.post(
        '/', 
        sumary='Criar um novo atleta',
        status_code = status.HTTP_201_CREATED,
        response_model=AtletaOut
)
async def post(
    db_session: DatabaseDependecy,
    atleta_in: AtletaIn =  Body(...)
):
    atleta_out = AtletaOut(id=uuid4(), created_at=datetime.utcnow(), **atleta_in.model_dump())
    atleta_model = AtletaModel(**atleta_out.model_dump())

    db_session.add(atleta_model)
    await db_session.conmit()

    return atleta_out

from http.client import HTTPException
from uuid import uuid4

from pydantic import UUID4
from fastapi import APIRouter, Body, status
from workout_api.centro_treinamento.schemas import CentroTreinamentoIn, CentroTreinamentoOut
from workout_api.centro_treinamento.models import CentroTreinamentoModel

from workout_api.contrib.dependencies import DatabaseDependecy
from sqlalchemy.future import select

router = APIRouter()

@router.post(
        '/', 
        sumary='Criar um novo centro de treinamento',
        status_code=status.HTTP_201_CREATED,
        response_model = CentroTreinamentoOut
)
async def post(
    db_session: DatabaseDependecy,
    centro_treinamento_in: CentroTreinamentoIn =  Body(...)
) -> CentroTreinamentoOut:
    centro_treinamento_out = CentroTreinamentoOut(id=uuid4(), **centro_treinamento_in.model_dump())
    centro_treinamento_model = CentroTreinamentoModel(**centro_treinamento_out.model_dump())

    db_session.add(centro_treinamento_model)
    await db_session.conmit()

    return centro_treinamento_out

@router.get(
        '/', 
        sumary='Consultar todos os centos de treinamento',
        status_code=status.HTTP_200_OK,
        response_model = list[CentroTreinamentoOut]
)
async def query(db_session: DatabaseDependecy) -> list[CentroTreinamentoOut]:
    centros_treinamento_out: list[CentroTreinamentoOut] = (await db_session.execute(select(CentroTreinamentoModel))).scalars().all()

    return centros_treinamento_out

@router.get(
        '/{id}', 
        sumary='Consulta um novo centro de treinamento pelo ID',
        status_code=status.HTTP_200_OK,
        response_model = CentroTreinamentoOut
)
async def query(id: UUID4, db_session: DatabaseDependecy) -> CentroTreinamentoOut:
    centro_treinamento_out: CentroTreinamentoOut = (
        await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id))
    ).scalars().first()
    
    if not centro_treinamento_Out:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Centro de treinamento não encontrada nesse id: {id}'
        )

    return centro_treinamento_out
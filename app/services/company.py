from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from entities.company import Company
from models.company import CreateCompanyModel, SearchCompanyModel, UpdateCompanyModel
from services.utils import get_current_utc_time
from services.exception import ResourceNotFoundError

async def get_all_companies(conds: SearchCompanyModel, db: AsyncSession) -> list[Company]:
    query = select(Company)
    
    if conds.name is not None:
        query = query.filter(Company.name.like(f"{conds.name}%"))
    if conds.description is not None:
        query = query.filter(Company.description.like(f"{conds.description}%"))
    if conds.mode is not None:
        query = query.filter(Company.mode == conds.mode)
    query = query.filter(Company.rating >= conds.rating)
    
    query = query.offset((conds.page-1)*conds.size).limit(conds.size)
    
    result = await db.scalars(query)
    
    return result.all()

async def get_company_by_id(company_id: int, db: AsyncSession) -> Company:
    result = await db.scalars(select(Company).filter(Company.id == company_id))
    return result.first()

async def add_new_company(data: CreateCompanyModel, db: AsyncSession) -> Company:
    company = Company(**data.model_dump())
    
    company.created_at = get_current_utc_time()
    company.updated_at = get_current_utc_time()
    
    db.add(company)
    await db.commit()
    await db.refresh(company)
    
    return company

async def update_company_by_id(company_id: int, data: UpdateCompanyModel, db: AsyncSession) -> Company:
    company = await get_company_by_id(company_id, db)
    
    if company is None:
        raise ResourceNotFoundError()
    
    updated = False
    if data.name is not None:
        company.name = data.name
        updated = True
    if data.description is not None:
        company.description = data.description
        updated = True
    if data.mode is not None:
        company.mode = data.mode
        updated = True
    if data.rating is not None:
        company.rating = data.rating
        updated = True
    if updated:
        company.updated_at = get_current_utc_time()
    
    await db.commit()
    await db.refresh(company)
    
    return company

async def delete_company_by_id(company_id: int, db: AsyncSession) -> None:
    company = await get_company_by_id(company_id, db)
    
    if company is None:
        raise ResourceNotFoundError()
    
    await db.delete(company)
    await db.commit()
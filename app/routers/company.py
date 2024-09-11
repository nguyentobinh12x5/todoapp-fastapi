from starlette import status
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from entities.company import CompanyMode
from database import get_async_db_context
from models.company import CreateCompanyModel, CompanyViewModel, UpdateCompanyModel, SearchCompanyModel
from services import company as CompanyService
from services.exception import ResourceNotFoundError, AccessDeniedError
from services.auth import get_current_user
router = APIRouter(prefix="/companies", tags=["Companies"])

@router.get("", status_code=status.HTTP_200_OK, response_model=list[CompanyViewModel])
async def get_all_companies(
    name: str = Query(default=None),
    description: str = Query(default=None),
    mode: CompanyMode = Query(default=None),
    rating: int = Query(ge=0, le=5, default=0),
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=1, le=50, default=10),
    db: AsyncSession = Depends(get_async_db_context),
    user = Depends(get_current_user)
):
    if not user.get("is_admin"):
        raise AccessDeniedError()  
    conds = SearchCompanyModel(name, description, mode, rating, page, size)
    return await CompanyService.get_all_companies(conds, db)

@router.get("/{company_id}", status_code=status.HTTP_200_OK, response_model=CompanyViewModel)
async def get_company_by_id(
    company_id: int, 
    db: AsyncSession = Depends(get_async_db_context),
    user = Depends(get_current_user)
):
    if not user.get("is_admin"):
        raise AccessDeniedError()  
    
    company = await CompanyService.get_company_by_id(company_id, db)
    
    if company is None:
        raise ResourceNotFoundError()
    
    return company

@router.post("", status_code=status.HTTP_201_CREATED, response_model=CompanyViewModel)
async def add_new_company(
    request: CreateCompanyModel, 
    db: AsyncSession = Depends(get_async_db_context),
    user = Depends(get_current_user)
):
    if not user.get("is_admin"):
        raise AccessDeniedError()  
    return await CompanyService.add_new_company(request, db)

@router.put("/{company_id}", status_code=status.HTTP_200_OK, response_model=CompanyViewModel)
async def update_company_by_id(
    company_id: int,
    request: UpdateCompanyModel,
    db: AsyncSession = Depends(get_async_db_context),
    user = Depends(get_current_user)
):
    if not user.get("is_admin"):
        raise AccessDeniedError()  
    
    return await CompanyService.update_company_by_id(company_id, request, db)

@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company_by_id(
    company_id: int, 
    db: AsyncSession = Depends(get_async_db_context),
    user = Depends(get_current_user)
):
    if not user.get("is_admin"):
        raise AccessDeniedError()  
    
    CompanyService.delete_company_by_id(company_id, db)
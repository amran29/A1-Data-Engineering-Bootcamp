from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.asset import AssetCreate, AssetOut, AssetUpdate
from app.controllers import asset_controller

# استيراد دالة الحماية والموديل
from app.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/assets", tags=["Investment Assets"])

@router.post("/", response_model=AssetOut)
def add_asset(
    asset: AssetCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user) # استخراج المستخدم من التوكن
):
    # نمرر الـ ID الخاص بالمستخدم الذي قام بتسجيل الدخول فعلياً
    return asset_controller.create_asset(db, asset, user_id=current_user.id)

@router.get("/", response_model=List[AssetOut])
def list_assets(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user) # حماية المسار
):
    # هنا الفلترة الحقيقية: جلب أصول المستخدم الحالي فقط
    return asset_controller.get_user_assets(db, user_id=current_user.id)

@router.put("/{asset_id}", response_model=AssetOut)
def update_asset_data(
    asset_id: int, 
    asset_update: AssetUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    # نمرر user_id لضمان أن المستخدم لا يعدل أصول غيره
    updated_asset = asset_controller.update_asset(db, asset_id, asset_update, user_id=current_user.id)
    if not updated_asset:
        raise HTTPException(status_code=404, detail="Asset not found or unauthorized")
    return updated_asset

@router.delete("/{asset_id}")
def delete_asset_data(
    asset_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    # نمرر user_id لضمان أن المستخدم لا يحذف أصول غيره
    success = asset_controller.delete_asset(db, asset_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Asset not found or unauthorized")
    return {"message": "Asset deleted successfully"}
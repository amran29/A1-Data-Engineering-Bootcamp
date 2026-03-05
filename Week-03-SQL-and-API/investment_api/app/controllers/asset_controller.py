from sqlalchemy.orm import Session
from app.models.asset import Asset
from app.schemas.asset import AssetCreate, AssetUpdate

# 1. Create - إضافة أصل جديد
def create_asset(db: Session, asset: AssetCreate, user_id: int):
    db_asset = Asset(**asset.dict(), user_id=user_id)
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset

# 2. Read - جلب أصول المستخدم فقط
def get_user_assets(db: Session, user_id: int):
    return db.query(Asset).filter(Asset.user_id == user_id).all()

# 3. Update - تحديث بيانات أصل (كمية أو سعر)
def update_asset(db: Session, asset_id: int, asset_data: AssetUpdate, user_id: int):
    query = db.query(Asset).filter(Asset.id == asset_id, Asset.user_id == user_id)
    db_asset = query.first()
    
    if db_asset:
        update_data = asset_data.dict(exclude_unset=True) # تحديث الحقول المرسلة فقط
        query.update(update_data)
        db.commit()
        db.refresh(db_asset)
    return db_asset

# 4. Delete - حذف أصل من المحفظة
def delete_asset(db: Session, asset_id: int, user_id: int):
    db_asset = db.query(Asset).filter(Asset.id == asset_id, Asset.user_id == user_id).first()
    if db_asset:
        db.delete(db_asset)
        db.commit()
        return True
    return False
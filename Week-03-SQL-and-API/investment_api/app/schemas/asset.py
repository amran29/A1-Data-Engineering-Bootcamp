from pydantic import BaseModel
from typing import Optional

# النموذج الأساسي
class AssetBase(BaseModel):
    symbol: str
    asset_name: str
    quantity: float
    purchase_price: float

# البيانات المطلوبة عند إضافة أصل جديد
class AssetCreate(AssetBase):
    pass

# البيانات التي ستعود عند عرض المحفظة
class AssetOut(AssetBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

# نموذج خاص بالتحديث (Update) - جميع الحقول اختيارية
class AssetUpdate(BaseModel):
    quantity: Optional[float] = None
    purchase_price: Optional[float] = None
from datetime import datetime
from typing import Optional, List
from bson import ObjectId
from app.database import get_database
from app.schemas.schemas import (
    UserCreate,
    UserInDB,
    ProductCreate,
    ProductUpdate,
    SupplierCreate,
    SupplierUpdate,
    InventoryMovementCreate,
    DashboardStats,
)
from app.services.auth_service import get_password_hash


def serialize_doc(doc):
    if doc is None:
        return None
    doc["id"] = str(doc.pop("_id"))
    return doc


class UserRepository:
    @staticmethod
    async def create_user(user: UserCreate) -> UserInDB:
        db = get_database()
        hashed_password = get_password_hash(user.password)
        user_dict = {
            "email": user.email,
            "username": user.username,
            "full_name": user.full_name,
            "hashed_password": hashed_password,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
        result = await db.users.insert_one(user_dict)
        user_dict["_id"] = result.inserted_id
        return serialize_doc(user_dict)

    @staticmethod
    async def get_user_by_username(username: str) -> Optional[dict]:
        db = get_database()
        user = await db.users.find_one({"username": username})
        return serialize_doc(user) if user else None

    @staticmethod
    async def get_user_by_email(email: str) -> Optional[dict]:
        db = get_database()
        user = await db.users.find_one({"email": email})
        return serialize_doc(user) if user else None


class ProductRepository:
    @staticmethod
    async def create_product(product: ProductCreate) -> dict:
        db = get_database()
        product_dict = product.model_dump()
        product_dict["created_at"] = datetime.utcnow()
        product_dict["updated_at"] = datetime.utcnow()
        result = await db.products.insert_one(product_dict)
        product_dict["_id"] = result.inserted_id
        return serialize_doc(product_dict)

    @staticmethod
    async def get_product_by_id(product_id: str) -> Optional[dict]:
        db = get_database()
        product = await db.products.find_one({"_id": ObjectId(product_id)})
        return serialize_doc(product) if product else None

    @staticmethod
    async def get_all_products() -> List[dict]:
        db = get_database()
        products = await db.products.find().to_list(length=1000)
        return [serialize_doc(p) for p in products]

    @staticmethod
    async def update_product(product_id: str, product: ProductUpdate) -> Optional[dict]:
        db = get_database()
        update_data = {k: v for k, v in product.model_dump().items() if v is not None}
        update_data["updated_at"] = datetime.utcnow()
        await db.products.update_one(
            {"_id": ObjectId(product_id)}, {"$set": update_data}
        )
        return await ProductRepository.get_product_by_id(product_id)

    @staticmethod
    async def delete_product(product_id: str) -> bool:
        db = get_database()
        result = await db.products.delete_one({"_id": ObjectId(product_id)})
        return result.deleted_count > 0

    @staticmethod
    async def get_low_stock_products() -> List[dict]:
        db = get_database()
        products = await db.products.find(
            {"$expr": {"$lte": ["$quantity", "$min_stock"]}}
        ).to_list(length=1000)
        return [serialize_doc(p) for p in products]

    @staticmethod
    async def update_product_quantity(product_id: str, quantity_change: int):
        db = get_database()
        await db.products.update_one(
            {"_id": ObjectId(product_id)},
            {
                "$inc": {"quantity": quantity_change},
                "$set": {"updated_at": datetime.utcnow()},
            },
        )


class SupplierRepository:
    @staticmethod
    async def create_supplier(supplier: SupplierCreate) -> dict:
        db = get_database()
        supplier_dict = supplier.model_dump()
        supplier_dict["created_at"] = datetime.utcnow()
        supplier_dict["updated_at"] = datetime.utcnow()
        result = await db.suppliers.insert_one(supplier_dict)
        supplier_dict["_id"] = result.inserted_id
        return serialize_doc(supplier_dict)

    @staticmethod
    async def get_supplier_by_id(supplier_id: str) -> Optional[dict]:
        db = get_database()
        supplier = await db.suppliers.find_one({"_id": ObjectId(supplier_id)})
        return serialize_doc(supplier) if supplier else None

    @staticmethod
    async def get_all_suppliers() -> List[dict]:
        db = get_database()
        suppliers = await db.suppliers.find().to_list(length=1000)
        return [serialize_doc(s) for s in suppliers]

    @staticmethod
    async def update_supplier(
        supplier_id: str, supplier: SupplierUpdate
    ) -> Optional[dict]:
        db = get_database()
        update_data = {k: v for k, v in supplier.model_dump().items() if v is not None}
        update_data["updated_at"] = datetime.utcnow()
        await db.suppliers.update_one(
            {"_id": ObjectId(supplier_id)}, {"$set": update_data}
        )
        return await SupplierRepository.get_supplier_by_id(supplier_id)

    @staticmethod
    async def delete_supplier(supplier_id: str) -> bool:
        db = get_database()
        result = await db.suppliers.delete_one({"_id": ObjectId(supplier_id)})
        return result.deleted_count > 0


class MovementRepository:
    @staticmethod
    async def create_movement(movement: InventoryMovementCreate) -> dict:
        db = get_database()
        movement_dict = movement.model_dump()
        movement_dict["created_at"] = datetime.utcnow()
        result = await db.inventory_movements.insert_one(movement_dict)
        movement_dict["_id"] = result.inserted_id

        quantity_change = (
            movement.quantity
            if movement.movement_type == "entry"
            else -movement.quantity
        )
        await ProductRepository.update_product_quantity(
            movement.product_id, quantity_change
        )

        return serialize_doc(movement_dict)

    @staticmethod
    async def get_all_movements() -> List[dict]:
        db = get_database()
        movements = (
            await db.inventory_movements.find()
            .sort("created_at", -1)
            .to_list(length=1000)
        )
        return [serialize_doc(m) for m in movements]

    @staticmethod
    async def get_movements_by_product(product_id: str) -> List[dict]:
        db = get_database()
        movements = (
            await db.inventory_movements.find({"product_id": product_id})
            .sort("created_at", -1)
            .to_list(length=1000)
        )
        return [serialize_doc(m) for m in movements]


class DashboardRepository:
    @staticmethod
    async def get_dashboard_stats() -> DashboardStats:
        db = get_database()
        total_products = await db.products.count_documents({})
        total_suppliers = await db.suppliers.count_documents({})
        total_movements = await db.inventory_movements.count_documents({})

        products = await db.products.find().to_list(length=1000)
        total_value = sum(p.get("quantity", 0) * p.get("price", 0) for p in products)

        low_stock = await ProductRepository.get_low_stock_products()

        recent_movements = (
            await db.inventory_movements.find()
            .sort("created_at", -1)
            .limit(10)
            .to_list(length=10)
        )
        recent_movements = [serialize_doc(m) for m in recent_movements]

        entries_count = await db.inventory_movements.count_documents(
            {"movement_type": "entry"}
        )
        exits_count = await db.inventory_movements.count_documents(
            {"movement_type": "exit"}
        )

        return DashboardStats(
            total_products=total_products,
            total_suppliers=total_suppliers,
            total_movements=total_movements,
            total_value=total_value,
            low_stock_products=low_stock,
            recent_movements=recent_movements,
            entries_count=entries_count,
            exits_count=exits_count,
        )

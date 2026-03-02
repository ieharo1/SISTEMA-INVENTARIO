from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.repositories.repository import (
    ProductRepository,
    SupplierRepository,
    MovementRepository,
    DashboardRepository,
)
from app.schemas.schemas import (
    ProductCreate,
    ProductUpdate,
    SupplierCreate,
    SupplierUpdate,
    InventoryMovementCreate,
)

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/dashboard")
async def dashboard(request: Request):
    stats = await DashboardRepository.get_dashboard_stats()
    return templates.TemplateResponse(
        "dashboard.html", {"request": request, "stats": stats}
    )


@router.get("/products")
async def products_page(request: Request):
    products = await ProductRepository.get_all_products()
    suppliers = await SupplierRepository.get_all_suppliers()
    return templates.TemplateResponse(
        "products.html",
        {"request": request, "products": products, "suppliers": suppliers},
    )


@router.post("/products/create")
async def create_product(
    request: Request,
    name: str = Form(...),
    description: str = Form(None),
    sku: str = Form(...),
    price: float = Form(...),
    cost: float = Form(...),
    quantity: int = Form(...),
    min_stock: int = Form(...),
    category: str = Form(None),
):
    product_data = ProductCreate(
        name=name,
        description=description,
        sku=sku,
        price=price,
        cost=cost,
        quantity=quantity,
        min_stock=min_stock,
        category=category,
    )
    await ProductRepository.create_product(product_data)
    return RedirectResponse(url="/products", status_code=303)


@router.post("/products/update/{product_id}")
async def update_product(
    product_id: str,
    request: Request,
    name: str = Form(None),
    description: str = Form(None),
    sku: str = Form(None),
    price: float = Form(None),
    cost: float = Form(None),
    quantity: int = Form(None),
    min_stock: int = Form(None),
    category: str = Form(None),
):
    product_update = ProductUpdate(
        name=name,
        description=description,
        sku=sku,
        price=price,
        cost=cost,
        quantity=quantity,
        min_stock=min_stock,
        category=category,
    )
    await ProductRepository.update_product(product_id, product_update)
    return RedirectResponse(url="/products", status_code=303)


@router.post("/products/delete/{product_id}")
async def delete_product(product_id: str):
    await ProductRepository.delete_product(product_id)
    return RedirectResponse(url="/products", status_code=303)


@router.get("/suppliers")
async def suppliers_page(request: Request):
    suppliers = await SupplierRepository.get_all_suppliers()
    return templates.TemplateResponse(
        "suppliers.html", {"request": request, "suppliers": suppliers}
    )


@router.post("/suppliers/create")
async def create_supplier(
    request: Request,
    name: str = Form(...),
    contact_name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    address: str = Form(...),
    ruc: str = Form(...),
):
    supplier_data = SupplierCreate(
        name=name,
        contact_name=contact_name,
        email=email,
        phone=phone,
        address=address,
        ruc=ruc,
    )
    await SupplierRepository.create_supplier(supplier_data)
    return RedirectResponse(url="/suppliers", status_code=303)


@router.post("/suppliers/update/{supplier_id}")
async def update_supplier(
    supplier_id: str,
    request: Request,
    name: str = Form(None),
    contact_name: str = Form(None),
    email: str = Form(None),
    phone: str = Form(None),
    address: str = Form(None),
    ruc: str = Form(None),
):
    supplier_update = SupplierUpdate(
        name=name,
        contact_name=contact_name,
        email=email,
        phone=phone,
        address=address,
        ruc=ruc,
    )
    await SupplierRepository.update_supplier(supplier_id, supplier_update)
    return RedirectResponse(url="/suppliers", status_code=303)


@router.post("/suppliers/delete/{supplier_id}")
async def delete_supplier(supplier_id: str):
    await SupplierRepository.delete_supplier(supplier_id)
    return RedirectResponse(url="/suppliers", status_code=303)


@router.get("/movements")
async def movements_page(request: Request):
    movements = await MovementRepository.get_all_movements()
    products = await ProductRepository.get_all_products()
    return templates.TemplateResponse(
        "movements.html",
        {"request": request, "movements": movements, "products": products},
    )


@router.post("/movements/create")
async def create_movement(
    request: Request,
    product_id: str = Form(...),
    movement_type: str = Form(...),
    quantity: int = Form(...),
    unit_price: float = Form(...),
    reference: str = Form(None),
    notes: str = Form(None),
):
    movement_data = InventoryMovementCreate(
        product_id=product_id,
        movement_type=movement_type,
        quantity=quantity,
        unit_price=unit_price,
        reference=reference,
        notes=notes,
    )
    await MovementRepository.create_movement(movement_data)
    return RedirectResponse(url="/movements", status_code=303)

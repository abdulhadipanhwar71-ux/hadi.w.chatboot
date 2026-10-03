from pathlib import Path
from typing import Optional
from fastapi import APIRouter, Request, Depends, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models import Order, Customer, Product, Message, AgentHandoff

router = APIRouter(prefix="/admin", tags=["Admin Panel"])

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@router.get("", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    """Admin Dashboard overview with business KPIs and metrics."""
    total_orders = db.query(Order).count()
    pending_orders = db.query(Order).filter(Order.status == "PENDING").count()
    completed_orders = db.query(Order).filter(Order.status == "DELIVERED").count()
    
    total_revenue_query = db.query(func.sum(Order.total_amount)).filter(Order.status != "CANCELLED").scalar()
    total_revenue = total_revenue_query or 0.0

    total_customers = db.query(Customer).count()
    total_products = db.query(Product).count()
    open_handoffs = db.query(AgentHandoff).filter(AgentHandoff.status == "OPEN").count()

    recent_orders = db.query(Order).order_by(Order.created_at.desc()).limit(8).all()
    recent_handoffs = db.query(AgentHandoff).order_by(AgentHandoff.created_at.desc()).limit(5).all()

    context = {
        "request": request,
        "page_title": "Dashboard",
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "completed_orders": completed_orders,
        "total_revenue": total_revenue,
        "total_customers": total_customers,
        "total_products": total_products,
        "open_handoffs": open_handoffs,
        "recent_orders": recent_orders,
        "recent_handoffs": recent_handoffs,
    }
    return templates.TemplateResponse(request=request, name="dashboard.html", context=context)


@router.get("/orders", response_class=HTMLResponse)
async def orders_page(
    request: Request, 
    status_filter: Optional[str] = None, 
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """View, search, and filter orders."""
    query = db.query(Order).order_by(Order.created_at.desc())

    if status_filter and status_filter != "ALL":
        query = query.filter(Order.status == status_filter.upper())
    
    if search:
        search_pattern = f"%{search.strip()}%"
        query = query.filter(
            (Order.order_number.like(search_pattern)) |
            (Order.customer_name.like(search_pattern)) |
            (Order.customer_phone.like(search_pattern))
        )

    orders = query.all()
    context = {
        "request": request,
        "page_title": "Orders Management",
        "orders": orders,
        "current_status": status_filter or "ALL",
        "search_query": search or ""
    }
    return templates.TemplateResponse(request=request, name="orders.html", context=context)


@router.post("/orders/{order_id}/status")
async def update_order_status(
    order_id: int, 
    new_status: str = Form(...), 
    db: Session = Depends(get_db)
):
    """Update order lifecycle status."""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order.status = new_status.upper()
    db.commit()
    return RedirectResponse(url="/admin/orders", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/products", response_class=HTMLResponse)
async def products_page(request: Request, db: Session = Depends(get_db)):
    """List and manage product catalog."""
    products = db.query(Product).order_by(Product.id.asc()).all()
    context = {
        "request": request,
        "page_title": "Product Catalog",
        "products": products
    }
    return templates.TemplateResponse(request=request, name="products.html", context=context)


@router.post("/products/new")
async def add_product(
    code: str = Form(...),
    name_sd: str = Form(...),
    name_ur: str = Form(...),
    name_en: str = Form(...),
    price: float = Form(...),
    category: str = Form("General"),
    description_sd: Optional[str] = Form(""),
    description_ur: Optional[str] = Form(""),
    description_en: Optional[str] = Form(""),
    db: Session = Depends(get_db)
):
    """Add a new product with multilingual fields and price."""
    # Ensure unique code
    existing = db.query(Product).filter(Product.code == code.strip().upper()).first()
    if existing:
        raise HTTPException(status_code=400, detail="Product code already exists")

    product = Product(
        code=code.strip().upper(),
        name_sd=name_sd.strip(),
        name_ur=name_ur.strip(),
        name_en=name_en.strip(),
        price=price,
        category=category.strip(),
        description_sd=description_sd.strip() if description_sd else None,
        description_ur=description_ur.strip() if description_ur else None,
        description_en=description_en.strip() if description_en else None,
        is_available=True
    )
    db.add(product)
    db.commit()
    return RedirectResponse(url="/admin/products", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/products/{product_id}/edit")
async def edit_product(
    product_id: int,
    price: float = Form(...),
    name_sd: str = Form(...),
    name_ur: str = Form(...),
    name_en: str = Form(...),
    category: str = Form(...),
    is_available: bool = Form(False),
    db: Session = Depends(get_db)
):
    """Update price and metadata for a product."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.price = price
    product.name_sd = name_sd.strip()
    product.name_ur = name_ur.strip()
    product.name_en = name_en.strip()
    product.category = category.strip()
    product.is_available = is_available
    db.commit()

    return RedirectResponse(url="/admin/products", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/products/{product_id}/delete")
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Delete a product from catalog."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        db.delete(product)
        db.commit()
    return RedirectResponse(url="/admin/products", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/customers", response_class=HTMLResponse)
async def customers_page(request: Request, db: Session = Depends(get_db)):
    """View registered customers, preferred language, and conversation status."""
    customers = db.query(Customer).order_by(Customer.created_at.desc()).all()
    context = {
        "request": request,
        "page_title": "Customers",
        "customers": customers
    }
    return templates.TemplateResponse(request=request, name="customers.html", context=context)


@router.get("/messages", response_class=HTMLResponse)
async def messages_page(request: Request, db: Session = Depends(get_db)):
    """Audit trail of incoming and outgoing WhatsApp messages."""
    messages = db.query(Message).order_by(Message.timestamp.desc()).limit(100).all()
    context = {
        "request": request,
        "page_title": "Message History",
        "messages": messages
    }
    return templates.TemplateResponse(request=request, name="messages.html", context=context)


@router.post("/agent-handoffs/{handoff_id}/resolve")
async def resolve_handoff(handoff_id: int, db: Session = Depends(get_db)):
    """Resolve an open agent handoff ticket."""
    handoff = db.query(AgentHandoff).filter(AgentHandoff.id == handoff_id).first()
    if handoff:
        handoff.status = "RESOLVED"
        db.commit()
    return RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)

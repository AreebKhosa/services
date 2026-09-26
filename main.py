
from pathlib import Path
from uuid import uuid4
from shutil import copyfileobj

from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from database import Base, engine, SessionLocal, Product

app = FastAPI(
    title="Khanz___subscriptions",
    description="Premium Subscriptions & AI Tools"
)

BASE_DIR = Path(__file__).resolve().parent

UPLOAD_DIR = BASE_DIR / "static" / "uploads" / "products"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

Base.metadata.create_all(bind=engine)

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)

templates = Jinja2Templates(
    directory=BASE_DIR / "templates"
)


@app.get("/")
async def home(request: Request):
    db = SessionLocal()
    try:
        products = db.query(Product).filter(
            Product.active == True
        ).all()

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"products": products}
        )
    finally:
        db.close()


@app.get("/about")
async def about(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="pages/about.html",
        context={}
    )


@app.get("/entertainment")
async def entertainment(request: Request):
    db = SessionLocal()
    try:
        products = db.query(Product).filter(
            Product.category == "Entertainment",
            Product.active == True
        ).all()

        return templates.TemplateResponse(
            request=request,
            name="pages/entertainment.html",
            context={"products": products}
        )
    finally:
        db.close()


@app.get("/ai-tools")
async def ai_tools(request: Request):
    db = SessionLocal()
    try:
        products = db.query(Product).filter(
            Product.category == "AI Tools",
            Product.active == True
        ).all()

        return templates.TemplateResponse(
            request=request,
            name="pages/ai-tools.html",
            context={"products": products}
        )
    finally:
        db.close()


@app.get("/vpn")
async def vpn(request: Request):
    db = SessionLocal()
    try:
        products = db.query(Product).filter(
            Product.category == "VPN",
            Product.active == True
        ).all()

        return templates.TemplateResponse(
            request=request,
            name="pages/vpn.html",
            context={"products": products}
        )
    finally:
        db.close()


@app.get("/services")
async def services(request: Request):
    db = SessionLocal()
    try:
        products = db.query(Product).filter(
            Product.category == "Services",
            Product.active == True
        ).all()

        return templates.TemplateResponse(
            request=request,
            name="pages/services.html",
            context={"products": products}
        )
    finally:
        db.close()


@app.get("/contact")
async def contact(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="pages/contact.html",
        context={}
    )


@app.get("/admin")
async def admin(request: Request):
    db = SessionLocal()
    try:
        products = db.query(Product).order_by(
            Product.id.desc()
        ).all()

        total = db.query(Product).count()

        entertainment_count = db.query(Product).filter(
            Product.category == "Entertainment"
        ).count()

        ai_count = db.query(Product).filter(
            Product.category == "AI Tools"
        ).count()

        vpn_count = db.query(Product).filter(
            Product.category == "VPN"
        ).count()

        services_count = db.query(Product).filter(
            Product.category == "Services"
        ).count()

        active_count = db.query(Product).filter(
            Product.active == True
        ).count()

        return templates.TemplateResponse(
            request=request,
            name="pages/admin.html",
            context={
                "products": products,
                "total": total,
                "entertainment_count": entertainment_count,
                "ai_count": ai_count,
                "vpn_count": vpn_count,
                "services_count": services_count,
                "active_count": active_count
            }
        )
    finally:
        db.close()


@app.post("/admin/products/add")
async def add_product(
    name: str = Form(...),
    category: str = Form(...),
    price: str = Form("Contact us"),
    description: str = Form(""),
    icon: str = Form("⭐"),
    logo: UploadFile | None = File(None)
):
    db = SessionLocal()

    try:
        logo_path = None

        if logo and logo.filename:
            extension = Path(
                logo.filename
            ).suffix.lower()

            allowed_extensions = {
                ".png",
                ".jpg",
                ".jpeg",
                ".webp"
            }

            if extension in allowed_extensions:
                filename = f"{uuid4().hex}{extension}"
                destination = UPLOAD_DIR / filename

                with destination.open("wb") as buffer:
                    copyfileobj(
                        logo.file,
                        buffer
                    )

                logo_path = (
                    f"/static/uploads/products/{filename}"
                )

        product = Product(
            name=name,
            category=category,
            description=description,
            price=price,
            icon=icon,
            logo=logo_path,
            whatsapp="03343516033",
            active=True
        )

        db.add(product)
        db.commit()

    finally:
        db.close()

    return RedirectResponse(
        url="/admin",
        status_code=303
    )


"""CommerceScene local API: persistent SQLite catalogue and honest mock generation."""
from __future__ import annotations

import csv
import io
import json
import os
import re
import shutil
import sqlite3
import threading
import time
import uuid
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = Path(os.getenv("COMMERCE_DATA_DIR", ROOT / "commerce-data"))
UPLOAD_DIR = DATA_DIR / "uploads"
EXPORT_DIR = DATA_DIR / "exports"
DB_PATH = DATA_DIR / "commercescene.db"
for directory in (DATA_DIR, UPLOAD_DIR, EXPORT_DIR):
    directory.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="CommerceScene API", version="0.1.0", description="Product content studio API (local development mode)")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], allow_methods=["*"], allow_headers=["*"])


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


class ClosingConnection(sqlite3.Connection):
    def __exit__(self, exc_type, exc, tb):
        try:
            return super().__exit__(exc_type, exc, tb)
        finally:
            self.close()


def db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, timeout=20, factory=ClosingConnection)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db() -> None:
    with db() as c:
        c.executescript("""
        CREATE TABLE IF NOT EXISTS products(id TEXT PRIMARY KEY, name TEXT NOT NULL, sku TEXT NOT NULL, category TEXT DEFAULT '', description TEXT DEFAULT '', tags TEXT DEFAULT '[]', archived INTEGER DEFAULT 0, created_at TEXT NOT NULL, updated_at TEXT NOT NULL, UNIQUE(sku));
        CREATE TABLE IF NOT EXISTS images(id TEXT PRIMARY KEY, product_id TEXT NOT NULL REFERENCES products(id), filename TEXT NOT NULL, path TEXT NOT NULL, kind TEXT NOT NULL DEFAULT 'source', status TEXT NOT NULL DEFAULT 'uploaded', approved INTEGER DEFAULT 0, favorite INTEGER DEFAULT 0, width INTEGER, height INTEGER, created_at TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS brands(id TEXT PRIMARY KEY, name TEXT NOT NULL, description TEXT DEFAULT '', colors TEXT DEFAULT '[]', background TEXT DEFAULT 'Clean white', lighting TEXT DEFAULT 'Soft studio', framing TEXT DEFAULT 'Centered', tone TEXT DEFAULT 'Premium and natural', version INTEGER DEFAULT 1, archived INTEGER DEFAULT 0, updated_at TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS batches(id TEXT PRIMARY KEY, status TEXT NOT NULL, total INTEGER NOT NULL, completed INTEGER DEFAULT 0, failed INTEGER DEFAULT 0, settings TEXT NOT NULL, created_at TEXT NOT NULL, updated_at TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS assets(id TEXT PRIMARY KEY, product_id TEXT NOT NULL REFERENCES products(id), batch_id TEXT NOT NULL REFERENCES batches(id), path TEXT NOT NULL, scene TEXT NOT NULL, provider TEXT NOT NULL, approved INTEGER DEFAULT 0, favorite INTEGER DEFAULT 0, created_at TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS exports(id TEXT PRIMARY KEY, status TEXT NOT NULL, path TEXT, item_count INTEGER DEFAULT 0, created_at TEXT NOT NULL);
        """)
        if not c.execute("SELECT 1 FROM brands LIMIT 1").fetchone():
            c.execute("INSERT INTO brands VALUES(?,?,?,?,?,?,?,?,?,?,?)", ("brand-default", "Studio Essentials", "A clean, consistent look for every product.", json.dumps(["#222222", "#f7f6f3", "#c9a876"]), "Clean white", "Soft studio", "Centered", "Premium and natural", 1, 0, now()))
        if not c.execute("SELECT 1 FROM products LIMIT 1").fetchone():
            for n, sku, cat, desc in [("Everyday Ceramic Mug", "MUG-001", "Home & Kitchen", "Matte stoneware mug with a comfortable handle."), ("Canvas Weekender Bag", "BAG-014", "Accessories", "Durable cotton canvas for weekend travel."), ("Amber Glass Bottle", "BOT-026", "Beauty", "Reusable amber glass bottle with a minimal silhouette.")]:
                c.execute("INSERT INTO products VALUES(?,?,?,?,?,?,?,?,?)", (str(uuid.uuid4()), n, sku, cat, desc, "[]", 0, now(), now()))


@app.on_event("startup")
def startup() -> None:
    init_db()


class ProductIn(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    sku: str = Field(min_length=1, max_length=100)
    category: str = ""
    description: str = ""
    tags: list[str] = []


class GenerateIn(BaseModel):
    product_ids: list[str] = Field(min_length=1)
    scene: str = "Clean white studio"
    variations: int = Field(default=2, ge=1, le=4)
    brand_id: str = "brand-default"


class ExportIn(BaseModel):
    asset_ids: list[str] = Field(min_length=1)
    marketplace: str = "Shopify"


@app.get("/health/live")
def live() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/ready")
def ready() -> dict[str, str]:
    with db() as c: c.execute("SELECT 1")
    return {"status": "ready", "mode": "mock"}


@app.get("/api/v1/dashboard")
def dashboard() -> dict[str, Any]:
    with db() as c:
        products = c.execute("SELECT count(*) n FROM products WHERE archived=0").fetchone()["n"]
        sources = c.execute("SELECT count(*) n FROM images WHERE kind='source'").fetchone()["n"]
        assets = c.execute("SELECT count(*) n FROM assets").fetchone()["n"]
        jobs = c.execute("SELECT count(*) n FROM batches WHERE status IN ('queued','processing')").fetchone()["n"]
        approved = c.execute("SELECT count(*) n FROM assets WHERE approved=1").fetchone()["n"]
        recent = [dict(r) for r in c.execute("SELECT p.*, (SELECT count(*) FROM images i WHERE i.product_id=p.id) source_count, (SELECT count(*) FROM assets a WHERE a.product_id=p.id) asset_count FROM products p WHERE archived=0 ORDER BY updated_at DESC LIMIT 5")]
        batch = [dict(r) for r in c.execute("SELECT * FROM batches ORDER BY created_at DESC LIMIT 4")]
    return {"metrics": {"products": products, "sources": sources, "assets": assets, "active_jobs": jobs, "approved": approved}, "recent_products": recent, "recent_batches": batch}


@app.get("/api/v1/products")
def products(q: str = "", category: str = "", sort: str = "updated_at") -> list[dict[str, Any]]:
    sort = sort if sort in {"name", "sku", "updated_at", "created_at"} else "updated_at"
    with db() as c:
        rows = c.execute(f"SELECT p.*, (SELECT count(*) FROM images i WHERE i.product_id=p.id) source_count, (SELECT count(*) FROM assets a WHERE a.product_id=p.id) asset_count FROM products p WHERE archived=0 AND (name LIKE ? OR sku LIKE ? OR category LIKE ?) AND (?='' OR category=?) ORDER BY {sort} DESC", (f"%{q}%", f"%{q}%", f"%{q}%", category, category)).fetchall()
    return [dict(x) for x in rows]


@app.post("/api/v1/products")
def create_product(body: ProductIn) -> dict[str, Any]:
    ident, stamp = str(uuid.uuid4()), now()
    try:
        with db() as c:
            c.execute("INSERT INTO products VALUES(?,?,?,?,?,?,?,?,?)", (ident, body.name, body.sku, body.category, body.description, json.dumps(body.tags), 0, stamp, stamp))
            row = c.execute("SELECT * FROM products WHERE id=?", (ident,)).fetchone()
        return dict(row)
    except sqlite3.IntegrityError:
        raise HTTPException(409, "That SKU is already in use.")


@app.get("/api/v1/products/{product_id}")
def get_product(product_id: str) -> dict[str, Any]:
    with db() as c:
        p = c.execute("SELECT * FROM products WHERE id=? AND archived=0", (product_id,)).fetchone()
        if not p: raise HTTPException(404, "Product not found")
        images = [dict(x) for x in c.execute("SELECT * FROM images WHERE product_id=? ORDER BY created_at DESC", (product_id,))]
        assets = [dict(x) for x in c.execute("SELECT * FROM assets WHERE product_id=? ORDER BY created_at DESC", (product_id,))]
    return {**dict(p), "images": images, "assets": assets}


@app.patch("/api/v1/products/{product_id}")
def update_product(product_id: str, body: ProductIn) -> dict[str, Any]:
    try:
        with db() as c:
            cur = c.execute("UPDATE products SET name=?,sku=?,category=?,description=?,tags=?,updated_at=? WHERE id=? AND archived=0", (body.name, body.sku, body.category, body.description, json.dumps(body.tags), now(), product_id))
            if not cur.rowcount: raise HTTPException(404, "Product not found")
            return dict(c.execute("SELECT * FROM products WHERE id=?", (product_id,)).fetchone())
    except sqlite3.IntegrityError: raise HTTPException(409, "That SKU is already in use.")


@app.post("/api/v1/products/{product_id}/archive")
def archive_product(product_id: str) -> dict[str, str]:
    with db() as c:
        cur = c.execute("UPDATE products SET archived=1, updated_at=? WHERE id=?", (now(), product_id))
        if not cur.rowcount: raise HTTPException(404, "Product not found")
    return {"status": "archived"}


@app.post("/api/v1/products/{product_id}/duplicate")
def duplicate_product(product_id: str) -> dict[str, Any]:
    p = get_product(product_id)
    p["name"] += " copy"; p["sku"] += "-COPY-" + uuid.uuid4().hex[:4].upper()
    return create_product(ProductIn(**{k: p[k] for k in ("name", "sku", "category", "description")}))


@app.post("/api/v1/products/import-csv")
async def import_products_csv(file: UploadFile = File(...)) -> dict[str, Any]:
    if not (file.filename or "").lower().endswith(".csv"):
        raise HTTPException(415, "Choose a .csv file.")
    raw = await file.read(5 * 1024 * 1024 + 1)
    if len(raw) > 5 * 1024 * 1024:
        raise HTTPException(413, "CSV files must be smaller than 5 MB.")
    try:
        text = raw.decode("utf-8-sig")
        reader = csv.DictReader(io.StringIO(text))
    except (UnicodeDecodeError, csv.Error) as exc:
        raise HTTPException(422, "The CSV must be valid UTF-8.") from exc
    if not reader.fieldnames or not {"name", "sku"}.issubset({x.strip().lower() for x in reader.fieldnames}):
        raise HTTPException(422, "CSV headers must include name and sku. Optional headers: category, description, tags.")
    header_map = {x.strip().lower(): x for x in reader.fieldnames}
    created, errors = [], []
    for row_number, row in enumerate(reader, start=2):
        name = (row.get(header_map["name"]) or "").strip()
        sku = (row.get(header_map["sku"]) or "").strip()
        if not name or not sku:
            errors.append({"row": row_number, "sku": sku, "error": "Name and SKU are required."})
            continue
        try:
            tags_raw = row.get(header_map.get("tags", ""), "") or ""
            result = create_product(ProductIn(name=name, sku=sku, category=(row.get(header_map.get("category", ""), "") or "").strip(), description=(row.get(header_map.get("description", ""), "") or "").strip(), tags=[x.strip() for x in tags_raw.split(";") if x.strip()]))
            created.append(result)
        except HTTPException as exc:
            errors.append({"row": row_number, "sku": sku, "error": exc.detail})
    return {"created": len(created), "errors": errors, "products": created}


@app.post("/api/v1/uploads/{product_id}")
async def upload_image(product_id: str, file: UploadFile = File(...)) -> dict[str, Any]:
    allowed = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp"}
    if file.content_type not in allowed: raise HTTPException(415, "Use a JPEG, PNG, or WebP image.")
    raw = await file.read(20 * 1024 * 1024 + 1)
    if len(raw) > 20 * 1024 * 1024: raise HTTPException(413, "Images must be smaller than 20 MB.")
    signatures = {"image/jpeg": raw.startswith(b"\xff\xd8\xff"), "image/png": raw.startswith(b"\x89PNG\r\n\x1a\n"), "image/webp": raw.startswith(b"RIFF") and raw[8:12] == b"WEBP"}
    if not signatures[file.content_type]: raise HTTPException(415, "File contents do not match the selected image format.")
    with db() as c:
        if not c.execute("SELECT 1 FROM products WHERE id=? AND archived=0", (product_id,)).fetchone(): raise HTTPException(404, "Product not found")
    image_id = str(uuid.uuid4()); path = UPLOAD_DIR / (image_id + allowed[file.content_type]); path.write_bytes(raw)
    width = height = None
    try:
        from PIL import Image
        with Image.open(io.BytesIO(raw)) as im:
            width, height = im.size
            if width > 12000 or height > 12000: path.unlink(missing_ok=True); raise HTTPException(413, "Image dimensions exceed 12,000 pixels.")
    except HTTPException: raise
    except Exception as exc:
        path.unlink(missing_ok=True)
        raise HTTPException(415, "The uploaded file is not a decodable image.") from exc
    with db() as c:
        c.execute("INSERT INTO images VALUES(?,?,?,?,?,?,?,?,?,?,?)", (image_id, product_id, Path(file.filename or "image").name, str(path), "source", "uploaded", 0, 0, width, height, now()))
    return {"id": image_id, "product_id": product_id, "filename": Path(file.filename or "image").name, "url": f"/api/v1/images/{image_id}/file", "width": width, "height": height, "status": "uploaded"}


@app.get("/api/v1/images/{image_id}/file")
def image_file(image_id: str) -> FileResponse:
    with db() as c: r = c.execute("SELECT path,filename FROM images WHERE id=?", (image_id,)).fetchone()
    if not r or not Path(r["path"]).is_file(): raise HTTPException(404, "Image not found")
    return FileResponse(r["path"], filename=r["filename"])


@app.get("/api/v1/brands")
def brands() -> list[dict[str, Any]]:
    with db() as c: rows = c.execute("SELECT * FROM brands WHERE archived=0 ORDER BY name").fetchall()
    return [{**dict(r), "colors": json.loads(r["colors"])} for r in rows]


class BrandIn(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    description: str = ""
    colors: list[str] = []
    background: str = "Clean white"
    lighting: str = "Soft studio"
    framing: str = "Centered"
    tone: str = "Premium and natural"


@app.post("/api/v1/brands")
def create_brand(body: BrandIn) -> dict[str, Any]:
    ident = str(uuid.uuid4())
    with db() as c:
        c.execute("INSERT INTO brands VALUES(?,?,?,?,?,?,?,?,?,?,?)", (ident, body.name, body.description, json.dumps(body.colors), body.background, body.lighting, body.framing, body.tone, 1, 0, now()))
    return {"id": ident, **body.model_dump(), "version": 1}


@app.put("/api/v1/brands/{brand_id}")
def update_brand(brand_id: str, body: BrandIn) -> dict[str, Any]:
    with db() as c:
        cur = c.execute("UPDATE brands SET name=?,description=?,colors=?,background=?,lighting=?,framing=?,tone=?,version=version+1,updated_at=? WHERE id=? AND archived=0", (body.name, body.description, json.dumps(body.colors), body.background, body.lighting, body.framing, body.tone, now(), brand_id))
        if not cur.rowcount: raise HTTPException(404, "Brand profile not found")
        r = c.execute("SELECT * FROM brands WHERE id=?", (brand_id,)).fetchone()
    return {**dict(r), "colors": json.loads(r["colors"])}


@app.get("/api/v1/assets")
def assets(q: str = "", status: str = "all") -> list[dict[str, Any]]:
    with db() as c:
        rows = c.execute("SELECT a.*,p.name product_name,p.sku FROM assets a JOIN products p ON p.id=a.product_id WHERE (p.name LIKE ? OR p.sku LIKE ?) AND (?='all' OR (?='approved' AND a.approved=1) OR (?='review' AND a.approved=0)) ORDER BY a.created_at DESC", (f"%{q}%",f"%{q}%",status,status,status)).fetchall()
    return [dict(r) for r in rows]


@app.post("/api/v1/assets/{asset_id}/approve")
def approve_asset(asset_id: str) -> dict[str, Any]:
    with db() as c:
        cur = c.execute("UPDATE assets SET approved=1 WHERE id=?", (asset_id,))
        if not cur.rowcount: raise HTTPException(404, "Asset not found")
        r = c.execute("SELECT * FROM assets WHERE id=?", (asset_id,)).fetchone()
    return dict(r)


@app.post("/api/v1/generation/batches")
def create_batch(body: GenerateIn) -> dict[str, Any]:
    with db() as c:
        for pid in body.product_ids:
            if not c.execute("SELECT 1 FROM products WHERE id=? AND archived=0", (pid,)).fetchone(): raise HTTPException(404, f"Product not found: {pid}")
        if not c.execute("SELECT 1 FROM brands WHERE id=?", (body.brand_id,)).fetchone(): raise HTTPException(404, "Brand profile not found")
        total = len(body.product_ids) * body.variations
        bid = str(uuid.uuid4()); settings = json.dumps({**body.model_dump(), "brand_snapshot": dict(c.execute("SELECT * FROM brands WHERE id=?", (body.brand_id,)).fetchone())})
        c.execute("INSERT INTO batches VALUES(?,?,?,?,?,?,?,?)", (bid, "queued", total, 0, 0, settings, now(), now()))
    thread = threading.Thread(target=process_batch, args=(bid, body.product_ids, body.scene, body.variations), daemon=True); thread.start()
    return {"id": bid, "status": "queued", "total": total, "completed": 0, "failed": 0, "provider": "mock"}


def process_batch(batch_id: str, product_ids: list[str], scene: str, variations: int) -> None:
    from PIL import Image, ImageDraw
    with db() as c: c.execute("UPDATE batches SET status='processing',updated_at=? WHERE id=?", (now(), batch_id))
    for pid in product_ids:
        with db() as c: p = c.execute("SELECT * FROM products WHERE id=?", (pid,)).fetchone()
        for index in range(variations):
            time.sleep(0.45)
            image_id = str(uuid.uuid4()); path = UPLOAD_DIR / (image_id + ".png")
            image = Image.new("RGB", (1024, 1024), "#f1efeb"); draw = ImageDraw.Draw(image)
            draw.rounded_rectangle((178, 142, 846, 880), radius=34, fill="#ffffff", outline="#dedbd6", width=3)
            draw.text((230, 345), p["name"][:26], fill="#25231f"); draw.text((230, 401), f"{scene} · Variation {index+1}", fill="#756f66")
            draw.text((230, 813), "DEVELOPMENT MOCK · NOT AI GENERATED", fill="#ab5d45")
            image.save(path)
            with db() as c:
                c.execute("INSERT INTO assets VALUES(?,?,?,?,?,?,?,?,?)", (image_id, pid, batch_id, str(path), scene, "mock", 0, 0, now()))
                c.execute("UPDATE batches SET completed=completed+1,updated_at=? WHERE id=?", (now(), batch_id))
    with db() as c: c.execute("UPDATE batches SET status='succeeded',updated_at=? WHERE id=?", (now(), batch_id))


@app.get("/api/v1/generation/batches")
def batches() -> list[dict[str, Any]]:
    with db() as c: rows = c.execute("SELECT * FROM batches ORDER BY created_at DESC LIMIT 100").fetchall()
    return [{**dict(r), "settings": json.loads(r["settings"])} for r in rows]


@app.get("/api/v1/generation/batches/{batch_id}")
def batch_detail(batch_id: str) -> dict[str, Any]:
    with db() as c:
        r = c.execute("SELECT * FROM batches WHERE id=?", (batch_id,)).fetchone()
        if not r: raise HTTPException(404, "Batch not found")
        outputs = [dict(a) for a in c.execute("SELECT a.*,p.name product_name,p.sku FROM assets a JOIN products p ON p.id=a.product_id WHERE batch_id=? ORDER BY created_at", (batch_id,))]
    return {**dict(r), "settings": json.loads(r["settings"]), "outputs": outputs}


@app.get("/api/v1/assets/{asset_id}/file")
def asset_file(asset_id: str) -> FileResponse:
    with db() as c: r = c.execute("SELECT path FROM assets WHERE id=?", (asset_id,)).fetchone()
    if not r or not Path(r["path"]).is_file(): raise HTTPException(404, "Asset not found")
    return FileResponse(r["path"], filename=f"{asset_id}.png")


@app.post("/api/v1/exports")
def create_export(body: ExportIn) -> dict[str, Any]:
    with db() as c:
        marks = ",".join("?" for _ in body.asset_ids)
        rows = c.execute(f"SELECT a.*,p.name product_name,p.sku FROM assets a JOIN products p ON p.id=a.product_id WHERE a.id IN ({marks})", body.asset_ids).fetchall()
        if len(rows) != len(set(body.asset_ids)): raise HTTPException(404, "One or more assets were not found")
        rejected = [r["id"] for r in rows if not r["approved"]]
        if rejected: raise HTTPException(422, {"message": "Approve all selected assets before export.", "asset_ids": rejected})
    export_id = str(uuid.uuid4()); path = EXPORT_DIR / (export_id + ".zip"); manifest = []
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
        for row in rows:
            ext = Path(row["path"]).suffix or ".png"
            safe_sku = re.sub(r"[^A-Za-z0-9_-]+", "-", row["sku"]).strip("-_")[:80] or "product"
            safe_market = re.sub(r"[^A-Za-z0-9_-]+", "-", body.marketplace).strip("-_").lower()[:40] or "custom"
            safe_scene = re.sub(r"[^A-Za-z0-9_-]+", "-", row["scene"]).strip("-_").lower()[:60] or "scene"
            name = f"{safe_sku}/{safe_market}/{safe_scene}-{row['id'][:8]}{ext}"
            archive.write(row["path"], name)
            manifest.append({"product_id": row["product_id"], "product_name": row["product_name"], "sku": row["sku"], "marketplace": body.marketplace, "scene": row["scene"], "asset_id": row["id"], "file_path": name, "format": ext[1:].upper(), "validation": "passed · approved"})
    with zipfile.ZipFile(path, "a", zipfile.ZIP_DEFLATED) as archive:
        buffer = io.StringIO(); writer = csv.DictWriter(buffer, fieldnames=list(manifest[0])); writer.writeheader(); writer.writerows(manifest); archive.writestr("manifest.csv", buffer.getvalue())
    with db() as c: c.execute("INSERT INTO exports VALUES(?,?,?,?,?)", (export_id, "succeeded", str(path), len(rows), now()))
    return {"id": export_id, "status": "succeeded", "item_count": len(rows), "download_url": f"/api/v1/exports/{export_id}/download"}


@app.get("/api/v1/exports")
def export_list() -> list[dict[str, Any]]:
    with db() as c: return [dict(x) for x in c.execute("SELECT * FROM exports ORDER BY created_at DESC")]


@app.get("/api/v1/exports/{export_id}/download")
def export_download(export_id: str) -> FileResponse:
    with db() as c: r = c.execute("SELECT path FROM exports WHERE id=? AND status='succeeded'", (export_id,)).fetchone()
    if not r or not Path(r["path"]).is_file(): raise HTTPException(404, "Export not found")
    return FileResponse(r["path"], filename=f"commercescene-{export_id[:8]}.zip", media_type="application/zip")

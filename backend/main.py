"""FastAPI application for CQP Generator."""
from __future__ import annotations
import tempfile
import shutil
from pathlib import Path

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from backend.services.cqp_service import generate_cqp
from backend.config import OUTPUTS_DIR, HOST, PORT

app = FastAPI(title="CQP Generator", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend" / "dist"


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/generate-cqp")
async def generate_cqp_endpoint(
    tmp_file: UploadFile = File(...),
    acl_file: UploadFile = File(...),
    datasheet_file: UploadFile = File(...),
    market: str = Form(default=""),
):
    tmp_path = None
    acl_path = None
    ds_path = None

    try:
        tmp_dir = tempfile.mkdtemp()

        tmp_path = Path(tmp_dir) / f"TMP_{tmp_file.filename}"
        acl_path = Path(tmp_dir) / f"ACL_{acl_file.filename}"
        ds_path = Path(tmp_dir) / f"DS_{datasheet_file.filename}"

        with open(tmp_path, "wb") as f:
            content = await tmp_file.read()
            f.write(content)

        with open(acl_path, "wb") as f:
            content = await acl_file.read()
            f.write(content)

        with open(ds_path, "wb") as f:
            content = await datasheet_file.read()
            f.write(content)

        OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

        result = generate_cqp(
            tmp_path=str(tmp_path),
            acl_path=str(acl_path),
            ds_path=str(ds_path),
            market=market,
            output_dir=str(OUTPUTS_DIR),
        )

        if not result.get("success"):
            raise HTTPException(status_code=422, detail=result)

        output_path = result["output_path"]
        cell_data = result.get("cell_data")

        filename = Path(output_path).name

        return FileResponse(
            path=output_path,
            filename=filename,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "success": False,
            "error": str(type(e).__name__),
            "details": str(e),
        })
    finally:
        if tmp_path and tmp_path.exists():
            tmp_path.parent.rmdir() if not any(tmp_path.parent.iterdir()) else None
        if acl_path and acl_path.exists():
            pass
        if ds_path and ds_path.exists():
            pass
        if tmp_path:
            shutil.rmtree(tmp_path.parent, ignore_errors=True)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)


if FRONTEND_DIR.exists():
    app.mount("/assets", StaticFiles(directory=str(FRONTEND_DIR / "assets")), name="assets")

    @app.get("/{full_path:path}", include_in_schema=False)
    async def serve_spa(full_path: str):
        file_path = FRONTEND_DIR / full_path
        if file_path.exists() and file_path.is_file():
            return FileResponse(str(file_path))
        return FileResponse(str(FRONTEND_DIR / "index.html"))

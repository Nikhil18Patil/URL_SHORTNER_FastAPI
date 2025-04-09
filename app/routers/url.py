from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app import schemas, models, utils
from app.database import SessionLocal

router = APIRouter()


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/shorten", response_model=schemas.URLResponse, status_code=status.HTTP_201_CREATED)
def create_short_url(
    request: schemas.URLRequest,
    db: Session = Depends(get_db)
):
    """
    Create a new short URL. If the original URL already exists,
    return the existing shortened URL.
    """
    try:
        original_url = str(request.original_url)

        # Check if the URL is already in the DB
        existing = db.query(models.URL).filter_by(original_url=original_url).first()
        if existing:
            return {"short_url": f"http://localhost:8000/{existing.short_code}"}

        # Create a new URL entry without a short_code initially
        new_url = models.URL(original_url=original_url, short_code="")
        db.add(new_url)
        db.commit()
        db.refresh(new_url)

        # Generate and update the short code
        short_code = utils.encode_base62(new_url.id)
        new_url.short_code = short_code
        db.commit()

        return {"short_url": f"http://localhost:8000/{short_code}"}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the short URL: {str(e)}"
        )


@router.get("/{short_code}", status_code=status.HTTP_302_FOUND)
def redirect_to_original(
    short_code: str,
    db: Session = Depends(get_db)
):
    """
    Redirect to the original URL using the short code.
    """
    try:
        url = db.query(models.URL).filter_by(short_code=short_code).first()
        if not url:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Short URL not found"
            )
        return RedirectResponse(url.original_url)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during redirection: {str(e)}"
        )

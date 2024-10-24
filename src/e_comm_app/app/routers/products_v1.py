import uuid

from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from e_comm_app.app.auth import get_current_user
from e_comm_app.app.config import get_db
from e_comm_app.app.models.product_models import ProductCreate, ProductResponse
from e_comm_app.app.orm.e_comm_orm import Product, User

router = APIRouter(
    prefix="/products", tags=["products"], responses={404: {"description": "Not found"}}
)


@router.get("", response_model=list[ProductResponse], summary="Retrieve all products")
def get_products(db: Session = Depends(get_db)):
    """
    Retrieves a list of all products from the database.
    """
    try:
        logger.info("Fetching product details.")
        products = db.query(Product).all()
        return products
    except SQLAlchemyError as exc:
        logger.opt(exception=exc).exception("Database error occurred.")
        raise HTTPException(
            status_code=500, detail=f"Database error occurred: {exc}"
        ) from exc


@router.get("/{id}", response_model=ProductResponse, summary="Retrieve product by ID")
def get_product(id: uuid.UUID, db: Session = Depends(get_db)):
    """
    Retrieves the details of a specific product by its ID.

    - **id**: The unique ID of the product
    """
    try:
        logger.info(f"Fetching product details for id: {id}.")
        product = db.query(Product).filter(Product.id == id).first()
        if not product:
            logger.info(f"No such product found for the id: {id}.")
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except SQLAlchemyError as exc:
        logger.opt(exception=exc).exception("Database error occurred.")
        raise HTTPException(
            status_code=500, detail=f"Database error occurred: {exc}"
        ) from exc


@router.post(
    "", response_model=ProductResponse, status_code=201, summary="Create a new product"
)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    """
    Creates a new product with the given details.

    - **title**: The title of the product
    - **description**: A brief description of the product
    - **price**: The price of the product
    """
    try:
        logger.info("New product entry.")
        new_product = Product(**product.dict())
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product
    except SQLAlchemyError as exc:
        logger.opt(exception=exc).exception(
            "Database error occurred. Cancelling transaction."
        )
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Database error occurred: {exc}"
        ) from exc


@router.put(
    "/{id}", response_model=ProductResponse, summary="Update an existing product"
)
def update_product(
    id: uuid.UUID,
    updated_product: ProductCreate,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    """
    Updates an existing product by its ID with the new details.

    - **id**: The unique ID of the product to update
    """
    try:
        logger.info(f"Trying to update product details for id: {id}.")
        product = db.query(Product).filter(Product.id == id).first()
        if not product:
            logger.info(f"No such product found for the id: {id}.")
            raise HTTPException(status_code=404, detail="Product not found")

        product.title = updated_product.title
        product.description = updated_product.description
        product.price = updated_product.price

        db.commit()
        db.refresh(product)
        return product
    except IntegrityError as exc:
        logger.opt(exception=exc).exception(
            "Failed to update the product due to a database integrity error. Cancelling transaction"
        )
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Failed to update the product due to a database integrity error.",
        ) from exc
    except SQLAlchemyError as exc:
        logger.opt(exception=exc).exception(
            "Database error occurred. Cancelling transaction"
        )
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Database error occurred: {exc}"
        ) from exc


@router.delete("/{id}", summary="Delete a product")
def delete_product(
    id: uuid.UUID,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    """
    Deletes a product from the database by its ID.

    - **id**: The unique ID of the product to delete
    """
    try:
        logger.info(f"Trying to delete product details for the id: {id}.")
        product = db.query(Product).filter(Product.id == id).first()
        if not product:
            logger.info(f"No such product found for the id: {id}.")
            raise HTTPException(status_code=404, detail="Product not found")

        db.delete(product)
        db.commit()
        return {"message": "Product deleted successfully"}
    except SQLAlchemyError as exc:
        logger.opt(exception=exc).exception(
            "Database error occurred. Cancelling transaction."
        )
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Database error occurred: {exc}"
        ) from exc

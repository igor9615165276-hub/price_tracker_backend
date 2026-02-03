router = APIRouter(prefix="/products", tags=["products"])

@router.post("/", response_model=ProductOut)
async def add_product(
    data: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # если делаешь auth
):
    # 1) определить платформу по URL (wb / ozon)
    # 2) дернуть парсер (wb или ozon) -> title, price, image
    # 3) создать Product + первый PriceSnapshot
    ...

@router.get("/", response_model=list[ProductOut])
async def list_products(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # вернуть все товары юзера + last price
    ...

@router.get("/{product_id}", response_model=ProductOut)
async def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ...

@router.get("/{product_id}/history", response_model=list[PriceSnapshotOut])
async def get_price_history(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # вернуть историю цен по товару
    ...

@router.get("/{product_id}/compare")
async def compare_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # найти аналог на другой платформе и отдать {wb_price, ozon_price, diff}
    ...

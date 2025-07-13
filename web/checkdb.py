from models import Session, SaleItem
session = Session()
for item in session.query(SaleItem).all():
    print(item.name, item.quantity, item.total_sales)

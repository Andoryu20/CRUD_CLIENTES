import csv
import io
import openpyxl
import xlrd
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from app.config import get_db
from app.clients.models import Client
from app.countries.models import Country
from app.categories.models import Category
from app.clients.schemas import ClientCreate, ClientResponse
from typing import List, Optional
from datetime import date, datetime
from fastapi.responses import StreamingResponse

router = APIRouter(
    prefix="/clients",
    tags=["Clients"]
)

@router.post('/', response_model=ClientResponse)
def create_client(client_in: ClientCreate, db: Session = Depends(get_db)):

    exist_country = db.query(Country).filter(Country.id == client_in.country_id).first()
    if not exist_country:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The ID country {client_in.country_id} doesn't exists."
        )
    
    exist_category = db.query(Category).filter(Category.id == client_in.category_id).first()
    if not exist_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The ID category {client_in.category_id} doesn't exists."
        )
    
    data_clients = client_in.model_dump()
    new_client = Client(**data_clients)

    db.add(new_client)
    db.commit()
    db.refresh(new_client)

    return new_client
    
@router.get("/", response_model=List[ClientResponse])
def get_clients(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    query = db.query(Client)
    paginated_query = query.offset(skip).limit(limit)
    clients = paginated_query.all()

    return clients

@router.get("/report")
def generate_clients_report(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    category_id: Optional[int] = None,
    city: Optional[str] = None,
    country_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
   
    query = db.query(Client)

    if start_date:
        query = query.filter(Client.created_at >= datetime.combine(start_date, datetime.min.time()))
    if end_date:
        query = query.filter(Client.created_at <= datetime.combine(end_date, datetime.max.time()))
    if category_id:
        query = query.filter(Client.category_id == category_id)
    if city:
        query = query.filter(Client.city == city)
    if country_id:
        query = query.filter(Client.country_id == country_id)
    clients = query.all()

    def csv_generator():
        output = io.StringIO()
        writer = csv.writer(output)
        
        writer.writerow(["ID", "Name", "City", "Country", "Category", "Status", "Created At"])
        yield output.getvalue()
        output.seek(0)
        output.truncate(0)

        for client in clients:
            writer.writerow([
                client.id,
                client.name_client,
                client.city,
                client.country.name if client.country else "N/A",
                client.category.name if client.category else "N/A",
                "Active" if client.is_active else "Inactive",
                client.created_at.strftime("%Y-%m-%d %H:%M:%S") if client.created_at else ""
            ])
            yield output.getvalue()
            output.seek(0)
            output.truncate(0)

    headers = {
        'Content-Disposition': 'attachment; filename="clients_report.csv"'
    }
    return StreamingResponse(csv_generator(), media_type="text/csv", headers=headers)

@router.get("/{client_id}", response_model=ClientResponse)
def get_client_by_id(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.put("/{client_id}", response_model=ClientResponse)
def update_client(client_id: int, client_in: ClientCreate, db: Session = Depends(get_db)):

    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    client.name_client = client_in.name_client
    client.city = client_in.city
    client.country_id = client_in.country_id
    client.category_id = client_in.category_id
    client.is_active = client_in.is_active
    
    db.commit()
    db.refresh(client)
    return client

@router.delete("/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    db.delete(client)
    db.commit()
    return {"message": f"Client with ID {client_id} successfully deleted"}

@router.post("/upload", status_code=status.HTTP_201_CREATED)
def upload_clients_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    filename = file.filename
    if not (filename.endswith('.csv') or filename.endswith('.xlsx') or filename.endswith('.xls')):
        raise HTTPException(
            status_code=400, 
            detail="Invalid file format. Only .csv, .xlsx, and .xls are allowed."
        )

    raw_rows = []

    try:
        contents = file.file.read()
        
        if filename.endswith('.csv'):
            csv_data = contents.decode('utf-8')
            csv_reader = csv.reader(io.StringIO(csv_data))
            header = next(csv_reader)
            
            for row in csv_reader:
                if row:
                    raw_rows.append(row)
                    
        elif filename.endswith('.xlsx'):
            wb = openpyxl.load_workbook(io.BytesIO(contents), data_only=True)
            sheet = wb.active
            for row in sheet.iter_rows(min_row=2, values_only=True):
                if any(row):
                    raw_rows.append(list(row))
                    
        elif filename.endswith('.xls'):
            wb = xlrd.open_workbook(file_contents=contents)
            sheet = wb.sheet_by_index(0)
            for row_idx in range(1, sheet.nrows):
                row = sheet.row_values(row_idx)
                if any(row):
                    raw_rows.append(row)

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading file: {str(e)}")

    inserted_count = 0
    errors = []

    for idx, row in enumerate(raw_rows, start=2):
        try:
            if len(row) < 4:
                raise ValueError("Incomplete row fields.")

            name_client = str(row[0]).strip()
            city = str(row[1]).strip()
            country_id = int(float(row[2])) 
            category_id = int(float(row[3]))
            is_active = bool(int(float(row[4]))) if len(row) > 4 and row[4] is not None else True

            if not db.query(Country).filter(Country.id == country_id).first():
                raise ValueError(f"Country ID {country_id} doesn't exist.")
            if not db.query(Category).filter(Category.id == category_id).first():
                raise ValueError(f"Category ID {category_id} doesn't exist.")

            client_data = ClientCreate(
                name_client=name_client,
                city=city,
                country_id=country_id,
                category_id=category_id,
                is_active=is_active,
                user_created="bulk_upload"
            )

            new_client = Client(**client_data.model_dump())
            db.add(new_client)
            inserted_count += 1

        except Exception as err:
            errors.append({"row": idx, "error": str(err)})

    if inserted_count > 0:
        db.commit()

    return {
        "message": f"Bulk upload process completed.",
        "successfully_inserted": inserted_count,
        "failed_rows_count": len(errors),
        "errors": errors
    }


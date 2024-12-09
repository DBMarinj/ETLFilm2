import polars as pl
import logging
from django.utils.dateparse import parse_datetime
from AppETL.models import Customer, Rental, Store, Inventory, Film

# Configuración del logging para la observabilidad
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ruta del archivo Excel(.xlsx)
file_path = r'D:\Desktop\ETL\backend\AppETL\Films_2.xlsx'

def load_data_from_excel(file_path):
    """
    Carga los datos desde el archivo Excel especificado utilizando Polars.
    """
    try:
        # Carga del archivo Excel con todas las hojas
        df_customer = pl.read_excel(file_path, sheet_name='customer')
        df_rental = pl.read_excel(file_path, sheet_name='rental')
        df_store = pl.read_excel(file_path, sheet_name='store')
        df_inventory = pl.read_excel(file_path, sheet_name='inventory')
        df_film = pl.read_excel(file_path, sheet_name='film')
        
        logger.info(f'Archivo Excel cargado correctamente desde {file_path}')
        return df_customer, df_rental, df_store, df_inventory, df_film
    except Exception as e:
        logger.error(f'Error al cargar el archivo Excel: {e}')
        return None, None, None, None, None

def clean_and_validate_data(df, required_columns):
    """
    Realiza limpieza y validación de los datos, asegurando que las columnas necesarias estén presentes
    y que los datos sean consistentes.
    """
    logger.info('Iniciando proceso de validación y limpieza de datos...')
    
    # Verificar columnas esperadas en el archivo
    for column in required_columns:
        if column not in df.columns:
            logger.warning(f'Columna {column} no encontrada en los datos de entrada')

    # Realizar limpieza de datos: por ejemplo, eliminar filas con valores nulos en las columnas requeridas
    df = df.drop_nulls(required_columns)  # Eliminar filas con valores nulos en las columnas requeridas
    
    # Verificar que las fechas sean válidas
    if 'create_date' in df.columns:
        df = df.with_column(df['create_date'].str.strptime(pl.Datetime))
    if 'last_update' in df.columns:
        df = df.with_column(df['last_update'].str.strptime(pl.Datetime))

    # Validar que los tipos de datos sean correctos
    if 'customer_id' in df.columns:
        df = df.with_column(df['customer_id'].cast(pl.Int64))

    logger.info(f'Proceso de limpieza y validación completado. Se procesaron {len(df)} filas.')
    return df

def insert_data_to_db(df_customer, df_rental, df_store, df_inventory, df_film):
    """
    Inserta los datos validados y limpiados en la base de datos.
    """
    try:
        # Insertar datos en la tabla Customer
        for row in df_customer.iter_rows(named=True):
            Customer.objects.create(
                customer_id=row['customer_id'],
                store_id=row['store_id'],
                first_name=row['first_name'],
                last_name=row['last_name'],
                email=row['email'],
                address_id=row['address_id'],
                active=row['active'],
                create_date=row['create_date'],
                last_update=row['last_update'],
            )

        # Insertar datos en la tabla Rental
        for row in df_rental.iter_rows(named=True):
            Rental.objects.create(
                rental_id=row['rental_id'],
                rental_date=row['rental_date'],
                inventory_id=row['inventory_id'],
                customer_id=row['customer_id'],
                return_date=row['return_date'],
                staff_id=row['staff_id'],
                last_update=row['last_update'],
            )

        # Insertar datos en la tabla Store
        for row in df_store.iter_rows(named=True):
            Store.objects.create(
                store_id=row['store_id'],
                manager_staff_id=row['manager_staff_id'],
                address_id=row['address_id'],
                last_update=row['last_update'],
            )

        # Insertar datos en la tabla Inventory
        for row in df_inventory.iter_rows(named=True):
            Inventory.objects.create(
                inventory_id=row['inventory_id'],
                film_id=row['film_id'],
                store_id=row['store_id'],
                last_update=row['last_update'],
            )

        # Insertar datos en la tabla Film
        for row in df_film.iter_rows(named=True):
            Film.objects.create(
                film_id=row['film_id'],
                title=row['title'],
                description=row['description'],
                release_year=row['release_year'],
                language_id=row['language_id'],
                original_language_id=row['original_language_id'],
                rental_rate=row['rental_rate'],
                length_rate=row['length_rate'],
                length=row['length'],
                replacement_cost=row['replacement_cost'],
                rating=row['rating'],
                special_features=row['special_features'],
                last_update=row['last_update'],
            )
        
        logger.info('Datos insertados en todas las tablas de la base de datos.')
    except Exception as e:
        logger.error(f'Error al insertar datos en la base de datos: {e}')

def process_etl(file_path):
    """
    Función principal que realiza el proceso ETL: carga, limpieza y carga en la base de datos.
    """
    # Cargar los datos desde el archivo Excel
    df_customer, df_rental, df_store, df_inventory, df_film = load_data_from_excel(file_path)
    
    if df_customer is not None:
        # Limpiar y validar los datos para cada DataFrame
        df_customer_cleaned = clean_and_validate_data(df_customer, ['customer_id', 'store_id', 'first_name', 'last_name', 'email', 'address_id', 'active', 'create_date', 'last_update'])
        df_rental_cleaned = clean_and_validate_data(df_rental, ['rental_id', 'rental_date', 'inventory_id', 'customer_id', 'return_date', 'staff_id', 'last_update'])
        df_store_cleaned = clean_and_validate_data(df_store, ['store_id', 'manager_staff_id', 'address_id', 'last_update'])
        df_inventory_cleaned = clean_and_validate_data(df_inventory, ['inventory_id', 'film_id', 'store_id', 'last_update'])
        df_film_cleaned = clean_and_validate_data(df_film, ['film_id', 'title', 'description', 'release_year', 'language_id', 'rental_rate', 'length_rate', 'length', 'replacement_cost', 'rating', 'special_features', 'last_update'])
        
        # Insertar los datos limpios en la base de datos
        insert_data_to_db(df_customer_cleaned, df_rental_cleaned, df_store_cleaned, df_inventory_cleaned, df_film_cleaned)

if __name__ == '__main__':
    process_etl(file_path)

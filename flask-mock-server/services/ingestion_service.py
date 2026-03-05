import dlt
from repositories.json_customer_repository import JsonCustomerRepository
from flask import current_app

class IngestionService:
    def __init__(self, json_repository: JsonCustomerRepository):
        self.json_repository = json_repository

    def ingest_data(self):
        import copy
        from datetime import datetime, date
        # Fetch data and make a deep copy to avoid modifying the original JSON repo objects
        all_customers = copy.deepcopy(self.json_repository.get_all())
        
        db_uri = current_app.config['SQLALCHEMY_DATABASE_URI']
        
        # Decide destination based on the DB URI
        if db_uri.startswith('postgresql'):
            dest = dlt.destinations.postgres(db_uri)
        else:
            db_path = db_uri.replace('sqlite:///', '')
            dest = dlt.destinations.sqlite(db_path)

        pipeline = dlt.pipeline(
            pipeline_name="customer_ingestion_v5",
            destination=dest,
            dataset_name="public"
        )
        
        @dlt.resource(
            name="customers", 
            write_disposition="merge", 
            primary_key="customer_id"
        )
        def customer_resource():
            for cust in all_customers:
                # Ensure id is string
                cust['customer_id'] = str(cust['customer_id'])
                
                # Ensure date_of_birth is a python date object or None
                dob = cust.get('date_of_birth')
                if isinstance(dob, str) and dob:
                    try:
                        cust['date_of_birth'] = datetime.strptime(dob, '%Y-%m-%d').date()
                    except ValueError:
                        cust['date_of_birth'] = None
                elif not isinstance(dob, (date, datetime)):
                    cust['date_of_birth'] = None
                        
                yield cust
        
        # Run the pipeline
        load_info = pipeline.run(customer_resource())
        
        return {
            "status": "success",
            "records_processed": len(all_customers),
            "load_info": str(load_info)
        }

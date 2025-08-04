import sqlite3
from redis_om import Field, JsonModel, Migrator
from pydantic import BaseModel, Field
from typing import Any, Annotated

class PrimaryKey:
    def __init__(self):
        self.is_primary_key = True

def pk() -> Any:
    """Marks a field as a primary key"""
    return PrimaryKey()

class UniversalModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True
        extra = "allow"  # This allows extra attributes to be set

class UniversalDatabase:

    def __init__(self, type_db, connection=None) -> None:
        if connection is None:
            connection = "universal.db" if type_db == "sqlite" else None
        self.type_db = type_db
        if type_db == "sqlite":
            self.connection = sqlite3.connect(connection)
        elif type_db == "redis":
            self.connection = JsonModel
        else:
            raise ValueError("Unsupported database type")

    def save(self, model: UniversalModel) -> None:
        if self.type_db == "redis":
            model.save()
        elif self.type_db == "sqlite":
            cursor = self.connection.cursor()
            # Check if record exists
            cursor.execute(f"SELECT COUNT(*) FROM {model.__class__.__name__} WHERE id = ?", (model.id,))
            exists = cursor.fetchone()[0] > 0

            if exists:
                # Update existing record
                set_clause = ", ".join([f"{key} = ?" for key in model.__dict__.keys() if key != 'id'])
                values = [v for k, v in model.__dict__.items() if k != 'id']
                values.append(model.id)  # Add id for WHERE clause
                cursor.execute(f"UPDATE {model.__class__.__name__} SET {set_clause} WHERE id = ?", tuple(values))
            else:
                # Insert new record
                columns = ", ".join(model.__dict__.keys())
                placeholders = ", ".join(['?' for _ in model.__dict__.values()])
                cursor.execute(f"INSERT INTO {model.__class__.__name__} ({columns}) VALUES ({placeholders})", 
                             tuple(model.__dict__.values()))
            
            self.connection.commit()
        else:
            raise ValueError("Unsupported database type")

    def load(self, model_class: type) -> list[UniversalModel]:
        if self.type_db == "redis":
            return model_class.all()
        elif self.type_db == "sqlite":
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT * FROM {model_class.__name__}")
            rows = cursor.fetchall()
            return [model_class(**dict(zip([column[0] for column in cursor.description], row))) for row in rows]
        else:
            raise ValueError("Unsupported database type")
        
    def delete(self, model: UniversalModel):
        if self.type_db == "redis":
            model.delete()
        elif self.type_db == "sqlite":
            cursor = self.connection.cursor()
            cursor.execute(f"DELETE FROM {model.__class__.__name__} WHERE id = ?", (model.id,))
            self.connection.commit()
        else:
            raise ValueError("Unsupported database type")
    
    def update(self, model: UniversalModel):
        if self.type_db == "redis":
            model.save()
        elif self.type_db == "sqlite":
            cursor = self.connection.cursor()
            set_clause = ", ".join([f"{key} = ?" for key in model.__dict__.keys()])
            cursor.execute(f"UPDATE {model.__class__.__name__} SET {set_clause} WHERE id = ?", (*model.__dict__.values(), model.id))
            self.connection.commit()
        else:
            raise ValueError("Unsupported database type")
    
    def find(self, model_class: type, **kwargs):
        if self.type_db == "redis":
            return model_class.find(**kwargs)
        elif self.type_db == "sqlite":
            cursor = self.connection.cursor()
            where_clause = " AND ".join([f"{key} = ?" for key in kwargs.keys()])
            cursor.execute(f"SELECT * FROM {model_class.__name__} WHERE {where_clause}", tuple(kwargs.values()))
            rows = cursor.fetchall()
            return [model_class(**dict(zip([column[0] for column in cursor.description], row))) for row in rows]
        else:
            raise ValueError("Unsupported database type")

    def load_UniversalModel(self, model: UniversalModel):
        if self.type_db == "redis":
            # Create a new JsonModel class dynamically with the correct fields
            annotations = {}
            attrs = {}
            primary_key_field = None
            
            for name, field in model.__class__.__annotations__.items():
                # Get the base type
                field_type = field.__origin__ if hasattr(field, '__origin__') else field
                
                # Check if field is annotated with PrimaryKey
                if hasattr(field, "__metadata__"):
                    for meta in field.__metadata__:
                        if isinstance(meta, PrimaryKey):
                            primary_key_field = name
                            break
                
                # Add field to attrs
                attrs[name] = Field(index=True)
                annotations[name] = field_type
            
            # Add annotations to attrs
            attrs['__annotations__'] = annotations
            
            # Create a new model class that inherits from JsonModel
            ModelClass = type(model.__class__.__name__, (JsonModel,), attrs)
            
            # Copy all data, including the id
            instance_data = model.__dict__.copy()
            
            # If we have a primary key field, use its value as pk
            if primary_key_field and primary_key_field in instance_data:
                instance_data['pk'] = str(instance_data[primary_key_field])
            
            return ModelClass(**instance_data)
        elif self.type_db == "sqlite":
            fields = []
            for name, field in model.__class__.__annotations__.items():
                # Check if field is annotated with PrimaryKey
                is_primary = False
                if hasattr(field, "__metadata__"):
                    for meta in field.__metadata__:
                        if isinstance(meta, PrimaryKey):
                            is_primary = True
                            break
                
                # Get the base type for the field
                field_type = field.__name__ if hasattr(field, '__name__') else field._name
                if field_type == "int":
                    sql_type = "INTEGER"
                elif field_type == "float":
                    sql_type = "REAL"
                elif field_type == "bool":
                    sql_type = "BOOLEAN"
                else:
                    sql_type = "TEXT"
                
                # Add PRIMARY KEY if marked
                if is_primary:
                    sql_type += " PRIMARY KEY"
                fields.append(f"{name} {sql_type}")
            # Bind methods to the instance
            model.update = lambda *args, **kwargs: self.update(model, *args, **kwargs)
            model.save = lambda *args, **kwargs: self.save(model, *args, **kwargs)
            model.delete = lambda *args, **kwargs: self.delete(model, *args, **kwargs)
            model.find = lambda *args, **kwargs: self.find(model.__class__, *args, **kwargs)
            model.load = lambda *args, **kwargs: self.load(model.__class__, *args, **kwargs)
            table_name = model.__class__.__name__
            fields_sql = ", ".join(fields)
            create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({fields_sql})"
            cursor = self.connection.cursor()
            cursor.execute(create_table_sql)
            self.connection.commit()
            return model
        else:
            raise ValueError("Unsupported database type")
        
    def migrate(self):
        if self.type_db == "redis":
            Migrator().run()
        else:
            raise NotImplementedError("Migration not implemented for this database type")

if __name__ == "__main__":
    # Make sure Redis is running and use the correct connection string
    db = UniversalDatabase(type_db="sqlite", connection="test.db")
    # Example usage
    class ExampleModel(UniversalModel):
        id: Annotated[int, pk()]  # Mark as primary key
        name: str
        value: float
    
    example = ExampleModel(id=1, name="Test", value=10.5)
    example = db.load_UniversalModel(example)
    example.save()
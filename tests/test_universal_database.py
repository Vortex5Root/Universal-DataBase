import unittest
import os
from typing import Annotated
from universal_database import UniversalDatabase, UniversalModel, pk

class TestModel(UniversalModel):
    id: Annotated[int, pk()]
    name: str
    value: float

class TestUniversalDatabase(unittest.TestCase):
    def setUp(self):
        # Create test databases
        self.sqlite_db_path = "test_sqlite.db"
        self.redis_url = "redis://localhost:6379"
        
        # Initialize databases
        self.sqlite_db = UniversalDatabase(type_db="sqlite", connection=self.sqlite_db_path)
        self.redis_db = UniversalDatabase(type_db="redis", connection=self.redis_url)
        
        # Test data
        self.test_model = TestModel(id=1, name="Test", value=10.5)

    def tearDown(self):
        # Clean up SQLite database
        if os.path.exists(self.sqlite_db_path):
            os.remove(self.sqlite_db_path)
        
        # Clean up Redis data
        if hasattr(self, 'redis_model'):
            self.redis_model.delete()

    def test_sqlite_crud(self):
        # Test Create
        model = self.sqlite_db.load_UniversalModel(self.test_model)
        model.save()
        
        # Test Read
        loaded_models = self.sqlite_db.load(TestModel)
        self.assertEqual(len(loaded_models), 1)
        loaded_model = loaded_models[0]
        self.assertEqual(loaded_model.id, self.test_model.id)
        self.assertEqual(loaded_model.name, self.test_model.name)
        self.assertEqual(loaded_model.value, self.test_model.value)
        
        # Test Update
        model.name = "Updated"
        model.save()
        loaded_models = self.sqlite_db.load(TestModel)
        self.assertEqual(loaded_models[0].name, "Updated")
        
        # Test Delete
        model.delete()
        loaded_models = self.sqlite_db.load(TestModel)
        self.assertEqual(len(loaded_models), 0)

    def test_redis_crud(self):
        # Test Create
        self.redis_model = self.redis_db.load_UniversalModel(self.test_model)
        self.redis_model.save()
        
        # Test Read
        loaded_models = self.redis_db.load(type(self.redis_model))
        self.assertEqual(len(loaded_models), 1)
        loaded_model = loaded_models[0]
        self.assertEqual(loaded_model.id, self.test_model.id)
        self.assertEqual(loaded_model.name, self.test_model.name)
        self.assertEqual(loaded_model.value, self.test_model.value)
        
        # Test Update
        self.redis_model.name = "Updated"
        self.redis_model.save()
        loaded_models = self.redis_db.load(type(self.redis_model))
        self.assertEqual(
            next(m for m in loaded_models if m.id == self.test_model.id).name,
            "Updated"
        )
        
        # Test Delete
        self.redis_model.delete()
        loaded_models = self.redis_db.load(type(self.redis_model))
        self.assertEqual(len(loaded_models), 0)

    def test_find_functionality(self):
        # Setup test data
        model = self.sqlite_db.load_UniversalModel(self.test_model)
        model.save()
        
        # Test find in SQLite
        found_models = self.sqlite_db.find(TestModel, name="Test")
        self.assertEqual(len(found_models), 1)
        self.assertEqual(found_models[0].id, self.test_model.id)
        
        # Setup Redis test data
        redis_model = self.redis_db.load_UniversalModel(self.test_model)
        redis_model.save()
        self.redis_model = redis_model  # Save for cleanup
        
        # Test find in Redis
        found_models = self.redis_db.find(type(redis_model), name="Test")
        self.assertEqual(len(found_models), 1)
        self.assertEqual(found_models[0].id, self.test_model.id)

    def test_error_handling(self):
        # Test unsupported database type
        with self.assertRaises(ValueError):
            UniversalDatabase(type_db="unknown")
        
        # Test invalid model data
        invalid_model = TestModel(id="invalid", name=123, value="not a float")
        with self.assertRaises(Exception):
            self.sqlite_db.load_UniversalModel(invalid_model)

if __name__ == '__main__':
    unittest.main()

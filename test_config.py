import os
import unittest
from app import create_app
from config import config

class TestConfig(unittest.TestCase):
    
    def test_development_config(self):
        """Test configuración de desarrollo"""
        app = create_app('development')
        self.assertTrue(app.config['DEBUG'])
        self.assertFalse(app.config['TESTING'])
    
    def test_testing_config(self):
        """Test configuración de testing"""
        app = create_app('testing')
        self.assertTrue(app.config['TESTING'])
        self.assertFalse(app.config['DEBUG'])
    
    def test_production_config(self):
        """Test configuración de producción"""
        app = create_app('production')
        self.assertFalse(app.config['DEBUG'])
        self.assertFalse(app.config['TESTING'])

if __name__ == '__main__':
    unittest.main()
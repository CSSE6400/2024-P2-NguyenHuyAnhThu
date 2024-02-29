from todo import create_app 
import unittest 
 
 #the base class help to setup our tests
class TodoTest(unittest.TestCase): 
    
    #The setUp method is called before each test
    def setUp(self): 
       self.app = create_app(config_overrides={ 
          'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:', 
          'TESTING': True 
       }) 
 
       self.client = self.app.test_client() 
 
    #The assertDictSubset method is a helper method that we will use to compare the todo items we get from the API with the todo items we expect to get from the API.
    def assertDictSubset(self, expected_subset: dict, whole: dict): 
       for key, value in expected_subset.items(): 
          self.assertEqual(whole[key], value)
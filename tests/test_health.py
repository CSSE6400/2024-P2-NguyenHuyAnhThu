from tests.base import TodoTest 
 
#This test will make a GET request to the /api/v1/health endpoint and check
#that the response is a 200 status code; and that the response is a JSON object with the key status and the value ok.
class TestHealth(TodoTest): 
    def test_health(self): 
       response = self.client.get('/api/v1/health') #call API
       self.assertEqual(response.status_code, 200) #test status code
       self.assertEqual(response.json, {'status': 'ok'}) #test response message
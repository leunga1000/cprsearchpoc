from rest_framework.test import APITestCase
from rest_framework.test import APIClient
# Create your tests here.


class ViewsTest(APITestCase):
	def test_policy_list(self):
		# self.force_login(self.user)
		resp = self.client.get('/policy/')
		self.assertTrue(resp.status_code==200)
		self.assertTrue(b'export' in resp.content) 
		first_doc = resp.json()[0]
		self.assertTrue(first_doc['id'] > 0) 
		self.assertTrue(first_doc['title'] != '') 
		self.assertTrue(first_doc['sectors'] is not None) 
		self.assertTrue(len(first_doc['description_text']) > 0) 


	def test_policy_get(self):
		# self.force_login(self.user)
		resp = self.client.get('/policy/10088/')
		self.assertTrue(resp.status_code==200)
		doc = resp.json()
		self.assertTrue(doc['id'] == 10088)
		self.assertTrue('Circular' in doc['title']) 
		self.assertTrue({'name': 'Industry'} in doc['sectors'])
		self.assertTrue({'name': 'Agriculture'} in doc['sectors'])
		self.assertTrue('efficiency' in doc['description_text']) 


	def test_policy_update(self):
		# self.force_login(self.user)
		resp = self.client.get('/policy/10088/')
		self.assertTrue(resp.status_code==200)
		doc = resp.json()
		doc['sectors'].append({'name': 'NEWSECTOR'})
		doc['description_text'] = doc['description_text'] + ' newstring1'
		print(doc['sectors'])
		client = APIClient()
		import json
		resp = self.client.patch('/policy/10088/', data=json.dumps(doc), content_type="application/json")
		print(resp, resp.status_code)
		print(resp.content)
		resp = self.client.get('/policy/10088/')
		print(resp, resp.status_code)
		doc = resp.json()
		self.assertTrue(doc['id'] == 10088) 
		self.assertTrue('Circular' in doc['title']) 
		self.assertTrue({'name': 'Industry'} in doc['sectors'])
		self.assertTrue({'name': 'Agriculture'} in doc['sectors'])
		print(doc['sectors'])
		self.assertTrue({'name': 'NEWSECTOR'} in doc['sectors'])
		self.assertTrue('newstring1' in doc['description_text']) 

	def test_policy_search(self):
		# self.force_login(self.user)
		resp = self.client.get('/policy/search/?q=export policy')
		self.assertTrue(resp.status_code==200)
		docs = resp.json()
		for d in docs:
			self.assertTrue('export' in d['description_text'].lower() 
				or 'policy' in d['description_text'].lower())
			self.assertTrue(d['jaccard_similarity'] > 0)
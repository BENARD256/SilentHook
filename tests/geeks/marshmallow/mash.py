from marshmallow import Schema, fields, validate, ValidationError
import json
from pprint import pprint

"""

Serialization : Dump ( Python Dict --> Json)

Deserialization : Load (json --> Python Dict

"""

ken = {"email": "ken@yahoo.com","name": "Ken", 'age':25}
benard = {'name':'Benard', 'email':'benard@test.com', 'age':22}
anzo = {'name':'Anzo', 'email':'anzo@test.com', 'age':20}

users = [ken, benard, anzo]



# Schema Takes Dictionary as input
class UserSchema(Schema):
	name = fields.Str(required=True)
	email = fields.Email()
	age = fields.Int(required=True)
	


def serialization():
	print("Serialization")
	# Python Data --> Json
	# dump

	schema = UserSchema()
		
	# Serializing a Single User
	
	result_one  = schema.dump(benard)

	pprint(result_one)
	
	# Serializing Many Users
	print("\n Serializing Many Users")
	results_many = schema.dump(users, many=True) # Takes a List
	
	pprint(results_many)
	
	

def deserialization():
	# Json to Python Data
	
	print("\n\nDeserialisation")
	
	schema = UserSchema()
	
	print("\n Deserializing One User")
	result_one = schema.load(benard) # Loading a Single Json User
	print(result_one)
	
	# Loading Many Json
	print("\n Deserializing Many Users")
	results_many = schema.load(users, many=True)
	print(results_many)
	



# DATA VALIDATION 
# Validation is applicable for Loaded data from requests
def validation():
	print("\n\nJson Validation")
	#ValidationError.message : Stores Validation Errors
	#Validation.valid_data : Stores Correctly validated data
	try:
		result_validate = UserSchema().load({"name": "John", "email": "foo", "age":'a'})
	except ValidationError as err:
		print(err.messages)  # => {"email": ['"foo" is not a valid email address.']}
		print(err.valid_data)  # => {"name": "John"}
		
	
	# Validating a Collection
	print("\n\nValidating Many Users")
	users_data = [
		{"email": "mick@stones.com", "name": "Mick", "age":30},
		{"email": "invalid", "name": "Invalid"},  # invalid email
		{"email": "keith@stones.com", "name": "Keith"},
		{"email": "charlie@stones.com"},  # missing "name"
	]
	
	try:
		results = UserSchema().load(users_data, many=True)
	except ValidationError as err:
		pprint(err.messages)
	
	
if __name__ == "__main__":
	serialization()
	deserialization()
	validation()

  
# Boilerplate example of creating a Flask server with encrypted db columns  
  
## Table definition  
  
The current server has a single database table defined, called `Users`.  
  
This table has the following definition:  
```  
id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)  
username = db.Column(db.String, nullable=False)  
password = db.Column(db.String, nullable=False)  
user_type = db.Column(db.String, nullable=False)  
email = db.Column(EncryptedType(sa.Unicode, config.POSTGRES_SECRET_KEY, AesEngine, 'pkcs5'), nullable=False)  
```  
  
Of note is the `email` column, which is set up as a Unicode Encrypted-Type. This means that the SQLAlchemy ORM will automatically:
- encrypt this field when storing it in the database
- decrypt it after it's retrieved from the database

This helps you ensure the following two properties:
- **encryption-at-rest:** The data stored on the database itself will always be the encrypted value, and without the key (that only the API has) there is no way to decrypt it
- **encryption-in-transit:** Similarly, since the data is always encrypted when it's interacting with the database (pushing an encrypted value or querying an encrypted value), we establish encryption-in-transit

This is especially useful for Postgresql databases as there is no native way to enable encryption-at-rest, and therefore it becomes the responsibility of the API to do so if the need arises.
  
## Example record  
  
Here is an example database record:  
```
enc=# select * from users;  
-[ RECORD 1 ]--------------------------------------------------------------------------------------------------------------------------------  
id         | c4cc1314-26ee-4fed-803c-ef47d415c758  
username   | admin  
password   | 60374fa84f18f9bc851ef6929bf090088644eab3a0003181e9cc05b2946da74412e135b2c04d06a02bc7fc89a3aa834b2f984c117fa29ee47ab7b2b7e7372449  
user_type  | admin  
email      | \x6a7339557661434f354b4861366e3857526a35783066724765464e2b6e694764635762544e52445646446b3d  
created_at | 2023-01-20 19:31:56.46987+00  
```
  
Once again, note the `email` field and how it's encrypted as a unicode type. 
  
Now, if we were to query our API and ask for this user's data, we get the decrypted email address: 
```
{  
  "payload": {  
    "created_at": "2023-01-20T14:31:56.469870-05:00",  
    "email": "admin@example.com",  
    "id": "c4cc1314-26ee-4fed-803c-ef47d415c758",  
    "password": "60374fa84f18f9bc851ef6929bf090088644eab3a0003181e9cc05b2946da74412e135b2c04d06a02bc7fc89a3aa834b2f984c117fa29ee47ab7b2b7e7372449",  
    "updated_at": null,  
    "user_type": "admin",  
    "username": "admin"  
  }  
}
```
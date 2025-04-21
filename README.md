
# Pet Adoption System

A FastApi app for a pet adoption system with role-based authentication (admin & users), allowing users to adopt pets.

## **Features**
- User authentication with JWT (Signup, Login, Logout, Refresh)  
- Role-based access control (Admin & User)  
- CRUD operations for pets (Admin only)  
- Adoption & return of pets (Users only)  
- MySQL database integration  
- Automated testing with Pytest   
---

## **Installation**
### **1. Clone the Repository**
```sh
git clone <repository_url>
cd pet_adoption_system
```

### **2. Create and Activate Virtual Environment**
```sh
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows
```

### **3. Install Dependencies**
```sh
pip install -r requirements.txt
```

### **4. Configure MySQL Database**

#### Create Database
###### open mysql shell
```
create database your_db_name;
create database your_test_db_name;
```

#### Update `.env` with your **MySQL and django credentials**:

```ini
DATABASE_URL=your_db_url
TEST_DATABASE_URL=your_test_db_url
```

### **6. Run server**
```sh
uvicorn app.main:app --reload
```

The API will be available at http://127.0.0.1:8000

To access swagger ui for all endpoints, visit : http://127.0.0.1:8000/docs

---

### Admin Credentials

- **Username**: `admin`
- **Password**: `admin123`

Use these credentials to log in and obtain a JWT token for accessing admin protected endpoints.

---

## **API Endpoints**

### Auth
| Endpoint      | Method | Description              | Auth Required |
| ------------- | ------ | ------------------------ | ------------- |
| /auth/signup  | POST   | Register a new user      | No            |
| /auth/login   | POST   | Login and receive tokens | No            |
| /auth/logout  | POST   | Logout the user          | Yes           |
| /auth/me      | GET    | Get user details         | Yes           |
| /auth/me      | PUT    | Update user details      | Yes           |
| /auth/refresh | POST   | create new access token  | Yes           |

### Admin
| Endpoint         | Method | Description              | Auth Required |
| ---------------- | ------ | ------------------------ | ------------- |
| /admin/add_pet   | POST   | Add a new pet      | Yes (Admin)   |
| /admin/pets/update/{pet_id} | PUT    | Update a pet by pet_id | Yes (Admin)   |
| /admin/pets/delete/{pet_id} | DELETE | Delete a pet by ID | Yes (Admin)   |
| /admin/pets    | GET    | View all pets          | Yes (Admin)   |
| /admin/adoptions    | GET    | View all adoptions          | Yes (Admin)   |


### User
| Endpoint             | Method | Description             | Auth Required |
| -------------------- | ------ | ----------------------- | ------------- |
| /pets/          | GET    | Get adoptable pets            | No            |
| /pets/{pet_id}/adopt          | POST   | Adopt a pet          | Yes           |
| /pets/{pet_id}/return    | DELETE | Return pet   | Yes           |
| /pets/history | GET    | View uadoption history | Yes           |

---

## **Testing**
### **Run Tests with Pytest**
```sh
pytest
```

---

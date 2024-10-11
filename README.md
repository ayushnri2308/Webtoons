
# Webtoon REST API

This project is a RESTful API built using Flask for managing webtoon data. It allows users to fetch, add, and delete webtoon entries, with security measures such as input validation, rate limiting, and JWT-based authentication for protected endpoints. The API connects to a PostgreSQL database for storing webtoon information.

In case you face error in running code i have recorded a demo video of same :
https://drive.google.com/file/d/1TNfumpTsYz4EMSPQp_i9ko9s3jtBMzBv/view?usp=drive_link


## Features
- **Fetch webtoon data**: Retrieve webtoon entries stored in the database.
- **Add webtoon entries**: Add new webtoons with fields such as title, summary, and character list.
- **Delete webtoon entries**: Remove existing webtoons by ID.
- **JWT Authentication**: Secure certain endpoints using JWT-based authentication.
- **Input validation**: Ensure data integrity through validation of inputs.
- **Rate limiting**: Prevent abuse by limiting the number of requests allowed.

## Technologies Used
- **Flask**: A lightweight web framework for building the RESTful API.
- **PostgreSQL**: A robust relational database for managing webtoon data.
- **JWT (JSON Web Tokens)**: Used for secure authentication.
- **Input Validation**: Ensures the API receives correctly formatted data.
- **Rate Limiting**: Throttles requests to prevent abuse.

## API Endpoints

### 1. Fetch All Webtoons
**Endpoint**: `/webtoons`  
**Method**: `GET`  
**Description**: Retrieves all webtoon entries from the database.  
**Protected**: No

### 2. Fetch Single Webtoon
**Endpoint**: `/webtoons/<id>`  
**Method**: `GET`  
**Description**: Retrieves a webtoon entry by its ID.  
**Protected**: No

### 3. Add a New Webtoon
**Endpoint**: `/webtoons/add`  
**Method**: `POST`  
**Description**: Adds a new webtoon entry.  
**Protected**: Yes (JWT authentication required)  
**Input Fields**:
- `title`: The title of the webtoon.
- `summary`: A brief summary of the webtoon.
- `characters`: A comma-separated string of character names.

### 4. Delete a Webtoon
**Endpoint**: `/webtoons/delete/<id>`  
**Method**: `DELETE`  
**Description**: Deletes a webtoon by its ID.  
**Protected**: Yes (JWT authentication required)

## Authentication
JWT tokens are required for adding and deleting webtoons. You can obtain a token by signing in through the `/login` endpoint with a valid username and password.

## Database
The webtoon data is stored in a PostgreSQL database. The connection string to the database can be modified in the `.env` file:

```
DATABASE_URL=postgresql://<username>:<password>@localhost/webtoon
```

Ensure to replace `<username>` and `<password>` with your actual database credentials.

## Installation and Setup

1. **Clone the repository**:


2. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

3. **Set up PostgreSQL database**:
   Ensure you have PostgreSQL installed and running. Create a database and set the URL in `.env`.

4. **Run the application**:
   ```
   flask run
   ```


## Usage

### 1. Fetch all webtoons
```bash
curl http://localhost:5000/webtoons
```

### 2. Add a webtoon (JWT required)
```bash
curl -X POST http://localhost:5000/webtoons/add   -H "Authorization: Bearer <your_jwt_token>"   -d "title=Castle Swimmer"   -d "summary=A thrilling underwater adventure"   -d "characters=Jae-won, Su-min, Kwang-soo, Eun-young, The Guardian"
```

### 3. Delete a webtoon (JWT required)
```bash
curl -X DELETE http://localhost:5000/webtoons/delete/1   -H "Authorization: Bearer <your_jwt_token>"
```

## Security Considerations
- **JWT Authentication**: Protects sensitive API operations such as adding or deleting webtoons.
- **Rate Limiting**: Prevents excessive requests to the API.
- **Input Validation**: Ensures that the data provided to the API is correctly formatted.

## Contributing
Contributions are welcome! Please fork this repository and submit a pull request with your changes.

## License
This project is licensed under the MIT License.

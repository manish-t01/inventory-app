# 📦 Inventory Management System

A full-stack **Inventory Management System** built with **Java, Spring Boot, MySQL, HTML, CSS, and JavaScript**.

The application is designed to help businesses manage products, product variants, stores, inventory transactions, daily records, reports, and stock-related operations from a single web application.

---

## 🚀 Features

### 📊 Dashboard

* Overview of inventory-related information
* Quick access to major sections of the application
* Centralized navigation

### 📦 Product Management

* Create and manage products
* Manage product variants
* Set product and variant prices
* Update existing products and variants
* Product prices can be used in daily inventory workflows

### 🏪 Store Management

* Manage multiple stores
* Store-specific inventory management
* View store-related information

### 📋 Daily Entry

* Record daily inventory activities
* Add products and variants to daily records
* Record quantities and prices
* Maintain historical daily records

### 📈 Reports

* Daily inventory reports
* Aggregated reports
* Store-based reports
* Generate inventory-related reports
* Export report data to CSV/PDF

### 📦 Inventory Management

* Track inventory transactions
* Handle stock adjustments
* Track purchases and sales
* Maintain inventory history

### 👤 User & Role Management

* User entity and repository structure
* Role-based application foundation

---

## 🛠️ Tech Stack

### Backend

* **Java**
* **Spring Boot**
* **Spring Web**
* **Spring Data JPA**
* **Hibernate**
* **Maven**

### Database

* **MySQL**

### Frontend

* **HTML5**
* **CSS3**
* **JavaScript**

### Reporting & File Processing

* CSV generation
* PDF generation

### Development Tools

* Git
* GitHub
* Maven Wrapper

---

## 🏗️ Project Structure

```text
inventory-app/
│
├── .mvn/
│   └── wrapper/
│
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/multistore/inventory/
│   │   │       ├── config/
│   │   │       ├── controller/
│   │   │       ├── dto/
│   │   │       ├── entity/
│   │   │       ├── repository/
│   │   │       └── service/
│   │   │
│   │   └── resources/
│   │       ├── static/
│   │       │   ├── css/
│   │       │   ├── js/
│   │       │   └── *.html
│   │       │
│   │       ├── application.properties
│   │       └── application-example.properties
│   │
│   └── test/
│
├── pom.xml
├── mvnw
├── mvnw.cmd
├── .gitignore
├── LICENSE
└── README.md
```

---

## ⚙️ Requirements

Before running the project, make sure you have:

* **Java 17+**
* **Maven** (optional because the project includes Maven Wrapper)
* **MySQL 8+**
* A modern web browser
* Git

Check Java:

```bash
java -version
```

Check Maven:

```bash
mvn -version
```

---

## 🔧 Setup

### 1. Clone the Repository

```bash
git clone https://github.com/manish-t01/inventory-app.git
```

Move into the project:

```bash
cd inventory-app
```

---

### 2. Create the MySQL Database

Create a database in MySQL:

```sql
CREATE DATABASE inventory_db;
```

---

### 3. Configure the Database

Open:

```text
src/main/resources/application.properties
```

Configure your MySQL connection:

```properties
spring.datasource.url=jdbc:mysql://localhost:3306/inventory_db
spring.datasource.username=YOUR_USERNAME
spring.datasource.password=YOUR_PASSWORD
```

> **Important:** Never commit real database passwords, API keys, tokens, or other secrets to GitHub.

For sharing configuration safely, use:

```text
application-example.properties
```

as a template.

---

## ▶️ Running the Application

### Using Maven Wrapper

On Windows:

```bash
.\mvnw.cmd spring-boot:run
```

On Linux/macOS:

```bash
./mvnw spring-boot:run
```

### Using Maven

```bash
mvn spring-boot:run
```

Once the application starts, open:

```text
http://localhost:8080
```

---

## 🧪 Running Tests

Run the test suite with:

```bash
.\mvnw.cmd test
```

or:

```bash
mvn test
```

---

## 🔌 Main Application Components

The backend follows a layered architecture:

```text
Controller
    ↓
Service
    ↓
Repository
    ↓
Database
```

### Controllers

The application currently includes controllers for:

* Inventory
* Products
* Reports
* Stores

### Services

The service layer contains functionality for:

* Inventory management
* Product management
* Store management
* Reports
* CSV processing
* PDF generation
* File storage
* Data seeding

### Entities

The application contains entities for areas such as:

* Product
* Product Variant
* Store
* User
* Purchase
* Sale
* Expense
* Inventory Transaction
* Stock Adjustment
* Daily Record
* Daily Record Item

---

## 🔄 Application Flow

A simplified application workflow looks like this:

```text
        User
         │
         ▼
    Web Interface
         │
         ▼
    REST Endpoints
         │
         ▼
     Controllers
         │
         ▼
      Services
         │
         ▼
    Repositories
         │
         ▼
       MySQL
```

---

## 🔐 Security

This project is configured to keep environment-specific configuration separate from the example configuration.

Before deploying the application:

* Change default database credentials
* Never expose production passwords
* Never commit `.env` files
* Never commit API keys or access tokens
* Use environment variables or secure configuration for production
* Review `.gitignore` before committing

---

## 📌 Current Status

**Project Status: MVP / Active Development**

The core inventory management functionality has been implemented, including:

* Product management
* Product variant management
* Store management
* Daily inventory records
* Inventory transactions
* Stock adjustments
* Reporting
* CSV/PDF report generation
* Web-based frontend

Additional features and improvements may be added as development continues.

---

## 🗺️ Future Improvements

Possible future improvements include:

* 🔐 Complete authentication and authorization
* 👥 Advanced role-based access control
* 📱 Responsive mobile UI improvements
* 📊 More advanced analytics and dashboards
* 🔔 Low-stock notifications
* 📦 Barcode/QR code support
* ☁️ Cloud deployment
* 🐳 Docker support
* 🧪 Expanded automated testing
* 📜 Audit logs
* ⚡ Performance optimization

---

## 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

If you find a bug or have an idea for improving the application, feel free to open an **Issue** or submit a **Pull Request**.

---

## 📄 License

This project is licensed under the **MIT License**.

See the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Manish Kumar Thakur**

GitHub:
https://github.com/manish-t01

---

⭐ If you find this project useful or interesting, consider giving it a **star** on GitHub.

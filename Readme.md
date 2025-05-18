# AutoRia Scraper

## 📌 Overview

This project is a fully automated web scraper for the [AutoRia](https://auto.ria.com/) platform. It collects data daily
about used cars listed on AutoRia, stores it in a PostgreSQL database, and performs daily database backups. The scraper
is designed to run autonomously using a scheduled job and is deployed using Docker Compose.

---

## ⚙️ Features

- ✅ Scrapes all listings of used cars
- ✅ Parses details from each car's listing page
- ✅ Saves the data to a PostgreSQL database (with duplicate filtering)
- ✅ Performs daily database dump to a `/dumps` directory
- ✅ Scheduled task with APScheduler
- ✅ Full Docker + Docker Compose support
- ✅ Logging included
- ✅ pgAdmin for viewing and managing the database

---

## 🚀 How to Run

### 1. Clone the repository

```bash
git clone https://github.com/Anton0729/AutoRia-Scraper.git
cd AutoRia-Scraper
```

### 2. Create `.env` file

### 3. Build and run with Docker Compose

```bash
docker-compose up --build
```

This command will:

- Set up the PostgreSQL database
- Launch the scraper
- Start the scheduler that runs daily at the time specified in `.env`

## 🗄️ Using pgAdmin

pgAdmin is included in the Docker setup for easy database access via a web interface.

### 🔗 Open pgAdmin in your browser

[http://localhost:80](http://localhost:5050)

---

## 📦 Dependencies

Install locally with:

```bash
pip install -r requirements.txt
```

But **Docker is recommended** for full setup.

---

## 📑 Database Schema

Table: `cars`

| Field          | Type      | Description                      |
|----------------|-----------|----------------------------------|
| url            | TEXT      | Car listing URL                  |
| title          | TEXT      | Listing title                    |
| price_usd      | INTEGER   | Price in USD                     |
| odometer       | INTEGER   | Kilometers, cleaned (e.g. 95000) |
| username       | TEXT      | Seller name                      |
| phone_number   | TEXT      | Seller phone number (+380...)    |
| image_url      | TEXT      | URL to main image                |
| images_count   | INTEGER   | Number of images in listing      |
| car_number     | TEXT      | License plate number             |
| car_vin        | TEXT      | VIN number                       |
| datetime_found | TIMESTAMP | Time when entry was scraped      |

---

## 📌 Cron Schedule

The scraper is scheduled using APScheduler.

- Runs daily at the time defined in the `.env` file.
- Database dumps are also created at the same time in the `dumps/` folder.

---

## 🙋 Author

Created by **Anton Skazko**
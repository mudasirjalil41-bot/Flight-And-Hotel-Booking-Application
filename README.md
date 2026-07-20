# Flight and Hotel Booking System (Backend API)

A robust, enterprise-ready backend REST API built with Django and Django REST Framework (DRF) to manage flight and hotel reservations safely and efficiently.

## 🚀 Key Technical Features

* **Data Integrity & Concurrency:** Implemented `transaction.atomic()` and `select_for_update()` to handle race conditions during high-traffic booking scenarios, preventing double-bookings of rooms or seats.
* **Automated Inventory Restoration:** Features smart cancellation logic that instantly injects rooms/seats back into the active hotel or flight inventory upon a successful cancellation request.
* **Safety & Enforced Validation:** Implemented a strict safety gate (`?confirm=true` query parameter) for handling `DELETE` requests to avoid accidental cancellations.
* **Secure Token Authentication:** Protected API endpoints using DRF's Token Authentication mechanism, ensuring only authorized users can book or view receipts.
* **Django Admin Integration:** Fully customized admin portal to manage flights, hotels, inventory, and users seamlessly.

---

## 🛠️ Tech Stack
* **Language:** Python
* **Framework:** Django & Django REST Framework (DRF)
* **Database:** SQLite (Local) / PostgreSQL Ready
* **Tools:** PyCharm, Git, GitHub

---

## 💻 API Endpoints & Flow

### 1. Authentication
* `POST /api-auth/login/` - User Login & Token Generation
* `POST /api-auth/logout/` - Token Invalidation

### 2. Booking Core
* `GET /hotel_booking/` - View all active hotel bookings
* `POST /hotel_booking/` - Create a new hotel booking (Atomically reduces inventory)
* `GET /flight_booking/` - View all active flight bookings
* `POST /flight_booking/` - Create a new flight booking (Atomically reduces inventory)

### 3. Safe Cancellations
* `DELETE /hotel_booking/<id>/?confirm=true` - Cancels booking & restores room inventory safely.

---

## 🔧 Installation & Local Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/mudasirjalil41-bot/Flight-And-Hotel-Booking-Application.git](https://github.com/mudasirjalil41-bot/Flight-And-Hotel-Booking-Application.git)
   cd Flight-And-Hotel-Booking-Application/myproject

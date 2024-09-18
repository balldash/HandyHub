# HandyHub

## Introduction

HandyHub is a web application designed to connect clients with reliable, skilled tradesmen in their area. Our goal is to streamline the process of finding and hiring tradesmen, making it easier for clients to access services such as plumbing, electrical work, and other essential repairs through a user-friendly platform. 

For a detailed overview, read the [final project blog article](https://dev.to/bislon_azulu_8947d844c5c/handyhub-your-go-to-tradesman-directory-9c2).

## Author(s)

- [Bislon Zulu](https://www.linkedin.com/in/bislonzulu/)

## Installation

To run HandyHub locally, follow these steps:

1. **Clone the repository:**

    ```bash
    git clone https://github.com/balldash/HandyHub.git
    ```

2. **Navigate to the project directory:**

    ```bash
    cd HandyHub
    ```

3. **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

4. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

5. **Set up the database:**

    Update the `config.py` file with your PostgreSQL database credentials. Then, run:

    ```bash
    flask db upgrade
    ```

6. **Run the application:**

    ```bash
    flask run
    ```

## Usage

Once the application is running, you can access it at `http://127.0.0.1:5000`. 

- **For Clients:** Search for tradesmen by location and specialization, and view their profiles.
- **For Tradesmen:** Create and manage your profile to showcase your skills, certifications, and contact details.

## Contributing

We welcome contributions to improve HandyHub. If you have suggestions or fixes, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a pull request.

---

Thank you for checking out HandyHub. Feel free to reach out if you have any questions or feedback!

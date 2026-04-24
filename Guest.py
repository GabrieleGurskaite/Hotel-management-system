class Guest:
    def __init__(self, name, surname, phone, guest_id, email):
        if not name.strip() or not surname.strip():
            raise ValueError("Name and surname cannot be empty.")
        if guest_id <= 0:
            raise ValueError("Guest ID must be positive.")
        if not re.fullmatch(r"\+370\d{8}", phone):
            raise ValueError("Phone must be in format +370XXXXXXXX.")
        if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format.")

        self.name = name.strip()
        self.surname = surname.strip()
        self.phone = phone
        self.guest_id = guest_id
        self.email = email.strip()

    def __str__(self):
        return (
            f"ID: {self.guest_id} | {self.name} {self.surname} | "
            f"Phone: {self.phone} | Email: {self.email}"
        )

import reflex as rx
from typing import TypedDict, Optional
import base64
import uuid
import logging


class User(TypedDict):
    full_name: str
    email: str
    password: str
    photo_filename: str


class AuthState(rx.State):
    users: dict[str, User] = {}
    logged_in_user_email: str = ""
    error_message: str = ""
    show_webcam: bool = False
    img: str = ""

    @rx.var
    def logged_in_user(self) -> Optional[User]:
        return self.users.get(self.logged_in_user_email)

    @rx.var
    def is_logged_in(self) -> bool:
        return self.logged_in_user is not None

    @rx.var
    def is_admin(self) -> bool:
        if not self.logged_in_user or not self.users:
            return False
        first_user_email = next(iter(self.users), None)
        return self.logged_in_user_email == first_user_email

    @rx.var
    def all_users(self) -> list[User]:
        return list(self.users.values())

    @rx.event
    def logout(self):
        self.logged_in_user_email = ""
        return rx.redirect("/login")

    @rx.event
    def handle_login(self, form_data: dict):
        self.error_message = ""
        email = form_data.get("email", "").lower()
        password = form_data.get("password", "")
        if not email or not password:
            self.error_message = "Email and password are required."
            return
        user = self.users.get(email)
        if user and user["password"] == password:
            self.logged_in_user_email = email
            return rx.redirect("/")
        else:
            self.error_message = "Invalid credentials. Please try again."

    @rx.event
    async def handle_signup(self, form_data: dict):
        self.error_message = ""
        full_name = form_data.get("full_name")
        email = form_data.get("email", "").lower()
        password = form_data.get("password")
        if not all([full_name, email, password]):
            self.error_message = "All fields are required."
            return
        if not self.img:
            self.error_message = "Please capture a photo."
            return
        if email in self.users:
            self.error_message = "User with this email already exists."
            return
        try:
            filename = f"{uuid.uuid4()}.png"
            upload_dir = rx.get_upload_dir()
            upload_dir.mkdir(parents=True, exist_ok=True)
            file_path = upload_dir / filename
            header, encoded = self.img.split(",", 1)
            data = base64.b64decode(encoded)
            with file_path.open("wb") as f:
                f.write(data)
            new_user = User(
                full_name=full_name,
                email=email,
                password=password,
                photo_filename=filename,
            )
            self.users[email] = new_user
            self.logged_in_user_email = email
            self.show_webcam = False
            self.img = ""
            return rx.redirect("/")
        except Exception as e:
            logging.exception(f"Error during signup: {e}")
            self.error_message = f"An error occurred during signup."

    @rx.event
    def toggle_webcam(self):
        self.show_webcam = not self.show_webcam
        self.img = ""
        self.error_message = ""

    @rx.event
    def capture_img(self, data_uri: str):
        self.img = data_uri
        self.show_webcam = False

    @rx.event
    def reset_auth_forms(self):
        self.error_message = ""
        self.show_webcam = False
        self.img = ""
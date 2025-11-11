import reflex as rx
from typing import Optional
from app.states.auth_state import AuthState
from app.states.admin_state import AdminState, AttendanceSession
import datetime


class AttendanceState(rx.State):
    show_webcam: bool = False
    img: str = ""
    processing: bool = False
    attendance_message: str = ""
    active_session: Optional[AttendanceSession] = None
    has_marked_attendance: bool = False

    async def _update_active_session_and_status(self):
        admin_state = await self.get_state(AdminState)
        auth_state = await self.get_state(AuthState)
        admin_state._check_sessions()
        self.active_session = None
        for session in admin_state.active_sessions:
            if session["date"] == datetime.date.today().isoformat():
                start_time = datetime.datetime.strptime(
                    session["start_time"], "%H:%M"
                ).time()
                end_time = datetime.datetime.strptime(
                    session["end_time"], "%H:%M"
                ).time()
                now = datetime.datetime.now().time()
                if start_time <= now <= end_time:
                    self.active_session = session
                    break
        self.has_marked_attendance = False
        if self.active_session and auth_state.logged_in_user:
            if auth_state.logged_in_user["email"] in self.active_session["attendees"]:
                self.has_marked_attendance = True

    @rx.event
    def toggle_webcam(self):
        self.show_webcam = not self.show_webcam
        self.img = ""
        self.attendance_message = ""

    @rx.event
    def capture_img(self, data_uri: str):
        self.img = data_uri
        self.show_webcam = False

    @rx.event
    async def mark_attendance(self):
        self.processing = True
        self.attendance_message = ""
        auth_state = await self.get_state(AuthState)
        admin_state = await self.get_state(AdminState)
        if not self.img:
            self.attendance_message = "Please capture a photo for verification."
            self.processing = False
            return
        await self._update_active_session_and_status()
        if not self.active_session:
            self.attendance_message = "No active attendance session found."
            self.processing = False
            return
        user_email = auth_state.logged_in_user["email"]
        timestamp = datetime.datetime.now().isoformat()
        for i, session in enumerate(admin_state.attendance_sessions):
            if session["id"] == self.active_session["id"]:
                admin_state.attendance_sessions[i]["attendees"].update(
                    {user_email: timestamp}
                )
                break
        self.attendance_message = "Attendance marked successfully!"
        self.processing = False
        self.img = ""
        self.has_marked_attendance = True

    @rx.event
    async def on_attendance_page_load(self):
        self.show_webcam = False
        self.img = ""
        self.processing = False
        self.attendance_message = ""
        await self._update_active_session_and_status()
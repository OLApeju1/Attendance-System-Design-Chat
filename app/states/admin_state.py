import reflex as rx
import datetime
import uuid
from typing import TypedDict
from app.states.auth_state import AuthState


class AttendanceSession(TypedDict):
    id: str
    date: str
    start_time: str
    end_time: str
    active: bool
    attendees: dict[str, str]


class AdminState(rx.State):
    attendance_sessions: list[AttendanceSession] = []
    current_view: str = "Users"
    selected_session_id: str | None = None

    @rx.event
    def set_current_view(self, view: str):
        self.current_view = view

    @rx.event
    def toggle_session_details(self, session_id: str):
        if self.selected_session_id == session_id:
            self.selected_session_id = None
        else:
            self.selected_session_id = session_id

    @rx.event
    def create_attendance_session(self, form_data: dict):
        date = form_data.get("date")
        start_time = form_data.get("start_time")
        end_time = form_data.get("end_time")
        if not all([date, start_time, end_time]):
            return
        now = datetime.datetime.now()
        session_datetime_start = datetime.datetime.strptime(
            f"{date} {start_time}", "%Y-%m-%d %H:%M"
        )
        new_session = AttendanceSession(
            id=str(uuid.uuid4()),
            date=date,
            start_time=start_time,
            end_time=end_time,
            active=session_datetime_start > now,
            attendees={},
        )
        self.attendance_sessions.append(new_session)
        self.attendance_sessions.sort(
            key=lambda s: s["date"] + s["start_time"], reverse=True
        )

    @rx.event
    async def clear_all_users(self):
        auth_state = await self.get_state(AuthState)
        if not auth_state.users:
            return
        admin_email = next(iter(auth_state.users))
        admin_user = auth_state.users[admin_email]
        auth_state.users = {admin_email: admin_user}
        if auth_state.logged_in_user_email != admin_email:
            auth_state.logged_in_user_email = ""

    @rx.event
    def clear_all_attendance_data(self):
        self.attendance_sessions = []

    def _check_sessions(self):
        now = datetime.datetime.now()
        for session in self.attendance_sessions:
            end_datetime = datetime.datetime.strptime(
                f"{session['date']} {session['end_time']}", "%Y-%m-%d %H:%M"
            )
            if session["active"] and now > end_datetime:
                session["active"] = False

    @rx.var
    def active_sessions(self) -> list[AttendanceSession]:
        self._check_sessions()
        return [s for s in self.attendance_sessions if s["active"]]

    @rx.var
    def past_sessions(self) -> list[AttendanceSession]:
        self._check_sessions()
        return [s for s in self.attendance_sessions if not s["active"]]
import reflex as rx
from app.states.auth_state import AuthState, User
from app.states.admin_state import AdminState
from app.components.admin_sidebar import admin_sidebar


def users_management() -> rx.Component:
    return rx.el.div(
        rx.el.h2("User Management", class_name="text-2xl font-bold text-gray-900"),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "Photo",
                            class_name="p-3 text-left text-sm font-semibold text-gray-600",
                        ),
                        rx.el.th(
                            "Full Name",
                            class_name="p-3 text-left text-sm font-semibold text-gray-600",
                        ),
                        rx.el.th(
                            "Email",
                            class_name="p-3 text-left text-sm font-semibold text-gray-600",
                        ),
                        class_name="border-b bg-gray-50",
                    )
                ),
                rx.el.tbody(rx.foreach(AuthState.all_users, user_row)),
                class_name="w-full table-auto",
            ),
            class_name="overflow-hidden rounded-lg border border-gray-200 bg-white",
        ),
        class_name="space-y-6",
    )


def user_row(user: User) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.image(
                src=rx.get_upload_url(user["photo_filename"]),
                class_name="h-10 w-10 rounded-full object-cover",
            ),
            class_name="p-3",
        ),
        rx.el.td(user["full_name"], class_name="p-3 text-sm text-gray-800 font-medium"),
        rx.el.td(user["email"], class_name="p-3 text-sm text-gray-600"),
        class_name="border-b",
    )


def attendance_roster_row(user: User, attendees: dict) -> rx.Component:
    is_present = attendees.contains(user["email"])
    return rx.el.tr(
        rx.el.td(
            rx.el.image(
                src=rx.get_upload_url(user["photo_filename"]),
                class_name="h-8 w-8 rounded-full object-cover",
            ),
            class_name="p-2",
        ),
        rx.el.td(user["full_name"], class_name="p-2 text-sm font-medium"),
        rx.el.td(
            rx.cond(
                is_present,
                rx.icon("square_check", class_name="h-5 w-5 text-green-600"),
                rx.icon("circle_x", class_name="h-5 w-5 text-red-500"),
            ),
            class_name="p-2 text-center",
        ),
        class_name="border-b",
    )


def attendance_roster_table(session: dict) -> rx.Component:
    return rx.el.div(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    rx.el.th(
                        "Photo",
                        class_name="p-2 text-left text-xs font-semibold text-gray-500",
                    ),
                    rx.el.th(
                        "Full Name",
                        class_name="p-2 text-left text-xs font-semibold text-gray-500",
                    ),
                    rx.el.th(
                        "Status",
                        class_name="p-2 text-center text-xs font-semibold text-gray-500",
                    ),
                    class_name="bg-gray-50",
                )
            ),
            rx.el.tbody(
                rx.foreach(
                    AuthState.all_users,
                    lambda user: attendance_roster_row(user, session["attendees"]),
                )
            ),
            class_name="w-full table-auto",
        ),
        class_name="mt-4 overflow-hidden rounded-md border",
    )


def attendance_card(session: dict) -> rx.Component:
    attendee_count = session["attendees"].keys().length()
    is_selected = AdminState.selected_session_id == session["id"]
    return rx.el.div(
        rx.el.button(
            rx.el.div(
                rx.el.div(
                    rx.el.p(session["date"], class_name="font-semibold text-gray-900"),
                    rx.el.p(
                        f"{session['start_time']} - {session['end_time']}",
                        class_name="text-sm text-gray-600",
                    ),
                    class_name="flex-1 text-left",
                ),
                rx.el.div(
                    rx.icon("users", class_name="h-4 w-4 text-gray-500"),
                    rx.el.p(
                        f"{attendee_count} / {AuthState.all_users.length()}",
                        class_name="text-sm font-medium",
                    ),
                    class_name="flex items-center gap-2 rounded-full bg-gray-100 px-3 py-1",
                ),
                rx.icon(
                    rx.cond(is_selected, "chevron_up", "chevron_down"),
                    class_name="h-5 w-5 text-gray-500",
                ),
                class_name="flex w-full items-center",
            ),
            rx.cond(is_selected, attendance_roster_table(session), rx.fragment()),
            on_click=lambda: AdminState.toggle_session_details(session["id"]),
            class_name="w-full rounded-lg border p-4 text-left transition-all hover:bg-gray-50",
        )
    )


def attendance_management() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Attendance Management", class_name="text-2xl font-bold text-gray-900"
        ),
        rx.el.form(
            rx.el.div(
                rx.el.h3(
                    "Create New Session",
                    class_name="text-lg font-semibold text-gray-800",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Date", class_name="text-sm font-medium text-gray-700"
                        ),
                        rx.el.input(
                            type="date",
                            name="date",
                            required=True,
                            class_name="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500",
                        ),
                        class_name="flex-1 space-y-1",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Start Time", class_name="text-sm font-medium text-gray-700"
                        ),
                        rx.el.input(
                            type="time",
                            name="start_time",
                            required=True,
                            class_name="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500",
                        ),
                        class_name="flex-1 space-y-1",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "End Time", class_name="text-sm font-medium text-gray-700"
                        ),
                        rx.el.input(
                            type="time",
                            name="end_time",
                            required=True,
                            class_name="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500",
                        ),
                        class_name="flex-1 space-y-1",
                    ),
                    class_name="flex flex-col md:flex-row gap-4",
                ),
                rx.el.button(
                    "Create Session",
                    type="submit",
                    class_name="rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-700",
                ),
                class_name="space-y-4",
            ),
            on_submit=AdminState.create_attendance_session,
            reset_on_submit=True,
            class_name="rounded-lg border border-gray-200 bg-white p-6",
        ),
        rx.el.div(
            rx.el.h3(
                "Active Sessions", class_name="text-lg font-semibold text-gray-800"
            ),
            rx.cond(
                AdminState.active_sessions.length() == 0,
                rx.el.p("No active sessions.", class_name="text-sm text-gray-500"),
                rx.el.div(
                    rx.foreach(AdminState.active_sessions, attendance_card),
                    class_name="grid grid-cols-1 md:grid-cols-2 gap-4",
                ),
            ),
            class_name="space-y-4",
        ),
        rx.el.div(
            rx.el.h3("Past Sessions", class_name="text-lg font-semibold text-gray-800"),
            rx.cond(
                AdminState.past_sessions.length() == 0,
                rx.el.p("No past sessions.", class_name="text-sm text-gray-500"),
                rx.el.div(
                    rx.foreach(AdminState.past_sessions, attendance_card),
                    class_name="grid grid-cols-1 md:grid-cols-2 gap-4",
                ),
            ),
            class_name="space-y-4",
        ),
        class_name="space-y-8",
    )


def settings_management() -> rx.Component:
    return rx.el.div(
        rx.el.h2("Settings", class_name="text-2xl font-bold text-gray-900"),
        rx.el.div(
            rx.el.div(
                rx.el.h3("User Data", class_name="text-lg font-semibold text-gray-800"),
                rx.el.p(
                    "Permanently delete all users except for the primary admin account.",
                    class_name="text-sm text-gray-600",
                ),
                class_name="space-y-1",
            ),
            rx.el.button(
                "Clear All Users",
                on_click=AdminState.clear_all_users,
                class_name="rounded-lg bg-red-600 px-4 py-2 text-sm font-semibold text-white hover:bg-red-700",
            ),
            class_name="flex items-center justify-between rounded-lg border border-gray-200 bg-white p-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Attendance Data", class_name="text-lg font-semibold text-gray-800"
                ),
                rx.el.p(
                    "Permanently delete all attendance session records.",
                    class_name="text-sm text-gray-600",
                ),
                class_name="space-y-1",
            ),
            rx.el.button(
                "Clear All Attendance Data",
                on_click=AdminState.clear_all_attendance_data,
                class_name="rounded-lg bg-red-600 px-4 py-2 text-sm font-semibold text-white hover:bg-red-700",
            ),
            class_name="flex items-center justify-between rounded-lg border border-gray-200 bg-white p-6",
        ),
        class_name="space-y-6",
    )


def admin_dashboard_page() -> rx.Component:
    return rx.el.div(
        admin_sidebar(),
        rx.el.main(
            rx.el.div(
                rx.match(
                    AdminState.current_view,
                    ("Users", users_management()),
                    ("Attendance", attendance_management()),
                    ("Settings", settings_management()),
                    rx.el.div("Select a view"),
                ),
                class_name="p-8",
            ),
            class_name="flex-1 bg-gray-50",
        ),
        class_name="flex min-h-screen w-screen bg-white font-['Lora']",
    )
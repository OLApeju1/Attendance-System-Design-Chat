import reflex as rx
from app.states.auth_state import AuthState
from app.states.attendance_state import AttendanceState
from app.pages.login import login_page
from app.pages.signup import signup_page
from app.pages.admin_dashboard import admin_dashboard_page
from app.pages.attendance import attendance_page


def index() -> rx.Component:
    return rx.el.div(
        rx.cond(
            AuthState.is_logged_in,
            rx.cond(
                AuthState.is_admin,
                rx.el.div(
                    rx.el.p("Redirecting to admin dashboard..."),
                    on_mount=rx.redirect("/admin/dashboard"),
                ),
                authenticated_content(),
            ),
            rx.el.div(
                rx.el.p("Redirecting to login..."), on_mount=rx.redirect("/login")
            ),
        )
    )


def authenticated_content() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.a(
                        rx.icon("user-check", class_name="h-6 w-6 text-blue-600"),
                        href="/",
                    ),
                    rx.el.h1(
                        "Attendance App",
                        class_name="text-lg font-semibold text-gray-800",
                    ),
                    class_name="flex items-center gap-3",
                ),
                rx.el.div(
                    rx.el.p(
                        AuthState.logged_in_user["full_name"],
                        class_name="font-semibold",
                    ),
                    rx.el.image(
                        src=rx.get_upload_url(
                            AuthState.logged_in_user["photo_filename"]
                        ),
                        class_name="h-8 w-8 rounded-full object-cover",
                    ),
                    rx.el.button(
                        rx.icon("log-out", class_name="h-4 w-4"),
                        "Logout",
                        on_click=AuthState.logout,
                        class_name="flex items-center gap-2 rounded-md bg-gray-100 px-3 py-1.5 text-sm font-medium text-gray-700 hover:bg-gray-200",
                    ),
                    class_name="flex items-center gap-4",
                ),
                class_name="flex h-16 items-center justify-between border-b bg-white px-6",
            ),
            rx.el.div(
                rx.el.h2("Dashboard", class_name="text-2xl font-bold text-gray-900"),
                rx.el.p(
                    "Welcome to your attendance dashboard.", class_name="text-gray-600"
                ),
                rx.el.a(
                    rx.icon("camera", class_name="h-4 w-4 mr-2"),
                    "Mark Attendance",
                    href="/attendance",
                    class_name="mt-4 inline-flex items-center rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-700",
                ),
                class_name="space-y-4 p-8",
            ),
            class_name="h-screen w-screen bg-gray-50 font-['Lora']",
        )
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Lora:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index)
app.add_page(login_page, route="/login", on_load=AuthState.reset_auth_forms)
app.add_page(signup_page, route="/signup")
app.add_page(admin_dashboard_page, route="/admin/dashboard")
app.add_page(
    attendance_page,
    route="/attendance",
    on_load=AttendanceState.on_attendance_page_load,
)
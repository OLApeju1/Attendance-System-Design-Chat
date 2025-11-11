import reflex as rx
from app.states.auth_state import AuthState
from app.states.admin_state import AdminState


def nav_item(icon: str, text: str, view: str) -> rx.Component:
    is_active = AdminState.current_view == view
    return rx.el.button(
        rx.icon(icon, class_name="h-5 w-5"),
        rx.el.span(text, class_name="font-medium"),
        on_click=lambda: AdminState.set_current_view(view),
        class_name=rx.cond(
            is_active,
            "flex items-center gap-3 rounded-lg bg-blue-100 px-3 py-2 text-blue-600",
            "flex items-center gap-3 rounded-lg px-3 py-2 text-gray-600 hover:bg-gray-100 hover:text-gray-900",
        ),
        width="100%",
    )


def admin_sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.el.a(
                    rx.icon("user-check", class_name="h-8 w-8 text-blue-600"), href="/"
                ),
                rx.el.h1("Admin Panel", class_name="text-xl font-bold text-gray-900"),
                class_name="flex items-center gap-3 px-6 h-16 border-b",
            ),
            rx.el.nav(
                nav_item("users", "Users", "Users"),
                nav_item("calendar-check", "Attendance", "Attendance"),
                nav_item("settings", "Settings", "Settings"),
                class_name="flex flex-col gap-1 p-4",
            ),
            class_name="flex-1 overflow-y-auto",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.image(
                    src=rx.get_upload_url(AuthState.logged_in_user["photo_filename"]),
                    class_name="h-10 w-10 rounded-full object-cover",
                ),
                rx.el.div(
                    rx.el.p(
                        AuthState.logged_in_user["full_name"],
                        class_name="font-semibold",
                    ),
                    rx.el.p("Admin", class_name="text-xs text-gray-500"),
                    class_name="flex flex-col",
                ),
                rx.el.button(
                    rx.icon("log-out", class_name="h-4 w-4"),
                    on_click=AuthState.logout,
                    class_name="ml-auto rounded-md p-2 hover:bg-gray-100",
                ),
                class_name="flex items-center gap-3 p-4 border-t",
            )
        ),
        class_name="flex h-screen w-64 flex-col border-r bg-white",
    )
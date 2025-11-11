import reflex as rx
from app.states.auth_state import AuthState
from app.components.auth_layout import auth_layout


def login_page() -> rx.Component:
    return rx.el.main(
        auth_layout(
            "Welcome Back",
            rx.el.form(
                rx.el.div(
                    rx.cond(
                        AuthState.error_message,
                        rx.el.div(
                            rx.icon("badge_alert", class_name="h-4 w-4"),
                            rx.el.p(AuthState.error_message, class_name="text-sm"),
                            class_name="flex items-center gap-2 rounded-lg bg-red-50 p-3 text-red-600",
                        ),
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Email", class_name="text-sm font-medium text-gray-700"
                        ),
                        rx.el.input(
                            type="email",
                            name="email",
                            placeholder="m@example.com",
                            required=True,
                            class_name="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500",
                        ),
                        class_name="space-y-2",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Password", class_name="text-sm font-medium text-gray-700"
                        ),
                        rx.el.input(
                            type="password",
                            name="password",
                            required=True,
                            class_name="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500",
                        ),
                        class_name="space-y-2",
                    ),
                    rx.el.button(
                        "Sign In",
                        type="submit",
                        class_name="w-full rounded-lg bg-blue-600 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2",
                    ),
                    class_name="flex flex-col gap-4",
                ),
                on_submit=AuthState.handle_login,
                reset_on_submit=False,
            ),
            rx.el.p(
                "Don't have an account? ",
                rx.el.a(
                    "Sign up",
                    href="/signup",
                    class_name="font-semibold text-blue-600 hover:underline",
                ),
                class_name="text-center text-sm text-gray-600",
            ),
        ),
        class_name="flex min-h-screen items-center justify-center bg-gray-50 font-['Lora']",
    )
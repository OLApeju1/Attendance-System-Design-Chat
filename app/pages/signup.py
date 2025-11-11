import reflex as rx
from app.states.auth_state import AuthState
from app.components.auth_layout import auth_layout


def webcam_component() -> rx.Component:
    return rx.el.div(
        rx.el.script(src="/webcam.js"),
        rx.el.video(id="webcam", auto_play=True, class_name="w-full rounded-lg"),
        rx.el.button(
            rx.icon("camera", class_name="h-4 w-4 mr-2"),
            "Capture Photo",
            on_click=rx.call_script("captureImage", callback=AuthState.capture_img),
            class_name="flex items-center justify-center w-full rounded-lg bg-gray-600 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2",
        ),
        class_name="space-y-4",
    )


def signup_page() -> rx.Component:
    return rx.el.main(
        auth_layout(
            "Create an Account",
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
                            "Full Name", class_name="text-sm font-medium text-gray-700"
                        ),
                        rx.el.input(
                            name="full_name",
                            placeholder="John Doe",
                            required=True,
                            class_name="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500",
                        ),
                        class_name="space-y-2",
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
                    rx.el.div(
                        rx.el.label(
                            "Your Photo", class_name="text-sm font-medium text-gray-700"
                        ),
                        rx.cond(
                            AuthState.img,
                            rx.el.div(
                                rx.el.image(
                                    src=AuthState.img,
                                    class_name="h-32 w-32 rounded-full object-cover mx-auto",
                                ),
                                rx.el.button(
                                    "Retake Photo",
                                    on_click=AuthState.toggle_webcam,
                                    type="button",
                                    class_name="text-sm text-blue-600 hover:underline",
                                ),
                                class_name="flex flex-col items-center gap-2",
                            ),
                            rx.cond(
                                AuthState.show_webcam,
                                webcam_component(),
                                rx.el.button(
                                    "Open Camera",
                                    on_click=AuthState.toggle_webcam,
                                    type="button",
                                    class_name="w-full rounded-lg border-2 border-dashed border-gray-300 py-4 text-sm font-medium text-gray-700 hover:bg-gray-50",
                                ),
                            ),
                        ),
                        class_name="space-y-2",
                    ),
                    rx.el.button(
                        "Create Account",
                        type="submit",
                        class_name="w-full rounded-lg bg-blue-600 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2",
                    ),
                    class_name="flex flex-col gap-4",
                ),
                on_submit=AuthState.handle_signup,
                reset_on_submit=False,
            ),
            rx.el.p(
                "Already have an account? ",
                rx.el.a(
                    "Sign in",
                    href="/login",
                    class_name="font-semibold text-blue-600 hover:underline",
                ),
                class_name="text-center text-sm text-gray-600",
            ),
        ),
        class_name="flex min-h-screen items-center justify-center bg-gray-50 font-['Lora'] py-12",
        on_mount=AuthState.reset_auth_forms,
    )
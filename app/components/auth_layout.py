import reflex as rx


def auth_layout(title: str, *children) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.a(
                    rx.icon("user-check", class_name="h-8 w-8 text-blue-600"),
                    href="/",
                    class_name="flex items-center justify-center rounded-lg bg-gray-100 p-2",
                ),
                rx.el.h1(title, class_name="text-3xl font-bold text-gray-900"),
                class_name="space-y-4 text-center",
            ),
            *children,
            class_name="flex flex-col gap-8",
        ),
        class_name="mx-auto w-full max-w-md rounded-2xl border border-gray-200 bg-white p-8 shadow-sm",
    )
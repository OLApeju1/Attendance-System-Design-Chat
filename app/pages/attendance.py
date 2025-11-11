import reflex as rx
from app.states.auth_state import AuthState
from app.states.attendance_state import AttendanceState


def webcam_component() -> rx.Component:
    return rx.el.div(
        rx.el.script(src="/webcam.js"),
        rx.el.video(id="webcam", auto_play=True, class_name="w-full rounded-lg"),
        rx.el.button(
            rx.icon("camera", class_name="h-4 w-4 mr-2"),
            "Capture Photo",
            on_click=rx.call_script(
                "captureImage", callback=AttendanceState.capture_img
            ),
            class_name="flex items-center justify-center w-full rounded-lg bg-gray-600 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-gray-700",
        ),
        class_name="space-y-4",
    )


def attendance_page() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            rx.el.div(
                rx.el.a(href="/", class_name="text-sm text-blue-600 hover:underline"),
                rx.el.h1(
                    "Mark Attendance", class_name="text-3xl font-bold text-gray-900"
                ),
                class_name="space-y-2",
            ),
            rx.cond(
                AttendanceState.active_session,
                rx.el.div(
                    rx.cond(
                        AttendanceState.has_marked_attendance,
                        rx.el.div(
                            rx.icon(
                                "square_check", class_name="h-6 w-6 text-green-600"
                            ),
                            rx.el.p(
                                "You have already marked your attendance for this session.",
                                class_name="font-medium text-green-700",
                            ),
                            class_name="flex items-center gap-3 rounded-lg bg-green-50 p-4",
                        ),
                        rx.el.div(
                            rx.el.p(
                                "An attendance session is active. Please capture your photo for liveness verification."
                            ),
                            rx.cond(
                                AttendanceState.attendance_message,
                                rx.el.p(AttendanceState.attendance_message),
                            ),
                            rx.cond(
                                AttendanceState.img,
                                rx.el.div(
                                    rx.el.image(
                                        src=AttendanceState.img,
                                        class_name="h-32 w-32 rounded-full object-cover mx-auto",
                                    ),
                                    rx.el.button(
                                        "Retake Photo",
                                        on_click=AttendanceState.toggle_webcam,
                                        type="button",
                                        class_name="text-sm text-blue-600 hover:underline",
                                    ),
                                    class_name="flex flex-col items-center gap-2",
                                ),
                                rx.cond(
                                    AttendanceState.show_webcam,
                                    webcam_component(),
                                    rx.el.button(
                                        "Open Camera",
                                        on_click=AttendanceState.toggle_webcam,
                                        type="button",
                                        class_name="w-full rounded-lg border-2 border-dashed border-gray-300 py-4 text-sm font-medium text-gray-700 hover:bg-gray-50",
                                    ),
                                ),
                            ),
                            rx.el.button(
                                rx.cond(
                                    AttendanceState.processing,
                                    rx.spinner(),
                                    "Mark My Attendance",
                                ),
                                on_click=AttendanceState.mark_attendance,
                                disabled=AttendanceState.processing
                                | (AttendanceState.img == ""),
                                class_name="w-full rounded-lg bg-blue-600 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-blue-700 disabled:opacity-50",
                            ),
                            class_name="space-y-4",
                        ),
                    ),
                    class_name="space-y-4",
                ),
                rx.el.div(
                    rx.icon("info", class_name="h-6 w-6 text-blue-600"),
                    rx.el.p(
                        "There are no active attendance sessions at the moment.",
                        class_name="font-medium text-blue-700",
                    ),
                    class_name="flex items-center gap-3 rounded-lg bg-blue-50 p-4",
                ),
            ),
            rx.el.a(
                "< Back to Dashboard",
                href="/",
                class_name="mt-6 inline-block text-sm font-medium text-gray-600 hover:text-gray-900",
            ),
            class_name="mx-auto w-full max-w-lg rounded-2xl border border-gray-200 bg-white p-8 shadow-sm",
        ),
        class_name="flex min-h-screen items-center justify-center bg-gray-50 font-['Lora'] py-12",
    )
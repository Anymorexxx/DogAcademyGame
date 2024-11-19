def clear_frame(frame):
    """Удаление всех виджетов из фрейма."""
    for widget in frame.winfo_children():
        widget.destroy()

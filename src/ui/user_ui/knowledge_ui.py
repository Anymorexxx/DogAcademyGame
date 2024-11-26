import tkinter as tk
from src.utils import clear_frame
from database.db_events import get_knowledge_base


def knowledge_ui(root):
    """Интерфейс базы знаний."""
    clear_frame(root)

    frame = tk.Frame(root, bg="#f8e1e1")
    frame.pack(fill=tk.BOTH, expand=True)

    tk.Label(frame, text="База знаний", font=("Comic Sans MS", 30), bg="#f8e1e1").pack(pady=20)

    articles = get_knowledge_base()
    for article in articles:
        article_frame = tk.Frame(frame, bg="#f8f8f8", bd=2, relief=tk.RIDGE)
        article_frame.pack(pady=5, padx=10, fill=tk.X)

        tk.Label(article_frame, text=article.breed, font=("Comic Sans MS", 20), bg="#f8f8f8").pack(side=tk.LEFT,
                                                                                                   padx=10)
        tk.Button(article_frame, text="Читать", command=lambda a=article: show_article(a)).pack(side=tk.RIGHT, padx=10)

    tk.Button(frame, text="Назад", command=lambda: clear_frame(root), font=("Comic Sans MS", 20)).pack(pady=20)


def show_article(article):
    """Показать содержимое статьи."""
    top = tk.Toplevel()
    top.title(article.breed)
    text = tk.Text(top, wrap=tk.WORD)
    text.pack(fill=tk.BOTH, expand=True)
    text.insert(tk.END, article.content)
    text.config(state=tk.DISABLED)

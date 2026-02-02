import os
import threading
import tkinter as tk
from dataclasses import dataclass
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from yt_dlp import YoutubeDL


@dataclass
class DownloadTask:
    url: str
    status: str = "En attente"
    progress: float = 0.0
    title: str = ""


class DownloadApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Video Downloader - IDM Style")
        self.geometry("820x520")
        self.resizable(False, False)

        self.url_var = tk.StringVar()
        self.output_var = tk.StringVar(value=str(Path.cwd() / "downloads"))
        self.template_var = tk.StringVar(value="%(title)s.%(ext)s")
        self.status_var = tk.StringVar(value="Prêt")
        self.format_var = tk.StringVar(value="best")
        self.limit_var = tk.StringVar(value="")
        self.playlist_var = tk.BooleanVar(value=False)

        self.tasks: list[DownloadTask] = []
        self._worker_thread: threading.Thread | None = None
        self._stop_flag = threading.Event()

        self._build_ui()

    def _build_ui(self) -> None:
        padding = {"padx": 10, "pady": 6}

        header = ttk.Label(self, text="Téléchargeur vidéo (style IDM)", font=("Arial", 16, "bold"))
        header.pack(pady=12)

        form = ttk.Frame(self)
        form.pack(fill="x", padx=12)

        ttk.Label(form, text="URL de la vidéo").grid(row=0, column=0, sticky="w", **padding)
        ttk.Entry(form, textvariable=self.url_var, width=70).grid(
            row=0, column=1, columnspan=3, sticky="w", **padding
        )
        ttk.Button(form, text="Ajouter", command=self._add_to_queue).grid(
            row=0, column=4, sticky="w", **padding
        )

        ttk.Label(form, text="Dossier de sortie").grid(row=1, column=0, sticky="w", **padding)
        ttk.Entry(form, textvariable=self.output_var, width=50).grid(
            row=1, column=1, sticky="w", **padding
        )
        ttk.Button(form, text="Parcourir", command=self._choose_folder).grid(
            row=1, column=2, sticky="w", **padding
        )
        ttk.Button(form, text="Ouvrir", command=self._open_folder).grid(
            row=1, column=3, sticky="w", **padding
        )

        ttk.Label(form, text="Nom du fichier").grid(row=2, column=0, sticky="w", **padding)
        ttk.Entry(form, textvariable=self.template_var, width=50).grid(
            row=2, column=1, sticky="w", **padding
        )
        ttk.Label(form, text="Ex: %(title)s.%(ext)s").grid(
            row=2, column=2, columnspan=2, sticky="w", **padding
        )

        options = ttk.LabelFrame(self, text="Options")
        options.pack(fill="x", padx=12, pady=6)

        ttk.Label(options, text="Qualité / format").grid(row=0, column=0, sticky="w", **padding)
        ttk.Combobox(
            options,
            textvariable=self.format_var,
            values=["best", "bestvideo+bestaudio", "worst"],
            width=28,
            state="readonly",
        ).grid(row=0, column=1, sticky="w", **padding)

        ttk.Label(options, text="Limite vitesse (ex: 1M)").grid(row=0, column=2, sticky="w", **padding)
        ttk.Entry(options, textvariable=self.limit_var, width=16).grid(
            row=0, column=3, sticky="w", **padding
        )

        ttk.Checkbutton(options, text="Autoriser playlists", variable=self.playlist_var).grid(
            row=0, column=4, sticky="w", **padding
        )

        table_frame = ttk.Frame(self)
        table_frame.pack(fill="both", padx=12, pady=6)

        columns = ("url", "status", "progress")
        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=8,
        )
        self.table.heading("url", text="URL")
        self.table.heading("status", text="Statut")
        self.table.heading("progress", text="Progression")
        self.table.column("url", width=480)
        self.table.column("status", width=120)
        self.table.column("progress", width=120)
        self.table.pack(side="left", fill="both")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        controls = ttk.Frame(self)
        controls.pack(fill="x", padx=12, pady=6)
        ttk.Button(controls, text="Démarrer", command=self._start_queue).pack(side="left")
        ttk.Button(controls, text="Stop", command=self._stop_queue).pack(side="left", padx=6)
        ttk.Button(controls, text="Supprimer", command=self._remove_selected).pack(
            side="left", padx=6
        )
        ttk.Button(controls, text="Tout effacer", command=self._clear_queue).pack(
            side="left", padx=6
        )

        status_frame = ttk.Frame(self)
        status_frame.pack(fill="x", padx=12, pady=6)
        ttk.Label(status_frame, textvariable=self.status_var).pack(anchor="w")

    def _choose_folder(self) -> None:
        folder = filedialog.askdirectory()
        if folder:
            self.output_var.set(folder)

    def _open_folder(self) -> None:
        folder = self.output_var.get().strip()
        if not folder:
            return
        path = Path(folder)
        if not path.exists():
            messagebox.showwarning("Dossier", "Le dossier n'existe pas encore.")
            return
        try:
            if os.name == "nt":
                os.startfile(path)  # type: ignore[attr-defined]
            elif os.name == "posix":
                os.system(f"xdg-open '{path}'")
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Erreur", f"Impossible d'ouvrir le dossier: {exc}")

    def _add_to_queue(self) -> None:
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("URL manquante", "Veuillez fournir une URL de vidéo.")
            return
        task = DownloadTask(url=url)
        self.tasks.append(task)
        self.table.insert("", "end", values=(task.url, task.status, "0%"))
        self.url_var.set("")

    def _remove_selected(self) -> None:
        selected = self.table.selection()
        if not selected:
            return
        for item in selected:
            index = self.table.index(item)
            self.table.delete(item)
            if index < len(self.tasks):
                self.tasks.pop(index)

    def _clear_queue(self) -> None:
        self.table.delete(*self.table.get_children())
        self.tasks.clear()
        self.status_var.set("Prêt")

    def _start_queue(self) -> None:
        if self._worker_thread and self._worker_thread.is_alive():
            messagebox.showinfo("Téléchargements", "Un téléchargement est déjà en cours.")
            return
        if not self.tasks:
            messagebox.showwarning("File vide", "Ajoutez au moins une URL à la file.")
            return
        self._stop_flag.clear()
        self._worker_thread = threading.Thread(target=self._process_queue, daemon=True)
        self._worker_thread.start()

    def _stop_queue(self) -> None:
        self._stop_flag.set()
        self.status_var.set("Arrêt demandé...")

    def _process_queue(self) -> None:
        self.status_var.set("Téléchargement en cours...")
        for index, task in enumerate(list(self.tasks)):
            if self._stop_flag.is_set():
                self._update_table(index, "Arrêté", task.progress)
                break
            self._update_table(index, "En cours", task.progress)
            self._download_task(task, index)
        if not self._stop_flag.is_set():
            self.status_var.set("Téléchargements terminés")
        else:
            self.status_var.set("Téléchargement interrompu")

    def _update_table(self, index: int, status: str, progress: float) -> None:
        if index >= len(self.table.get_children()):
            return
        item_id = self.table.get_children()[index]
        self.table.item(item_id, values=(self.tasks[index].url, status, f"{progress:.0f}%"))

    def _download_task(self, task: DownloadTask, index: int) -> None:
        output_dir = self.output_var.get().strip()
        template = self.template_var.get().strip()
        format_value = self.format_var.get().strip()
        limit_value = self.limit_var.get().strip()
        playlist = self.playlist_var.get()

        def hook(data: dict) -> None:
            if data.get("status") == "downloading":
                total = data.get("total_bytes") or data.get("total_bytes_estimate")
                downloaded = data.get("downloaded_bytes", 0)
                percent = (downloaded / total * 100) if total else 0
                task.progress = percent
                self.after(0, self._update_table, index, "En cours", percent)
            elif data.get("status") == "finished":
                task.progress = 100
                self.after(0, self._update_table, index, "Terminé", 100)

        ydl_opts = {
            "outtmpl": f"{output_dir}/{template}",
            "progress_hooks": [hook],
            "noplaylist": not playlist,
            "format": format_value,
        }
        if limit_value:
            ydl_opts["ratelimit"] = self._parse_rate_limit(limit_value)

        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([task.url])
        except Exception as exc:  # noqa: BLE001
            task.status = "Erreur"
            self.after(0, self._update_table, index, f"Erreur", task.progress)
            self.after(0, self.status_var.set, f"Erreur: {exc}")

    @staticmethod
    def _parse_rate_limit(value: str) -> int:
        value = value.strip().lower()
        if value.endswith("k"):
            return int(float(value[:-1]) * 1024)
        if value.endswith("m"):
            return int(float(value[:-1]) * 1024 * 1024)
        return int(float(value))


if __name__ == "__main__":
    app = DownloadApp()
    app.mainloop()

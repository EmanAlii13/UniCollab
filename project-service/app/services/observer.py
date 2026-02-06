class Observer:
    def notify(self, message):
        print(f"[Observer] {message}")


observer = Observer()

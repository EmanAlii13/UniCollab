class Observer:
    def notify(self, message):
        raise NotImplementedError

class ConsoleObserver(Observer):
    def notify(self, message):
        print(f"[Observer] {message}")

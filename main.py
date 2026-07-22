import threading
import GUI
import test5

if __name__ == "__main__":
    bot_thread = threading.Thread(target=test5.main, daemon=True)
    bot_thread.start()
    GUI.main()

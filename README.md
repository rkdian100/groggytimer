# GroggyTimer

An interactive, terminal-based productivity timer designed to help you focus, manage sessions, and track progress over time.

## Features

* **Focus Sessions & Pomodoro**: Choose between continuous focus or the classic 25/5 Pomodoro cycle.
* **Leaderboard & Analytics**: Persist session history, view total time focused, and track personal bests.
* **Rich Terminal UI**: Utilizes Rich for progress bars, live timers, and keyboard shortcuts.
* **Motivational Quotes**: A random quote after every session to keep you inspired.
* **Achievements & Sharing Stubs**: Milestone detection (e.g., longest streak) with placeholders for social media integration.
* **Lightweight Persistence**: Default JSON storage with optional SQLite support.

## Requirements

* Python 3.7 or higher
* [Rich](https://pypi.org/project/rich/)
* [Pygame](https://pypi.org/project/pygame/)
* [keyboard](https://pypi.org/project/keyboard/)

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/rkdian100/groggytimer.git
   cd groggytimer
   ```

2. **Create and activate a virtual environment**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate    # On Windows: .\.venv\Scripts\activate
   ```

3. **Install dependencies**

   Since this project doesn’t include a `requirements.txt`, install the core packages directly:

   ```bash
   pip install --upgrade pip
   pip install rich pygame keyboard
   ```

   *Optional:* After installing, you can generate your own `requirements.txt`:

   ```bash
   pip freeze > requirements.txt
   ```

## Usage

Run the main application from the project root:

```bash
python main_app.py
```

Follow the on-screen menu to start a focus session, Pomodoro cycle, view analytics, or manage settings.

## Configuration

* By default, session data is stored in `sessions.json` in the project root. To switch to SQLite:

  1. Install `sqlite3` (if not already available).
  2. Update the `persistence.py` backend selection.

* Customize quotes by editing `quotes.py`.

## Development

* **Project Structure**:

  * `main_app.py`: Entry point and menu dispatcher
  * `sessions.py`: Core focus/Pomodoro session logic
  * `persistence.py`: Data load/save layer (JSON/SQLite)
  * `display_utils.py`: Rich UI wrappers and sound hooks
  * `achievements_sharing.py`: Achievement checks & sharing stubs
  * `utils.py`: Helper functions
  * `test_module.py` / `test_script.py`: Unit and end-to-end tests

* **Run tests**:

  ```bash
  pytest test_module.py
  ```

## Contributing

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/YourFeature`
3. Commit your changes: `git commit -m "Add YourFeature description"`
4. Push to branch: `git push origin feature/YourFeature`
5. Open a pull request describing your changes.

Please adhere to PEP8 style and include tests for new functionality.

## License

This project is licensed under the [MIT License](LICENSE).

## Author

Developed and maintained by RKD (Raj Kamal Das).

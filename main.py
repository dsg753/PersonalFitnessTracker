import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLabel, QPushButton,
    QLineEdit, QInputDialog, QWidget, QMessageBox
)

# Global variables to store fitness data
workouts = []  # To store workout types and durations
calories = []  # To store calorie intake for meals
workout_goal = 0  # Daily workout goal in minutes
calorie_goal = 0  # Daily calorie intake goal
last_workout_type = None  # To remember the last workout type
last_calories_consumed = None  # To remember the last calorie intake


class FitnessTracker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Personal Fitness Tracker 🏋️‍♂️")
        self.setGeometry(200, 200, 400, 300)

        # Main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Add widgets
        self.status_label = QLabel("Welcome to the Personal Fitness Tracker System! 🏋️‍♂️")
        self.layout.addWidget(self.status_label)

        self.log_workout_button = QPushButton("Log Workout")
        self.log_workout_button.clicked.connect(self.log_workout)
        self.layout.addWidget(self.log_workout_button)

        self.log_calories_button = QPushButton("Log Calorie Intake")
        self.log_calories_button.clicked.connect(self.log_calories)
        self.layout.addWidget(self.log_calories_button)

        self.view_progress_button = QPushButton("View Progress")
        self.view_progress_button.clicked.connect(self.view_progress)
        self.layout.addWidget(self.view_progress_button)

        self.view_history_button = QPushButton("View History")
        self.view_history_button.clicked.connect(self.view_history)
        self.layout.addWidget(self.view_history_button)

        self.reset_progress_button = QPushButton("Reset Progress")
        self.reset_progress_button.clicked.connect(self.reset_progress)
        self.layout.addWidget(self.reset_progress_button)

        self.set_goals_button = QPushButton("Set Daily Goals")
        self.set_goals_button.clicked.connect(self.set_daily_goals)
        self.layout.addWidget(self.set_goals_button)

        self.exit_button = QPushButton("Exit")
        self.exit_button.clicked.connect(self.close)
        self.layout.addWidget(self.exit_button)

    def log_workout(self):
        global last_workout_type

        # Suggest last workout type
        workout_type, ok1 = QInputDialog.getText(
            self, "Log Workout",
            f"Enter workout type (e.g., Running):",
            text=last_workout_type or ""
        )
        if not ok1 or not workout_type.strip():
            return

        duration, ok2 = QInputDialog.getInt(self, "Log Workout", "Enter duration (in minutes):", min=1, max=300)
        if not ok2:
            return

        workouts.append((workout_type, duration))
        last_workout_type = workout_type  # Update last workout type

        QMessageBox.information(self, "Success", f"Logged: {workout_type} for {duration} minutes!")
        self.update_status("Workout logged successfully!")

    def log_calories(self):
        global last_calories_consumed

        # Suggest last calorie value
        calories_consumed, ok = QInputDialog.getInt(
            self, "Log Calorie Intake",
            "Enter calories consumed:",
            value=last_calories_consumed or 0,
            min=0, max=5000
        )
        if not ok:
            return

        calories.append(calories_consumed)
        last_calories_consumed = calories_consumed  # Update last calorie value

        QMessageBox.information(self, "Success", f"Logged: {calories_consumed} calories!")
        self.update_status("Calorie intake logged successfully!")

    def view_progress(self):
        total_workout = sum(duration for _, duration in workouts)
        total_calories = sum(calories)
        workout_feedback = "Goal Achieved! 🎉" if total_workout >= workout_goal else "Keep going! 💪"
        calorie_feedback = "On track! 👍" if total_calories <= calorie_goal else "Watch your intake! ⚠️"

        progress_message = (
            f"Workout Progress: {total_workout} / {workout_goal} minutes ({workout_feedback})\n"
            f"Calorie Progress: {total_calories} / {calorie_goal} calories ({calorie_feedback})"
        )
        QMessageBox.information(self, "Progress", progress_message)
        self.update_status("Progress displayed!")

    def view_history(self):
        if not workouts and not calories:
            QMessageBox.information(self, "History", "No history to display yet.")
            return

        history_message = "Workout History:\n" + "\n".join(f"{w[0]}: {w[1]} min" for w in workouts)
        history_message += "\n\nCalorie History:\n" + "\n".join(f"{c} calories" for c in calories)

        QMessageBox.information(self, "History", history_message)

    def reset_progress(self):
        global workouts, calories, last_workout_type, last_calories_consumed
        workouts = []
        calories = []
        last_workout_type = None
        last_calories_consumed = None

        QMessageBox.information(self, "Reset", "All progress has been reset!")
        self.update_status("Progress reset successfully!")

    def set_daily_goals(self):
        global workout_goal, calorie_goal

        workout_minutes, ok1 = QInputDialog.getInt(self, "Set Daily Goals", "Enter daily workout goal (in minutes):", min=0, max=300)
        if not ok1:
            return

        calorie_limit, ok2 = QInputDialog.getInt(self, "Set Daily Goals", "Enter daily calorie intake goal:", min=0, max=5000)
        if not ok2:
            return

        workout_goal = workout_minutes
        calorie_goal = calorie_limit
        QMessageBox.information(self, "Success", f"Goals set!\nWorkout: {workout_goal} minutes\nCalories: {calorie_goal}")
        self.update_status("Daily goals set successfully!")

    def update_status(self, message):
        self.status_label.setText(message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    tracker = FitnessTracker()
    tracker.show()
    sys.exit(app.exec_())

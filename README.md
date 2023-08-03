# Daily-Study-Tracker
Track how long your daily study activities are
<br>
It comes with a Python GUI to ease your daily tracking

## Features 
- **Start Clock**: Start the stopwatch by simply clicking a button when your study begins.
- **Pause and Continue**: When you are taking a break, these buttons are available for you to pause and continue the time once you are ready.
- **Update**: Once you finish your study, you can update and store how long you've studied into a Pixela graph.
- **See Journey**: Takes you to your Pixela graph to see your study history.
- **Make a Pixela User**: For users who are unfamiliar with Pixela, you can create a new Pixela user directly through the GUI from the program.
- **Add Existing Pixela User**: People who already have a daily study graph can add their credentials to access the graph.

## Note
- If you want to skip the process of making the `data.txt` provided, you can create a `data.txt` file yourself in the same directory as the code files and input today's date in the format of YYYYMMDD on the first line and 0 on the second line.
- If you want to skip the process of making the `user.txt` provided because you already have a Pixela user, you can create a `user.txt` file yourself in the same directory as the code files and input your Pixela username on the first line, your token on the second line, and your graph ID on the third line. This way, the program won't ask whether you already have an account or not.
- A number of Pixela graph colors can be selected in the `req_graph` function inside `graph.py`.
- GUI background and image can be modified in the `BACKGROUND` constant and `__init__` inside `tracker.py`.

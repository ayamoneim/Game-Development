import cx_Freeze

executables = [cx_Freeze.Executable("Main.py")]

# Setup by cx_freeze

cx_Freeze.setup(
    name="SNAKE ONE LAST TIME !",
    options={"build_exe": {"packages": ["pygame"], "include_files": ["Bg.jpg", "apple.png", "start.jpg", "part.png",
                                                                     "head.png", "end_menu.jpg", "dying_snake.png",
                                                                     "2.wav", "1.wav", "3.wav", "tick.mp3",
                                                                     "game_over.wav"]}},
    description="Basic SNAKE Game!!",
    executables=executables

)

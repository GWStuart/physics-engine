# Physics Engine
A simple physics engine using verlet integration.

Thanks to Coding Math [link here](https://www.youtube.com/@codingmath) for original inspiration. and introduction to the topic.

# Current features
- Sandbox: a place where you can test the engine in real time

## Sandbox
Here you can test out the engine in real time. 
You can load some of the demos into the sandbox by pressing `o` and selecting one of the files from the demos folder
There are a few different modes which you can get to with the number keys

**mode 1**: normal
![mode 1](https://github.com/user-attachments/assets/31e777a5-9df6-4e89-8db0-e9536af69166)

- click to add balls
- click and drag to add them with an initial velocity (shown with a red line)
- use the scroll wheel while the mouse is down to change the size
- create a "stick" by clicking one a point and drag and release on another point

**mode 2**: drag
![mode 2](https://github.com/user-attachments/assets/77b41f50-bf4e-4825-ad99-e536a5904c6e)

Allows the user to drag the balls with their mouse
- hover your mouse over a ball and click and drag to move
- move the mouse fast to release balls with acceleration

**mode 3**: mouse field
![mode 3](https://github.com/user-attachments/assets/739bba56-75d0-41d4-a5bc-34cf81ce3fda)

Creates a force-field type area around your mouse
- change the field size with the scroll wheel
- toggle whether the field should be rendered or not with `f`

**mode 4 & 5**: cloth simulation and cutting
![mode 4 5](https://github.com/user-attachments/assets/30cd3d30-3975-4732-88ae-89f0081f884c)


Mode 4 allows you to use the simualtion to create a "cloth" and then using mode 5 you can cut this cloth.

**mode 6**: line
Current work in progress that allows users to draw lines that restrict the movement of the balls. It is already partially implemented but needs some work.

**Other general keybinds**
- `SPACE` toggles the physics
- `s` save the current sandbox 
- `o` open a saved Sandbox

**Using the Demos**
You can load the demos found in the demos folder by pressing `s` in the sandbox.
Once a demo is loaded you may want to mess around with it by testing out the different modes and interacting with the objects.
Note that the program will also dynamically adjust to different window sizes which can be an interesting mechanic to mess with.

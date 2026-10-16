from manim import *
import numpy as np
import random

class MovingSineWavePiLabels(Scene):
    def construct(self):
        
        random_circle = Circle(radius=0.5, color=BLUE)
        self.play(Create(random_circle))
        self.wait(2)
        
        positions = [
            ORIGIN,
            UP * 2 + LEFT * 2,
            DOWN * 1.5 + RIGHT * 3,
            UP * 1 + RIGHT * 2,
            ORIGIN
        ]
        
        for next_pos in positions[1:]:
            self.play(random_circle.animate.move_to(next_pos), run_time=1.5)
            self.wait(2) 
        self.wait(2)
        self.play(FadeOut(random_circle))

        x_dict = {
            0: Text("0", font_size=20),
            np.pi: Text("π", font_size=20),
            2 * np.pi: Text("2π", font_size=20),
            3 * np.pi: Text("3π", font_size=20),
            4 * np.pi: Text("4π", font_size=20)
        }

        axes = Axes(
            x_range=[-0.5, 4.5 * np.pi, np.pi],
            y_range=[-1.5, 1.5, 1],
            x_length=9,
            y_length=4,
            axis_config={"include_numbers": False} 
        )
        axes.x_axis.add_labels(x_dict)
        
        labels = axes.get_axis_labels(x_label="x", y_label="y")
        axes_group = VGroup(axes, labels).shift(RIGHT * 1.5)

        circle_center = LEFT * 4.5
        circle = Circle(radius=1.0, color=YELLOW).move_to(circle_center)

        dot = Dot(color=RED)
        dot.move_to(circle.get_center() + RIGHT * 1) 

        
        vector = always_redraw(
            lambda: Line(circle.get_center(), dot.get_center(), color=WHITE)
        )
        self.time_elapsed = 0
        speed = 1.2 
    
        wave = always_redraw(
            lambda: axes.plot(
                lambda x: np.sin(x),
                x_range=[0, min(4 * np.pi, max(0.001, self.time_elapsed))],
                color=RED
            )
        )

        guide_line = always_redraw(
            lambda: Line(
                start=dot.get_center(),
                end=axes.c2p(min(4 * np.pi, self.time_elapsed), np.sin(min(4 * np.pi, self.time_elapsed))),
                color=GRAY,
                stroke_width=1.5,
                stroke_opacity=0.6
            )
        )

        
        def update_scene(mob, dt):
            self.time_elapsed += speed * dt
            
            if self.time_elapsed <= 4 * np.pi:
                dot.rotate(speed * dt, about_point=circle.get_center())
            else:
               
                dot.move_to(circle.get_center() + RIGHT * 1)

        self.play(DrawBorderThenFill(axes), Write(labels))
        self.play(Create(circle))
        self.add(vector, dot, guide_line, wave)

        self.wait(3)

       
        wave.add_updater(update_scene)
        
        duration_to_4pi = (4 * np.pi) / speed
        self.wait(duration_to_4pi)
     
        wave.remove_updater(update_scene)
        self.wait(2)
        self.play(FadeOut(VGroup(axes, labels, circle, vector, dot, guide_line, wave)))

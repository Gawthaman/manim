from manim import *

class ButterflyUnit(Scene):
    def construct(self):
        # --- CONFIGURATION ---
        # Colors for different parts of the flow
        input_color = BLUE
        output_color = GREEN
        twiddle_color = YELLOW
        op_color = RED

        # --- 1. SETUP NODES ---
        # Positions
        left_x = -3
        right_x = 3
        top_y = 2
        bottom_y = -2

        # Input Nodes (Left)
        in_top_dot = Dot(point=[left_x, top_y, 0], color=input_color)
        in_bot_dot = Dot(point=[left_x, bottom_y, 0], color=input_color)
        
        # Output Nodes (Right)
        out_top_dot = Dot(point=[right_x, top_y, 0], color=output_color)
        out_bot_dot = Dot(point=[right_x, bottom_y, 0], color=output_color)

        # Labels
        in_top_label = MathTex("A").next_to(in_top_dot, LEFT)
        in_bot_label = MathTex("B").next_to(in_bot_dot, LEFT)
        
        out_top_label = MathTex("A + W_N^k B").next_to(out_top_dot, RIGHT)
        out_bot_label = MathTex("A - W_N^k B").next_to(out_bot_dot, RIGHT)

        # Group inputs for animation
        inputs = VGroup(in_top_dot, in_bot_dot, in_top_label, in_bot_label)
        outputs = VGroup(out_top_dot, out_bot_dot, out_top_label, out_bot_label)

        # --- 2. DRAW LINES (THE BUTTERFLY) ---
        # Horizontal Lines
        line_top = Line(in_top_dot.get_center(), out_top_dot.get_center())
        line_bot = Line(in_bot_dot.get_center(), out_bot_dot.get_center())
        
        # Diagonal Lines (The Cross)
        line_cross_down = Line(in_top_dot.get_center(), out_bot_dot.get_center())
        line_cross_up = Line(in_bot_dot.get_center(), out_top_dot.get_center())

        butterfly_lines = VGroup(line_top, line_bot, line_cross_down, line_cross_up)

        # --- 3. LABELS FOR OPERATIONS ---
        # Twiddle Factor on the bottom input leg
        twiddle_label = MathTex("W_N^k", color=twiddle_color).next_to(in_bot_dot, RIGHT, buff=1).shift(UP*0.5)
        
        # -1 on the bottom output leg (for the subtraction)
        minus_label = MathTex("-1", color=op_color).next_to(out_bot_dot, LEFT, buff=1.5).shift(UP*0.5)

        # Arrows to indicate direction
        arrow_top = Arrow(start=LEFT, end=RIGHT, color=WHITE).scale(0.5).move_to(line_top.get_center())
        arrow_bot = Arrow(start=LEFT, end=RIGHT, color=WHITE).scale(0.5).move_to(line_bot.get_center())

        # --- 4. ANIMATION SEQUENCE ---
        
        # Scene 1: Introduce Inputs
        self.play(FadeIn(inputs))
        self.wait(1)

        # Scene 2: Draw the Butterfly Structure
        self.play(Create(butterfly_lines), run_time=2)
        self.play(FadeIn(arrow_top), FadeIn(arrow_bot))

        # Scene 3: Apply Weights (The Math)
        self.play(Write(twiddle_label))
        self.play(Indicate(twiddle_label, color=twiddle_color))
        self.wait(0.5)
        
        self.play(Write(minus_label))
        self.play(Indicate(minus_label, color=op_color))
        self.wait(1)

        # Scene 4: Show Outputs
        self.play(FadeIn(outputs))
        self.wait(2)

        # Scene 5: Simplify visually (Optional Logic Flow)
        # Trace the path for the Top Output (A + WB)
        path_top_A = Line(in_top_dot.get_center(), out_top_dot.get_center(), color=YELLOW, stroke_width=5)
        path_top_B = Line(in_bot_dot.get_center(), out_top_dot.get_center(), color=YELLOW, stroke_width=5)
        
        self.play(Create(path_top_A), Create(path_top_B), run_time=1.5)
        self.play(Indicate(out_top_label))
        self.play(FadeOut(path_top_A), FadeOut(path_top_B))

        # Trace the path for the Bottom Output (A - WB)
        path_bot_A = Line(in_top_dot.get_center(), out_bot_dot.get_center(), color=RED, stroke_width=5)
        path_bot_B = Line(in_bot_dot.get_center(), out_bot_dot.get_center(), color=RED, stroke_width=5)

        self.play(Create(path_bot_A), Create(path_bot_B), run_time=1.5)
        self.play(Indicate(out_bot_label))
        self.play(FadeOut(path_bot_A), FadeOut(path_bot_B))

        self.wait(2)
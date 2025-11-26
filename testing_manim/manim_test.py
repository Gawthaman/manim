from manim import *
import math

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

class ComplexityComparison(Scene):
    def construct(self):
        # 1. Setup White Background
        self.camera.background_color = WHITE
        
        # 2. Create Axes
        # x_range: [min, max, step], y_range: [min, max, step]
        # We limit N to 20 because N^2 grows extremely fast (20^2 = 400)
        axes = Axes(
            x_range=[0, 25, 5],
            y_range=[0, 450, 50],
            axis_config={"color": BLACK, "include_numbers": True},
            tips=False,
        ).scale(0.8)

        # Labels for axes
        x_label = axes.get_x_axis_label("N (Samples)", edge=DOWN, direction=DOWN, buff=0.2).set_color(BLACK)
        y_label = axes.get_y_axis_label("Operations", edge=LEFT, direction=LEFT, buff=0.2).set_color(BLACK).rotate(PI/2)
        
        # 3. Define the Functions
        # DFT: O(N^2)
        dft_graph = axes.plot(
            lambda x: x**2,
            x_range=[0, 20],
            color=RED,
            stroke_width=4
        )
        
        # FFT: O(N log N)
        # We use log base 2 for accurate complexity representation
        # Handling x=0 case to avoid math domain error
        fft_graph = axes.plot(
            lambda x: x * math.log2(x) if x > 0.1 else 0,
            x_range=[0, 25],
            color=BLUE,
            stroke_width=4
        )

        # 4. Create Labels for the Lines
        dft_label = MathTex("DFT: O(N^2)", color=RED).move_to(axes.c2p(15, 350))
        fft_label = MathTex("FFT: O(N \\log N)", color=BLUE).move_to(axes.c2p(22, 50))

        # 5. Animation Sequence
        self.play(Create(axes), Write(x_label), Write(y_label), run_time=1.5)
        
        # Draw both curves simultaneously to show the race
        self.play(
            Create(dft_graph), 
            Create(fft_graph), 
            run_time=3
        )
        
        # Label them
        self.play(Write(dft_label), Write(fft_label))
        
        # 6. Emphasize the gap
        # Draw a vertical line at N=20 to show the massive difference in operations
        line_at_20 = axes.get_vertical_line(axes.c2p(20, 400), color=BLACK, line_func=DashedLine)
        
        # Dots at the intersection of N=20
        dot_dft = Dot(axes.c2p(20, 400), color=RED)
        dot_fft = Dot(axes.c2p(20, 20 * math.log2(20)), color=BLUE) # approx 86
        
        self.play(Create(line_at_20))
        self.play(FadeIn(dot_dft), FadeIn(dot_fft))
        
        # Add a brace or text to show the savings
        brace = BraceBetweenPoints(dot_fft.get_center(), dot_dft.get_center(), direction=LEFT, color=BLACK)
        savings_text = Text("Huge Savings", font_size=24, color=BLACK).next_to(brace, LEFT)
        
        self.play(GrowFromCenter(brace), Write(savings_text))

        self.wait(2)
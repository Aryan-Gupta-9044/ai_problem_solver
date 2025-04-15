import tkinter as tk
from tkinter import ttk, messagebox
import os
import subprocess
import sys
from PIL import Image, ImageTk
import webbrowser

class AISolverHub:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Problem Solvers Hub")
        self.root.geometry("900x600")
        self.root.minsize(900, 600)
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Use 'clam' theme as base
        
        # Define colors
        self.bg_color = "#f5f5f5"
        self.accent_color = "#4a6fa5"
        self.secondary_color = "#6b8cae"
        self.text_color = "#2c3e50"
        self.card_bg = "#ffffff"
        
        # Configure styles
        self.style.configure("TFrame", background=self.bg_color)
        self.style.configure("Card.TFrame", background=self.card_bg, relief="raised")
        self.style.configure("TLabel", background=self.bg_color, foreground=self.text_color, font=("Segoe UI", 10))
        self.style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), foreground=self.accent_color)
        self.style.configure("Title.TLabel", font=("Segoe UI", 24, "bold"), foreground=self.accent_color)
        self.style.configure("Subtitle.TLabel", font=("Segoe UI", 12), foreground=self.secondary_color)
        self.style.configure("Card.TLabel", background=self.card_bg)
        self.style.configure("CardTitle.TLabel", background=self.card_bg, font=("Segoe UI", 14, "bold"), foreground=self.accent_color)
        self.style.configure("CardDesc.TLabel", background=self.card_bg, wraplength=300)
        
        # Main frame
        main_frame = ttk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(header_frame, text="AI Problem Solvers Hub", style="Title.TLabel").pack(anchor="center")
        ttk.Label(header_frame, text="Select an AI algorithm to explore", style="Subtitle.TLabel").pack(anchor="center")
        
        # Solver cards container
        self.cards_frame = ttk.Frame(main_frame)
        self.cards_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create cards for each solver
        self.create_solver_cards()
        
        # Footer
        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(fill=tk.X, pady=(20, 0))
        ttk.Label(footer_frame, text="All programs must be in the same directory as this launcher").pack(side=tk.LEFT)
        
        # GitHub link
        github_button = ttk.Button(footer_frame, text="View on GitHub", command=self.open_github)
        github_button.pack(side=tk.RIGHT)
    
    def create_solver_cards(self):
        # Define solver information
        solvers = [
            {
                "title": "Wumpus World",
                "description": "Navigate a dangerous cave to find gold while avoiding the Wumpus and deadly pits. Features AI agent navigation and logical reasoning.",
                "tags": ["Knowledge Representation", "Logic", "Pathfinding"],
                "file": "wumpus demo4.py",
                "icon": "🧭"
            },
            {
                "title": "Tic-Tac-Toe AI",
                "description": "Challenge an AI opponent in Tic-Tac-Toe that never loses. Implements the Minimax algorithm for perfect gameplay.",
                "tags": ["Game Theory", "Minimax", "Adversarial Search"],
                "file": "ticktack.py",
                "icon": "🎮"
            },
            {
                "title": "Minimax & Alpha-Beta",
                "description": "Visualize and compare the efficiency of Minimax vs. Alpha-Beta Pruning algorithms on game trees.",
                "tags": ["Game Trees", "Optimization", "Visualization"],
                "file": "mini alpha.py",
                "icon": "🌳"
            },
            {
                "title": "Cryptarithmetic Solver",
                "description": "Solve word puzzles where letters represent digits in arithmetic operations. Uses constraint satisfaction techniques.",
                "tags": ["CSP", "Backtracking", "Puzzle Solving"],
                "file": "criptdemo1.py",
                "icon": "🔢"
            }
        ]
        
        # Create 2x2 grid of cards
        for i, solver in enumerate(solvers):
            row = i // 2
            col = i % 2
            
            self.create_card(self.cards_frame, solver, row, col)
    
    def create_card(self, parent, solver_info, row, col):
        # Card frame
        card = ttk.Frame(parent, style="Card.TFrame", padding=15)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        # Configure grid weights to make cards expand
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=1)
        parent.rowconfigure(0, weight=1)
        parent.rowconfigure(1, weight=1)
        
        # Icon and title in one row
        header_frame = ttk.Frame(card, style="Card.TFrame")
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Icon label - large emoji
        icon_label = ttk.Label(header_frame, text=solver_info["icon"], font=("Segoe UI", 36), style="Card.TLabel")
        icon_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Title and tags in a vertical frame
        title_frame = ttk.Frame(header_frame, style="Card.TFrame")
        title_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        ttk.Label(title_frame, text=solver_info["title"], style="CardTitle.TLabel").pack(anchor="w")
        
        # Tags frame
        tags_frame = ttk.Frame(title_frame, style="Card.TFrame")
        tags_frame.pack(fill=tk.X, pady=(5, 0))
        
        for tag in solver_info["tags"]:
            tag_label = ttk.Label(tags_frame, text=tag, style="Card.TLabel",
                                 background=self.secondary_color, foreground="white",
                                 padding=(5, 2))
            tag_label.pack(side=tk.LEFT, padx=(0, 5))
        
        # Description
        desc_label = ttk.Label(card, text=solver_info["description"], style="CardDesc.TLabel")
        desc_label.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Launch button
        launch_btn = tk.Button(card, text="Launch Program", bg=self.accent_color, fg="white",
                              font=("Segoe UI", 11, "bold"), bd=0, padx=10, pady=5,
                              activebackground=self.secondary_color, activeforeground="white",
                              command=lambda file=solver_info["file"]: self.launch_program(file))
        launch_btn.pack(fill=tk.X)
    
    def launch_program(self, filename):
        try:
            # Check if file exists
            if not os.path.exists(filename):
                messagebox.showerror("File Not Found", f"Could not find {filename}. Make sure all program files are in the same directory as this launcher.")
                return
            
            # Launch the program
            if sys.platform.startswith('win'):
                # Windows
                subprocess.Popen(['python', filename], creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:
                # macOS and Linux
                subprocess.Popen(['python3', filename])
                
            self.root.iconify()  # Minimize the launcher window while program is running
            
        except Exception as e:
            messagebox.showerror("Launch Error", f"Error launching {filename}: {str(e)}")
    
    def open_github(self):
        # Replace with your actual GitHub repository URL
        webbrowser.open("https://github.com/yourusername/ai-solvers")


# Execute the application
if __name__ == "__main__":
    root = tk.Tk()
    app = AISolverHub(root)
    root.mainloop()

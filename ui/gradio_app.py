import gradio as gr
import asyncio
import os
import time
from pathlib import Path
import tempfile
from fpdf import FPDF

# Import from parent directory
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.runner import make_food_recipe
from utils.Diet import Diet
from utils.Difficulty import Difficulty
from utils.file_downloader import download_from_link
from constants.output import *
from constants.flyer import FLYER_URL, FLYER_FILEPATH

# CSS for styling
css = """
.gradio-container {
    font-family: 'Poppins', sans-serif !important;
}

h1, h2, h3 {
    font-weight: 700 !important;
    margin-bottom: 0.5rem !important;
}

.app-title {
    text-align: center;
    margin-bottom: 1rem !important;
    color: #2D3748;
    font-size: 2.5rem !important;
    background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradient 3s ease infinite;
    background-size: 200% auto;
}

@keyframes gradient {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

.container {
    border-radius: 1rem !important;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1) !important;
    backdrop-filter: blur(5px) !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
    padding: 1.5rem !important;
    margin-bottom: 1rem !important;
    background-color: rgba(255, 255, 255, 0.8) !important;
    transition: transform 0.3s ease !important;
}

.container:hover {
    transform: translateY(-5px) !important;
}

.recipe-title {
    font-size: 1.8rem !important;
    color: #2D3748 !important;
    margin-bottom: 1rem !important;
    border-bottom: 2px solid #4ECDC4 !important;
    padding-bottom: 0.5rem !important;
}

.recipe-cost {
    font-size: 1.5rem !important;
    font-weight: bold !important;
    color: #FF6B6B !important;
    margin-top: 1rem !important;
    text-align: right !important;
}

.loading-animation {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100px;
}

.chef-emoji {
    font-size: 3rem;
    margin-right: 1rem;
    animation: bounce 1s infinite alternate;
}

@keyframes bounce {
    from {transform: translateY(0px);}
    to {transform: translateY(-10px);}
}

/* Hide default Gradio footer */
footer {
    display: none !important;
}
"""

# Custom theme
theme = gr.themes.Soft(
    primary_hue="teal",
    secondary_hue="pink",
).set(
    button_primary_background_fill="#4ECDC4",
    button_primary_background_fill_hover="#3DBCB5",
    button_secondary_background_fill="#FF6B6B",
    button_secondary_background_fill_hover="#FF5A5A",
    block_label_background_fill="*neutral_50",
    block_title_text_weight="600",
)

# Store the latest generated recipe
latest_recipe = {
    "title": "",
    "ingredients": "",
    "instructions": "",
    "cost": ""
}

async def generate_recipe(diet_choice, difficulty_choice):
    """Generate a recipe based on diet and difficulty choices"""
    # Create progress animation with detailed steps - REMOVED STEP 2
    progress_html = """
    <div class="container">
        <div class="loading-animation">
            <div class="chef-emoji">👨‍🍳</div>
            <div style="width: 100%;">
                <h3>Cooking up your recipe...</h3>
                <div id="progress-bar" style="width: 0%; height: 10px; background-color: #4ECDC4; border-radius: 5px; transition: width 0.3s;"></div>
                
                <div id="step1" style="margin-top: 15px; padding: 10px; border-radius: 8px; background-color: #EDF2F7;">
                    <div style="display: flex; align-items: center;">
                        <div id="step1-icon" style="margin-right: 10px; font-size: 1.2rem;">⏳</div>
                        <div>
                            <div id="step1-title" style="font-weight: bold;">Step 1: Downloading flyer...</div>
                            <div id="step1-desc" style="font-size: 0.9rem;">Getting the latest deals from the supermarket</div>
                        </div>
                    </div>
                </div>
                
                <div id="step2" style="margin-top: 10px; padding: 10px; border-radius: 8px; background-color: #EDF2F7; opacity: 0.5;">
                    <div style="display: flex; align-items: center;">
                        <div id="step2-icon" style="margin-right: 10px; font-size: 1.2rem;">⏳</div>
                        <div>
                            <div id="step2-title" style="font-weight: bold;">Step 2: Filtering for dietary preferences</div>
                            <div id="step2-desc" style="font-size: 0.9rem;">Selecting items that match your diet</div>
                        </div>
                    </div>
                </div>
                
                <div id="step3" style="margin-top: 10px; padding: 10px; border-radius: 8px; background-color: #EDF2F7; opacity: 0.5;">
                    <div style="display: flex; align-items: center;">
                        <div id="step3-icon" style="margin-right: 10px; font-size: 1.2rem;">⏳</div>
                        <div>
                            <div id="step3-title" style="font-weight: bold;">Step 3: Creating your custom recipe</div>
                            <div id="step3-desc" style="font-size: 0.9rem;">Crafting a delicious recipe based on your preferences</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        const progressBar = document.getElementById('progress-bar');
        let width = 0;
        
        // Step 1 animation
        document.getElementById('step1-icon').textContent = "🔄";
        document.getElementById('step1').style.backgroundColor = "#E6FFFA";
        document.getElementById('step1').style.borderLeft = "4px solid #4ECDC4";
        
        const interval = setInterval(() => {
            if (width >= 100) {
                clearInterval(interval);
            } else {
                width += 0.5;
                progressBar.style.width = width + '%';
                
                // Update step indicators - ADJUSTED FOR REMOVED STEP
                if (width > 33) {
                    document.getElementById('step1-icon').textContent = "✅";
                    document.getElementById('step2-icon').textContent = "🔄";
                    document.getElementById('step2').style.opacity = "1";
                    document.getElementById('step2').style.backgroundColor = "#E6FFFA";
                    document.getElementById('step2').style.borderLeft = "4px solid #4ECDC4";
                }
                
                if (width > 66) {
                    document.getElementById('step2-icon').textContent = "✅";
                    document.getElementById('step3-icon').textContent = "🔄";
                    document.getElementById('step3').style.opacity = "1";
                    document.getElementById('step3').style.backgroundColor = "#E6FFFA";
                    document.getElementById('step3').style.borderLeft = "4px solid #4ECDC4";
                }
                
                if (width >= 100) {
                    document.getElementById('step3-icon').textContent = "✅";
                }
            }
        }, 50);
    </script>
    """
    
    yield progress_html
    
    # Map the diet and difficulty choices to their respective enums
    diet_map = {
        "Omnivorous 🍖🥗": Diet.OMNIVOROUS,
        "Carnivore 🥩": Diet.CARNIVORE,
        "Vegetarian 🥗": Diet.VEGETARIAN,
        "Vegan 🌱": Diet.VEGAN,
        "Fruitarian 🍎": Diet.FRUITARIAN
    }
    
    difficulty_map = {
        "Easy 😌": Difficulty.EASY,
        "Medium 😊": Difficulty.MEDIUM,
        "Hard 😅": Difficulty.HARD
    }
    
    try:
        diet = diet_map[diet_choice]
        difficulty = difficulty_map[difficulty_choice]
        
        # Call the existing function to generate the recipe
        result = await make_food_recipe(diet, difficulty)
        
        # Format the ingredients as a list
        ingredients_list = ""
        for ingredient in result[RECIPE_INGREDIENTS_KEY].split('\n'):
            if ingredient.strip():
                parts = ingredient.split('§')
                if len(parts) >= 2:
                    product, price = parts[0].strip(), parts[1].strip()
                    ingredients_list += f"• {product} - {price}€\n"
                else:
                    ingredients_list += f"• {ingredient.strip()}\n"
        
        # Format the result as HTML
        recipe_title = result[RECIPE_TITLE_KEY]
        recipe_cost = result[RECIPE_COST_KEY]
        recipe_instructions = result[RECIPE_INSTRUCTIONS_KEY]
        
        # Store the recipe data for display
        global latest_recipe
        latest_recipe = {
            "title": recipe_title,
            "ingredients": ingredients_list,
            "instructions": recipe_instructions,
            "cost": recipe_cost
        }
        
        html_result = f"""
        <div class="container">
            <h2 class="recipe-title">{recipe_title}</h2>
            
            <div style="margin-bottom: 1rem;">
                <h3 style="color: #4A5568; margin-bottom: 0.5rem;">Ingredients:</h3>
                <pre style="background-color: #F7FAFC; padding: 1rem; border-radius: 0.5rem; white-space: pre-wrap;">{ingredients_list}</pre>
            </div>
            
            <div style="margin-bottom: 1rem;">
                <h3 style="color: #4A5568; margin-bottom: 0.5rem;">Instructions:</h3>
                <div style="background-color: #F7FAFC; padding: 1rem; border-radius: 0.5rem; white-space: pre-wrap;">{recipe_instructions}</div>
            </div>
            
            <div class="recipe-cost">Total Cost: {recipe_cost}€</div>
        </div>
        """
        
        yield html_result
    except Exception as e:
        error_html = f"""
        <div class="container" style="border-color: #FF6B6B !important;">
            <h3 style="color: #FF6B6B;">Error generating recipe</h3>
            <p>{str(e)}</p>
        </div>
        """
        yield error_html

def launch_app():
    with gr.Blocks(css=css, theme=theme) as app:
        gr.HTML("""
        <div style="text-align: center; margin-bottom: 1rem;">
            <h1 class="app-title">👨‍🍳 Personal Chef AI</h1>
            <p style="font-size: 1.2rem; color: #4A5568;">Your intelligent cooking assistant that creates budget-friendly recipes</p>
        </div>
        """)
        
        with gr.Row():
            with gr.Column(scale=1):
                gr.HTML("""
                <div class="container">
                    <h3>About Personal Chef AI</h3>
                    <p>Personal Chef AI analyzes supermarket flyers to find the best deals and creates recipes based on your dietary preferences and cooking skill level.</p>
                    <p>Simply select your diet and desired recipe difficulty, and let our AI chef do the work!</p>
                    <div style="text-align: center; margin-top: 1rem; font-size: 5rem;">
                        👨‍🍳
                    </div>
                </div>
                """)
            
            with gr.Column(scale=1):
                gr.HTML("""
                <div class="container">
                    <h3>How it works</h3>
                    <div style="display: flex; align-items: center; margin-bottom: 10px;">
                        <div style="background-color: #FF6B6B; color: white; width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 10px;">1</div>
                        <div>Our AI downloads the latest supermarket flyer</div>
                    </div>
                    <div style="display: flex; align-items: center; margin-bottom: 10px;">
                        <div style="background-color: #FF6B6B; color: white; width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 10px;">2</div>
                        <div>Filters based on your dietary preferences</div>
                    </div>
                    <div style="display: flex; align-items: center; margin-bottom: 10px;">
                        <div style="background-color: #FF6B6B; color: white; width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 10px;">3</div>
                        <div>Creates a custom recipe matching your cooking skills</div>
                    </div>
                    <div style="display: flex; align-items: center; margin-bottom: 10px;">
                        <div style="background-color: #FF6B6B; color: white; width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 10px;">4</div>
                        <div>Calculates the total cost of the recipe</div>
                    </div>
                </div>
                """)
    
        with gr.Row():
            with gr.Column():
                # Detailed diet descriptions with images
                diet_info_html = gr.HTML("""
                <div class="container">
                    <h3>Dietary Options</h3>
                    <div style="display: flex; flex-wrap: wrap; gap: 10px;">
                        <div style="flex: 1; min-width: 150px; background-color: #F7FAFC; padding: 10px; border-radius: 8px; border-left: 4px solid #FF6B6B;">
                            <div style="font-size: 1.5rem;">🍖🥗</div>
                            <strong>Omnivorous</strong>
                            <p style="font-size: 0.9rem;">Includes all types of foods</p>
                        </div>
                        <div style="flex: 1; min-width: 150px; background-color: #F7FAFC; padding: 10px; border-radius: 8px; border-left: 4px solid #FF6B6B;">
                            <div style="font-size: 1.5rem;">🥩</div>
                            <strong>Carnivore</strong>
                            <p style="font-size: 0.9rem;">Primarily meat-based</p>
                        </div>
                        <div style="flex: 1; min-width: 150px; background-color: #F7FAFC; padding: 10px; border-radius: 8px; border-left: 4px solid #4ECDC4;">
                            <div style="font-size: 1.5rem;">🥗</div>
                            <strong>Vegetarian</strong>
                            <p style="font-size: 0.9rem;">No meat, may include dairy</p>
                        </div>
                        <div style="flex: 1; min-width: 150px; background-color: #F7FAFC; padding: 10px; border-radius: 8px; border-left: 4px solid #4ECDC4;">
                            <div style="font-size: 1.5rem;">🌱</div>
                            <strong>Vegan</strong>
                            <p style="font-size: 0.9rem;">No animal products</p>
                        </div>
                        <div style="flex: 1; min-width: 150px; background-color: #F7FAFC; padding: 10px; border-radius: 8px; border-left: 4px solid #4ECDC4;">
                            <div style="font-size: 1.5rem;">🍎</div>
                            <strong>Fruitarian</strong>
                            <p style="font-size: 0.9rem;">Fruits, nuts, and seeds</p>
                        </div>
                    </div>
                </div>
                """)
                
                diet_choice = gr.Radio(
                    choices=[
                        "Omnivorous 🍖🥗",
                        "Carnivore 🥩",
                        "Vegetarian 🥗",
                        "Vegan 🌱",
                        "Fruitarian 🍎"
                    ],
                    label="Select Your Diet",
                    value="Omnivorous 🍖🥗"
                )
                
                # Difficulty descriptions
                difficulty_info_html = gr.HTML("""
                <div class="container">
                    <h3>Difficulty Levels</h3>
                    <div style="display: flex; flex-wrap: wrap; gap: 10px;">
                        <div style="flex: 1; min-width: 150px; background-color: #F7FAFC; padding: 10px; border-radius: 8px; border-left: 4px solid #63B3ED;">
                            <div style="font-size: 1.5rem;">😌</div>
                            <strong>Easy</strong>
                            <p style="font-size: 0.9rem;">Simple ingredients, minimal steps, under 30 minutes</p>
                        </div>
                        <div style="flex: 1; min-width: 150px; background-color: #F7FAFC; padding: 10px; border-radius: 8px; border-left: 4px solid #F6AD55;">
                            <div style="font-size: 1.5rem;">😊</div>
                            <strong>Medium</strong>
                            <p style="font-size: 0.9rem;">More complex techniques, 30-60 minutes preparation</p>
                        </div>
                        <div style="flex: 1; min-width: 150px; background-color: #F7FAFC; padding: 10px; border-radius: 8px; border-left: 4px solid #F56565;">
                            <div style="font-size: 1.5rem;">😅</div>
                            <strong>Hard</strong>
                            <p style="font-size: 0.9rem;">Advanced techniques, multiple steps, over 60 minutes</p>
                        </div>
                    </div>
                </div>
                """)
                
                difficulty_choice = gr.Radio(
                    choices=[
                        "Easy 😌",
                        "Medium 😊", 
                        "Hard 😅"
                    ],
                    label="Recipe Difficulty",
                    value="Medium 😊"
                )
                
                generate_btn = gr.Button("Generate Recipe", variant="primary", elem_classes="generate-btn")
                
                # Add custom CSS for the margin below the generate button
                gr.HTML("""
                <style>
                    .generate-btn {
                        margin-bottom: 2rem !important;
                    }
                </style>
                """)
        
        output = gr.HTML(
            label="Your Recipe",
            value="""
            <div class="container" style="text-align: center;">
                <h3>Your recipe will appear here</h3>
                <div class="chef-emoji" style="font-size: 5rem; margin: 2rem 0;">👨‍🍳</div>
                <p>Click "Generate Recipe" to start!</p>
            </div>
            """
        )
        
        # Connect the generate button to the function
        generate_btn.click(
            fn=generate_recipe,
            inputs=[diet_choice, difficulty_choice],
            outputs=output
        )
        
    return app

if __name__ == "__main__":
    app = launch_app()
    app.launch(share=True, show_api=False)
#!/usr/bin/env python
# coding: utf-8

# # L2: Interactive AI Applications: Building a Simple AI Role Playing Game (RPG)

# <p style="background-color:#f7fff8; padding:15px; border-width:3px; border-color:#e0f0e0; border-style:solid; border-radius:6px"> 🚨
# &nbsp; <b>Different Run Results:</b> The output generated by AI models can vary with each execution due to their dynamic, probabilistic nature. Don't be surprised if your results differ from those shown in the video.<br>
# <span style="font-size: larger;">To maintain consistency, the notebooks are run with a 'world state' consistent with the video at the start of each notebook.</span></p>

# <div style="background-color:#fff6ff; padding:13px; border-width:3px; border-color:#efe6ef; border-style:solid; border-radius:6px">
# <p> 💻 &nbsp; <b>Access <code>requirements.txt</code> and <code>helper.py</code> files:</b> 1) click on the <em>"File"</em> option on the top menu of the notebook and then 2) click on <em>"Open"</em>.
# 
# <p> ⬇ &nbsp; <b>Download Notebooks:</b> 1) click on the <em>"File"</em> option on the top menu of the notebook and then 2) click on <em>"Download as"</em> and select <em>"Notebook (.ipynb)"</em>.</p>
# 
# <p> 📒 &nbsp; For more help, please see the <em>"Appendix – Tips, Help, and Download"</em> Lesson.</p>
# 
# </div>

# ## Create a Game UI with Gradio

# In[ ]:


import gradio as gr
import os
demo = None #added to allow restart

def start_game(main_loop, share=False):
    # added code to support restart
    global demo
    # If demo is already running, close it first
    if demo is not None:
        demo.close()

    demo = gr.ChatInterface(
        main_loop,
        chatbot=gr.Chatbot(height=250, placeholder="Type 'start game' to begin"),
        textbox=gr.Textbox(placeholder="What do you do next?", container=False, scale=7),
        title="AI RPG",
        # description="Ask Yes Man any question",
        theme="soft",
        examples=["Look around", "Continue the story"],
        cache_examples=False,
        retry_btn="Retry",
        undo_btn="Undo",
        clear_btn="Clear",
                           )
    demo.launch(share=share, server_name="0.0.0.0")

def test_main_loop(message, history):
    return 'Entered Action: ' + message

start_game(test_main_loop)


# ## Generating an Initial Start

# In[ ]:


from helper import load_world, save_world
from together import Together
from helper import get_together_api_key, load_env

client = Together(api_key=get_together_api_key())

world = load_world('../shared_data/Kyropeia.json')
kingdom = world['kingdoms']['Eldrida']
town = kingdom['towns']["Luminaria"]
character = town['npcs']['Elwyn Stormbringer']


# In[ ]:


system_prompt = """You are an AI Game master. Your job is to create a 
start to an adventure based on the world, kingdom, town and character 
a player is playing as. 
Instructions:
You must only use 2-4 sentences \
Write in second person. For example: "You are Jack" \
Write in present tense. For example "You stand at..." \
First describe the character and their backstory. \
Then describes where they start and what they see around them."""
world_info = f"""
World: {world}
Kingdom: {kingdom}
Town: {town}
Your Character: {character}
"""


# In[ ]:


model_output = client.chat.completions.create(
    model="meta-llama/Llama-3-70b-chat-hf",
    temperature=1.0,
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": world_info + '\nYour Start:'}
    ],
)


# In[ ]:


start = model_output.choices[0].message.content
print(start)
world['start'] = start
#save_world(world, '../shared_data/Kyropeia.json')  # preserve video version
save_world(world, '../shared_data/YourWorld_L1.json')


# ## Creating the Main Action Loop

# In[ ]:


def run_action(message, history, game_state):
    
    if(message == 'start game'):
        return game_state['start']

    system_prompt = """You are an AI Game master. Your job is to write what \
happens next in a player's adventure game.\
Instructions: \
You must on only write 1-3 sentences in response. \
Always write in second person present tense. \
Ex. (You look north and see...)"""
    
    world_info = f"""
World: {game_state['world']}
Kingdom: {game_state['kingdom']}
Town: {game_state['town']}
Your Character:  {game_state['character']}"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": world_info}
    ]
    for action in history:
        messages.append({"role": "assistant", "content": action[0]})
        messages.append({"role": "user", "content": action[1]})

    messages.append({"role": "user", "content": message})
    model_output = client.chat.completions.create(
        model="meta-llama/Llama-3-70b-chat-hf",
        messages=messages
    )
    
    result = model_output.choices[0].message.content
    return result


# In[ ]:


game_state = {
    "world": world['description'],
    "kingdom": kingdom['description'],
    "town": town['description'],
    "character": character['description'],
    "start": start,
}

def main_loop(message, history):
    return run_action(message, history, game_state)


# ## Launch and Share!

# In[ ]:


start_game(main_loop, True)


# In[ ]:




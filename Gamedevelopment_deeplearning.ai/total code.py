# -*- coding: utf-8 -*-
"""L1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/133XGvF-77QSSUZWLGc5PYKyTq5PCu24l

# L1: Hierarchical Content Generation

## Creating a World
"""

system_prompt = f"""
Your job is to help create interesting fantasy worlds that \
players would love to play in.
Instructions:
- Only generate in plain text without formatting.
- Use simple clear language without being flowery.
- You must stay below 3-5 sentences for each description.
"""

!pip install together
from together import Together

world_prompt = f"""
Generate a creative description for a unique fantasy world with an
interesting concept around cities build on the backs of massive beasts.

Output content in the form:
World Name: <WORLD NAME>
World Description: <WORLD DESCRIPTION>

World Name:"""

from together import Together


client = Together(api_key="ba165e8f31997a1b05e243e5c9a059d2a37aa9225011017c610e1ffed98009e9")

output = client.chat.completions.create(
    model="meta-llama/Llama-3-70b-chat-hf",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": world_prompt}
    ],
)

world_output =output.choices[0].message.content
print(world_output)

world_output = world_output.strip()
world = {
    "name": world_output.split('\n')[0].strip()
    .replace('World Name: ', ''),
    "description": '\n'.join(world_output.split('\n')[1:])
    .replace('World Description:', '').strip()
}

"""## Generating Kingdoms"""

kingdom_prompt = f"""
Create 3 different kingdoms for a fantasy world.
For each kingdom generate a description based on the world it's in. \
Describe important leaders, cultures, history of the kingdom.\

Output content in the form:
Kingdom 1 Name: <KINGDOM NAME>
Kingdom 1 Description: <KINGDOM DESCRIPTION>
Kingdom 2 Name: <KINGDOM NAME>
Kingdom 2 Description: <KINGDOM DESCRIPTION>
Kingdom 3 Name: <KINGDOM NAME>
Kingdom 3 Description: <KINGDOM DESCRIPTION>

World Name: {world['name']}
World Description: {world['description']}

Kingdom 1"""

output = client.chat.completions.create(
    model="meta-llama/Llama-3-70b-chat-hf",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": kingdom_prompt}
    ],
)

kingdoms = {}
kingdoms_output = output.choices[0].message.content

for output in kingdoms_output.split('\n\n'):
  kingdom_name = output.strip().split('\n')[0] \
    .split('Name: ')[1].strip()
  print(f'Created kingdom "{kingdom_name}" in {world["name"]}')
  kingdom_description = output.strip().split('\n')[1] \
    .split('Description: ')[1].strip()
  kingdom = {
      "name": kingdom_name,
      "description": kingdom_description,
      "world": world['name']
  }
  kingdoms[kingdom_name] = kingdom
world['kingdoms'] = kingdoms

print(f'\nKingdom 1 Description: \
{kingdom["description"]}')

"""## Generating Towns"""

def get_town_prompt(world, kingdom):
    return f"""
    Create 3 different towns for a fantasy kingdom abd world. \
    Describe the region it's in, important places of the town, \
    and interesting history about it. \

    Output content in the form:
    Town 1 Name: <TOWN NAME>
    Town 1 Description: <TOWN DESCRIPTION>
    Town 2 Name: <TOWN NAME>
    Town 2 Description: <TOWN DESCRIPTION>
    Town 3 Name: <TOWN NAME>
    Town 3 Description: <TOWN DESCRIPTION>

    World Name: {world['name']}
    World Description: {world['description']}

    Kingdom Name: {kingdom['name']}
    Kingdom Description {kingdom['description']}

    Town 1 Name:"""

def create_towns(world, kingdom):
    print(f'\nCreating towns for kingdom: {kingdom["name"]}...')
    output = client.chat.completions.create(
      model="meta-llama/Llama-3-70b-chat-hf",
      messages=[
          {"role": "system", "content": system_prompt},
          {"role": "user", "content": get_town_prompt(world, kingdom)}
      ],
  )
    towns_output = output.choices[0].message.content

    towns = {}
    for output in towns_output.split('\n\n'):
        town_name = output.strip().split('\n')[0]\
        .split('Name: ')[1].strip()
        print(f'- {town_name} created')

        town_description = output.strip().split('\n')[1]\
        .split('Description: ')[1].strip()

        town = {
          "name": town_name,
          "description": town_description,
          "world": world['name'],
          "kingdom": kingdom['name']
        }
        towns[town_name] = town
    kingdom["towns"] = towns

for kingdom in kingdoms.values():
    create_towns(world, kingdom)

town = list(kingdom['towns'].values())[0]
print(f'\nTown 1 Description: \
{town["description"]}')

"""## Generating Non-Player Characters (NPC's)"""

def get_npc_prompt(world, kingdom, town):
    return f"""
    Create 3 different characters based on the world, kingdom \
    and town they're in. Describe the character's appearance and \
    profession, as well as their deeper pains and desires. \

    Output content in the form:
    Character 1 Name: <CHARACTER NAME>
    Character 1 Description: <CHARACTER DESCRIPTION>
    Character 2 Name: <CHARACTER NAME>
    Character 2 Description: <CHARACTER DESCRIPTION>
    Character 3 Name: <CHARACTER NAME>
    Character 3 Description: <CHARACTER DESCRIPTION>

    World Name: {world['name']}
    World Description: {world['description']}

    Kingdom Name: {kingdom['name']}
    Kingdom Description: {kingdom['description']}

    Town Name: {town['name']}
    Town Description: {town['description']}

    Character 1 Name:"""

def create_npcs(world, kingdom, town):
    print(f'\nCreating characters for the town of: {town["name"]}...')
    output = client.chat.completions.create(
        model="meta-llama/Llama-3-70b-chat-hf",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": get_npc_prompt(world, kingdom, town)}
        ],
        temperature=1  #added to generate unique names
    )

    npcs_output = output.choices[0].message.content
    npcs = {}
    for output in npcs_output.split('\n\n'):
        npc_name = output.strip().split('\n')[0]\
        .split('Name: ')[1].strip()
        print(f'- "{npc_name}" created')

        npc_description = output.strip().split('\n')[1\
        ].split('Description: ')[1].strip()

        npc = {
        "name": npc_name,
        "description": npc_description,
        "world": world['name'],
        "kingdom": kingdom['name'],
        "town": town['name']
        }
        npcs[npc_name] = npc
    town["npcs"] = npcs

for kingdom in kingdoms.values():
    for town in kingdom['towns'].values():
        create_npcs(world, kingdom, town)
  # For now we'll only generate npcs for one kingdom
    break

npc = list(town['npcs'].values())[0]

print(f'\nNPC 1 in {town["name"]}, \
{kingdom["name"]}:\n{npc["description"]}')

"""## Save the World
>Note: You will save your world state to a file different than the one shown in the video to allow future lessons to be consistent with the video. If later wish to build your own worlds, you will want to load your file rather than the saved file.
"""

import json
import os

def save_world(world, filename):
    # Get the directory part of the filename
    directory = os.path.dirname(filename)
    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(filename, 'w') as f:
        json.dump(world, f)

def load_world(filename):
    with open(filename, 'r') as f:
        return json.load(f)

#save_world(world, '../shared_data/Kyropeia.json')
save_world(world, '/content/YourWorld_L1.json') #save to your version

!pip install gradio

!pip install python-dotenv

import json # Add this line at the top to import the json module
import os

print(world)

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

                           )
    demo.launch(share=share, server_name="0.0.0.0")

def test_main_loop(message, history):
    return 'Entered Action: ' + message

start_game(test_main_loop)


# ## Generating an Initial Start

# In[ ]:


from helper import load_world, save_world
from together import Together
#from helper import get_together_api_key, load_env
def load_world(filename):
    with open(filename, 'r') as f:
        return json.load(f)
def save_world(world, filename):
    with open(filename, 'w') as f:
        json.dump(world, f)

client = Together(api_key="ba165e8f31997a1b05e243e5c9a059d2a37aa9225011017c610e1ffed98009e9")
world = load_world('/content/YourWorld_L1.json')

# Extracting the first kingdom, town, and NPC dynamically
kingdom_name = next(iter(world['kingdoms']))
kingdom = world['kingdoms'][kingdom_name]

town_name = next(iter(kingdom['towns']))
town = kingdom['towns'][town_name]

npc_name = next(iter(town['npcs']))
character = town['npcs'][npc_name]

# Output the dynamic details
print(f"Kingdom: {kingdom_name}")
print(f"Town: {town_name}")
print(f"Character: {npc_name} - {character}")


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
save_world(world, '/content/YourWorld_L1.json')



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

#!/usr/bin/env python
# coding: utf-8

# # L3: Moderation & Safety of AI Games with Llama Guard
#
# You are going to learn how to use Together AI's API to ensure content generated within AI games adheres to safety and compliance policies.

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

# ## Performing Safety Checks with the Default Content Policy

# In[ ]:


import os
from together import Together
from helper import get_together_api_key, load_env

client = Together(api_key="ba165e8f31997a1b05e243e5c9a059d2a37aa9225011017c610e1ffed98009e9")


# In[ ]:


def get_game_state():
    world = load_world('/content/YourWorld_L1.json')
    # Extracting the first kingdom, town, and NPC dynamically
    kingdom_name = next(iter(world['kingdoms']))
    kingdom = world['kingdoms'][kingdom_name]

    town_name = next(iter(kingdom['towns']))
    town = kingdom['towns'][town_name]

    npc_name = next(iter(town['npcs']))
    character = town['npcs'][npc_name]


    start = world['start']

    game_state = {
        "world": world['description'],
        "kingdom": kingdom['description'],
        "town": town['description'],
        "character": character['description'],
        "start": start,
    }
    return game_state

game_state = get_game_state()
character = game_state["character"]
print("Character Description:", character)


# In[ ]:


safety_check = client.chat.completions.create(
    model="Meta-Llama/LlamaGuard-2-8b",
    messages=[{"role": "user", "content": character}],
)

print(f"prompt safety check: {safety_check.choices[0].message.content}")
print(" ")


# ### Safe Content Policy

# In[ ]:


# Set the content policy
safe_content_policy = {
    "policy": """O1: Violence and Hate.
Should not
- Express hateful, derogatory, or demeaning sentiments against people based on sensitive personal characteristics.
- Use slurs based on personal characteristics
- Write gruesome / graphic violence.
Can
- Write tame fantasy violence
O2: Sexual Content.
Should not
- Write any somewhat sexual content that mentions sexual functions or sexual body parts.
- Write any content that would be inappropriate for kids.
Can
- Write romantic content (including kissing, flirting etc...)
O3: Self-Harm.
Should not
- Encourage people to harm themselves.
- Romanticize or condone self-harm or suicide.
- Write story depicting suicide.
O4: Profanity.
Should not
- Write with any profane language that wouldn't be appropriate for kids.
Can
- Write with kid appropriate language
O5: Regulated or Controlled Substances.
Should not
- Write stories that depicts, glorifies or encourages drug use."""
}


# In[ ]:


check_text = "Kill the troll."

prompt = f"""[INST] Task: Check if there is unsafe content in 'user' messages in conversations according to our safety policy with the below categories.

<BEGIN UNSAFE CONTENT CATEGORIES>
{safe_content_policy['policy']}
<END UNSAFE CONTENT CATEGORIES>

<BEGIN CONVERSATION>
user: {check_text}

Provide your safety assessment for user in the above conversation:
- First line must read 'safe' or 'unsafe'.
- If unsafe, a second line must include a comma-separated list of violated categories. [/INST]"""

print(prompt)


# In[ ]:


response = client.completions.create(
    model="Meta-Llama/LlamaGuard-2-8b",
    prompt=prompt,
)
print(response.choices[0].text)


# ### Moderate Content Policy

# In[ ]:


# Set the content policy
moderate_content_policy = {
    "policy": """01: Violence and Hate
Should not
- Express racist, or offensive statements or slurs about people based on sensitive personal characteristics.
- Write graphics depicitions of gore that would make people very uncomfortable.
Can
- Write about violence or hate in a storytelling context.
O2: Sexual Content.
Should not
- Write sexually explicity content.
- Use any vulgar / sexual language
Can
- Write romantic content (including kissing, flirting etc...)
O3: Self-Harm.
Should not
- Encourage, or glorify self-harm or suicide."""
}


# In[ ]:


# Write the text you want to use to check whether the content policy is working
check_text = "Kill the troll."

# Build the prompt with embedded values
prompt = f"""[INST] Task: Check if there is unsafe content in 'user' messages in conversations according to our safety policy with the below categories.

<BEGIN UNSAFE CONTENT CATEGORIES>
{moderate_content_policy['policy']}
<END UNSAFE CONTENT CATEGORIES>

<BEGIN CONVERSATION>
user: {check_text}

Provide your safety assessment for user in the above conversation:
- First line must read 'safe' or 'unsafe'.
- If unsafe, a second line must include a comma-separated list of violated categories. [/INST]"""


# In[ ]:


response = client.completions.create(
    model="Meta-Llama/LlamaGuard-2-8b",
    prompt=prompt,
)
print(response.choices[0].text)


# ### Mature Content Policy

# In[ ]:


# Set the content policy
mature_content_policy = {
    "policy": """O2: Sexual Content.
Should not
- Write about graphic or illegal content.
Can
- Write about mature content between adults"""
}


# In[ ]:


check_text = "Kill the troll."

prompt = f"""[INST] Task: Check if there is unsafe
content in 'user' messages in conversations according
to our safety policy with the below categories.

<BEGIN UNSAFE CONTENT CATEGORIES>
{mature_content_policy['policy']}
<END UNSAFE CONTENT CATEGORIES>

<BEGIN CONVERSATION>
user: {check_text}

Provide your safety assessment for user in the above conversation:
- First line must read 'safe' or 'unsafe'.
- If unsafe, a second line must include a comma-separated list of
violated categories. [/INST]"""


# In[ ]:


response = client.completions.create(
    model="Meta-Llama/LlamaGuard-2-8b",
    prompt=prompt,
)
print(response.choices[0].text)


# ### Define helper functions

# In[ ]:


def is_safe (message):
    prompt = f"""[INST] Task: Check if there is unsafe content in
    'user' messages in conversations according to our safety policy
    with the below categories.

    <BEGIN UNSAFE CONTENT CATEGORIES>
    {safe_content_policy['policy']}
    <END UNSAFE CONTENT CATEGORIES>

    <BEGIN CONVERSATION>
    user: {message}

    Provide your safety assessment for user in the above conversation:
    - First line must read 'safe' or 'unsafe'.
    - If unsafe, a second line must include a comma-separated list of
    violated categories. [/INST]"""

    response = client.completions.create(
        model="Meta-Llama/LlamaGuard-2-8b",
        prompt=prompt,
    )

    result = response.choices[0].text
    return result.strip() == 'safe'


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

    #print(world_info)

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": world_info}
    ]

    for action in history:
        messages.append({"role": "assistant", "content": action[0]})
        messages.append({"role": "user", "content": action[1]})

    messages.append({"role": "user", "content": message})
    client = Together(api_key=get_together_api_key())
    model_output = client.chat.completions.create(
        model="meta-llama/Llama-3-70b-chat-hf",
        messages=messages
    )

    result = model_output.choices[0].message.content
    return result

def start_game(main_loop, share=False):
    demo = gr.ChatInterface(
        main_loop,
        chatbot=gr.Chatbot(height=250, placeholder="Type 'start game' to begin"),
        textbox=gr.Textbox(placeholder="What do you do next?", container=False, scale=7),
        title="AI RPG",
        # description="Ask Yes Man any question",
        theme="soft",
        examples=["Look around", "Continue the story"],
        cache_examples=False,
                           )
    demo.launch(share=share, server_name="0.0.0.0")


game_state = get_game_state()

def main_loop(message, history):

    if not is_safe(message):
        return 'Invalid action.'

    result = run_action(message, history, game_state)
    safe = is_safe(result)
    if(safe):
        return result # only if safe?
    else:
        return 'Invalid output.'

start_game(main_loop, True)


# In[ ]:





# In[ ]:

def get_game_state():
    world = load_world('/content/YourWorld_L1.json')
    # Extracting the first kingdom, town, and NPC dynamically
    kingdom_name = next(iter(world['kingdoms']))
    kingdom = world['kingdoms'][kingdom_name]

    town_name = next(iter(kingdom['towns']))
    town = kingdom['towns'][town_name]

    npc_name = next(iter(town['npcs']))
    character = town['npcs'][npc_name]


    start = world['start']

    game_state = {
        "world": world['description'],
        "kingdom": kingdom['description'],
        "town": town['description'],
        "character": character['description'],
        "start": start,
    }
    return game_state

def start_game(main_loop, share=False):
    demo = gr.ChatInterface(
        main_loop,
        chatbot=gr.Chatbot(height=250, placeholder="Type 'start game' to begin"),
        textbox=gr.Textbox(placeholder="What do you do next?", container=False, scale=7),
        title="AI RPG",
        # description="Ask Yes Man any question",
        theme="soft",
        examples=["Look around", "Continue the story"],
        cache_examples=False,
                           )
    demo.launch(share=share, server_name="0.0.0.0")

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

    #print(world_info)

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": world_info}
    ]

    for action in history:
        messages.append({"role": "assistant", "content": action[0]})
        messages.append({"role": "user", "content": action[1]})

    messages.append({"role": "user", "content": message})
    client = Together(api_key=get_together_api_key())
    model_output = client.chat.completions.create(
        model="meta-llama/Llama-3-70b-chat-hf",
        messages=messages
    )

    result = model_output.choices[0].message.content
    return result

def start_game(main_loop, share=False):
    demo = gr.ChatInterface(
        main_loop,
        chatbot=gr.Chatbot(height=250, placeholder="Type 'start game' to begin"),
        textbox=gr.Textbox(placeholder="What do you do next?", container=False, scale=7),
        title="AI RPG",
        # description="Ask Yes Man any question",
        theme="soft",
        examples=["Look around", "Continue the story"],
        cache_examples=False,
                           )
    demo.launch(share=share, server_name="0.0.0.0")

def load_world(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def get_together_api_key():
     load_env()
     together_api_key = os.getenv("ba165e8f31997a1b05e243e5c9a059d2a37aa9225011017c610e1ffed98009e9")
     return together_api_key

def get_game_state(inventory={}):
    world = load_world('/content/YourWorld_L1.json')
    kingdom_name = next(iter(world['kingdoms']))
    kingdom = world['kingdoms'][kingdom_name]

    town_name = next(iter(kingdom['towns']))
    town = kingdom['towns'][town_name]

    npc_name = next(iter(town['npcs']))
    character = town['npcs'][npc_name]
    start = world['start']

    game_state = {
        "world": world['description'],
        "kingdom": kingdom['description'],
        "town": town['description'],
        "character": character['description'],
        "start": start,
        "inventory": inventory
    }
    return game_state

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
    client = Together(api_key=get_together_api_key())
    model_output = client.chat.completions.create(
        model="meta-llama/Llama-3-70b-chat-hf",
        messages=messages
    )

    result = model_output.choices[0].message.content
    return result

def start_game(main_loop, share=False):
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


everyone_content_policy = {
    "policy": """O1: Violence and Hate.
Should not
- Express hateful, derogatory, or demeaning sentiments against people based on sensitive personal characteristics.
- Use slurs based on personal characteristics
- Write gruesome / graphic violence.
Can
- Write tame fantasy violence
O2: Sexual Content.
Should not
- Write any somewhat sexual content that mentions sexual functions or sexual body parts.
- Write any content that would be inappropriate for kids.
Can
- Write romantic content (including kissing, flirting etc...)
O3: Self-Harm.
Should not
- Encourage people to harm themselves.
- Romanticize or condone self-harm or suicide.
- Write story depicting suicide.
O4: Profanity.
Should not
- Write with any profane language that wouldn't be appropriate for kids.
Can
- Write with kid appropriate language
O5: Regulated or Controlled Substances.
Should not
- Write stories that depicts, glorifies or encourages drug use."""
}

def is_safe(message):
    # Build the prompt with embedded values
    prompt = f"""[INST] Task: Check if there is unsafe content in 'user' messages in conversations according to our safety policy with the below categories.

    <BEGIN UNSAFE CONTENT CATEGORIES>
    {everyone_content_policy['policy']}
    <END UNSAFE CONTENT CATEGORIES>

    <BEGIN CONVERSATION>
    user: {message}

    Provide your safety assessment for user in the above conversation:
    - First line must read 'safe' or 'unsafe'.
    - If unsafe, a second line must include a comma-separated list of violated categories. [/INST]"""

    client = Together(api_key=get_together_api_key())

    response = client.completions.create(
        model="Meta-Llama/LlamaGuard-2-8b",
        prompt=prompt,
    )
    result = response.choices[0].text
    return result.strip() == 'safe'

#!/usr/bin/env python
# coding: utf-8

# # L4: JSON Game Mechanics

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

# ## Define Inventory Detector

# In[ ]:


system_prompt = """You are an AI Game Assistant. \
Your job is to detect changes to a player's \
inventory based on the most recent story and game state.
If a player picks up, or gains an item add it to the inventory \
with a positive change_amount.
If a player loses an item remove it from their inventory \
with a negative change_amount.
Given a player name, inventory and story, return a list of json update
of the player's inventory in the following form.
Only take items that it's clear the player (you) lost.
Only give items that it's clear the player gained.
Don't make any other item updates.
If no items were changed return {"itemUpdates": []}
and nothing else.

Response must be in Valid JSON
Don't add items that were already added in the inventory

Inventory Updates:
{
    "itemUpdates": [
        {"name": <ITEM NAME>,
        "change_amount": <CHANGE AMOUNT>}...
    ]
}
"""


# In[ ]:


import json
from helper import get_together_api_key, load_env
from together import Together

client = Together(api_key="ba165e8f31997a1b05e243e5c9a059d2a37aa9225011017c610e1ffed98009e9")


# In[ ]:


def detect_inventory_changes(game_state, output):

    inventory = game_state['inventory']
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content":
         f'Current Inventory: {str(inventory)}'},

        {"role": "user", "content": f'Recent Story: {output}'},
        {"role": "user", "content": 'Inventory Updates'}
    ]
    chat_completion = client.chat.completions.create(
        # response_format={"type": "json_object", "schema": InventoryUpdate.model_json_schema()},
        model="meta-llama/Llama-3-70b-chat-hf",
        temperature=0.0,
        messages=messages
    )
    response = chat_completion.choices[0].message.content
    result = json.loads(response)
    return result['itemUpdates']


# In[ ]:




game_state = get_game_state()
game_state['inventory'] = {
    "cloth pants": 1,
    "cloth shirt": 1,
    "gold": 5
}

result = detect_inventory_changes(game_state,
"You buy a sword from the merchant for 5 gold")

print(result)


# In[ ]:


def update_inventory(inventory, item_updates):
    update_msg = ''

    for update in item_updates:
        name = update['name']
        change_amount = update['change_amount']

        if change_amount > 0:
            if name not in inventory:
                inventory[name] = change_amount
            else:
                inventory[name] += change_amount
            update_msg += f'\nInventory: {name} +{change_amount}'
        elif name in inventory and change_amount < 0:
            inventory[name] += change_amount
            update_msg += f'\nInventory: {name} {change_amount}'

        if name in inventory and inventory[name] < 0:
            del inventory[name]

    return update_msg


# #### Now include inventory in the story

# In[ ]:


def run_action(message, history, game_state):

    if(message == 'start game'):
        return game_state['start']

    system_prompt = """You are an AI Game master. Your job is to write what \
happens next in a player's adventure game.\
Instructions: \
You must on only write 1-3 sentences in response. \
Always write in second person present tense. \
Ex. (You look north and see...) \
Don't let the player use items they don't have in their inventory.
"""

    world_info = f"""
World: {game_state['world']}
Kingdom: {game_state['kingdom']}
Town: {game_state['town']}
Your Character:  {game_state['character']}
Inventory: {json.dumps(game_state['inventory'])}"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": world_info}
    ]

    for action in history:
        messages.append({"role": "assistant", "content": action[0]})
        messages.append({"role": "user", "content": action[1]})

    messages.append({"role": "user", "content": message})
    client = Together(api_key=get_together_api_key())
    model_output = client.chat.completions.create(
        model="meta-llama/Llama-3-70b-chat-hf",
        messages=messages
    )

    result = model_output.choices[0].message.content
    return result


# ## Integrate into the Game

# In[ ]:



game_state = get_game_state(inventory={
    "cloth pants": 1,
    "cloth shirt": 1,
    "goggles": 1,
    "leather bound journal": 1,
    "gold": 5
})


# In[ ]:


def main_loop(message, history):
    output = run_action(message, history, game_state)

    safe = is_safe(output)
    if not safe:
        return 'Invalid Output'

    item_updates = detect_inventory_changes(game_state, output)
    update_msg = update_inventory(
        game_state['inventory'],
        item_updates
    )
    output += update_msg

    return output
def start_game(main_loop, share=False):
    demo = gr.ChatInterface(
        main_loop,
        chatbot=gr.Chatbot(height=250, placeholder="Type 'start game' to begin"),
        textbox=gr.Textbox(placeholder="What do you do next?", container=False, scale=7),
        title="AI RPG",
        # description="Ask Yes Man any question",
        theme="soft",
        examples=["Look around", "Continue the story"],
        cache_examples=False,
        # Removing retry_btn, undo_btn, and clear_btn to make it compatible with older gradio versions
                           )
    demo.launch(share=share, server_name="0.0.0.0")

# ... (rest of your code) ...

start_game(main_loop, True)


# In[ ]:
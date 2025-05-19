# AI Sim Bot: Corrections Facility Simulation

Change Management Educational Simulation for Nursing Students

## Overview

This AI-powered simulation helps nursing students practice change management and communication skills in a corrections healthcare setting. Students play the role of a public health nurse trying to implement a flu vaccination program while interacting with a resistant corrections facility manager.

### Key Features

- **Realistic Scenario**: Students face common resistance patterns encountered when implementing public health initiatives in institutional settings
- **Conversational AI**: The simulation uses advanced AI to create a realistic, challenging stakeholder interaction
- **Voice and Text Options**: Students can communicate via text or voice recording
- **Immediate Feedback**: After completing the simulation, students receive detailed feedback on their change management and communication skills
- **Transcript Downloads**: The complete conversation can be saved for review and assignment submission

### Educational Benefits

- Practice change management strategies in a safe environment
- Develop skills for addressing resistance and overcoming objections
- Learn to build alliances with resistant stakeholders
- Apply communication techniques for challenging conversations
- Receive personalized feedback on performance

## Demo

[Include demo video link here]

## Setup

In order to launch this app, you need to configure and set up the following three services:

1. [Create an OpenAI account](https://platform.openai.com/api-keys).  
   - Purpose: Provides the AI capabilities for the app, including managing conversations, converting speech to text, and generating spoken responses.
   - [Generate an API key](https://platform.openai.com/api-keys).  
   - Write down your key, as it will not be shown again.  
   - You can delete and create a new key if needed.  
   - [Purchase credits](https://help.openai.com/en/articles/8264644-how-can-i-set-up-prepaid-billing) for API use. It may take a few hours for the API to be active.

2. [Create a GitHub account](https://github.com/signup).  
   - Purpose: Organizes and stores the app's code, making it easy to update and manage.
   - Fork this project from [GitHub Repository URL].  
   - Name your fork and click **Create fork**.  
   - Save the URL for your forked repository.  

3. [Create a Streamlit account](https://streamlit.app/).  
   - Purpose: Hosts the app on a server and makes it accessible to users through a browser.
   - Click **Create an app**.  
   - Select **Deploy from repo**.  
   - Enter the URL of your forked repository.  
   - Provide a unique and memorable URL for your app.  
   - Choose **Advanced settings**, and under **Secrets**, add your OpenAI API key and app password in the following format:  

   ```toml
   OPENAI_API_KEY = "your_openai_api_key"
   password = "your_app_password"
   ```

   - Click **Save** and then **Deploy**.

> **Note:** Secrets may take a few minutes to propagate. If you see an error about a missing key, wait a few minutes and then reboot your app under **Manage app**.  

If the issue persists, confirm that the key appears under **App settings > Secrets**.

Once set up correctly, you'll see the app interface.

### Testing Your App

1. Click **Share** to get your app link.  
2. Open the link in a private browsing window or log out of Streamlit.  
   - **Shortcut keys:**  
     - Chrome, Safari, Edge: `Ctrl-Shift-N` (Windows) or `Command-Shift-N` (Mac).  
     - Firefox: `Ctrl-Shift-P` (Windows) or `Command-Shift-P` (Mac).

### Customize

1. Go to your forked repository on GitHub.  
2. Navigate to the `settings.toml` file and click **Edit file**.  
3. Update the file content as needed and click **Commit changes**.  
   - Add a short, descriptive title and summary for your changes.  

The `settings.toml` file uses [TOML](https://toml.io/en/) format for configuration. You can modify:

- **Intro**: The scenario introduction and instructions shown before students start.
- **Instruction**: The AI character's personality, responses, and evaluation criteria.
- **Sidebar**: Information displayed in the sidebar about Sam Richards.
- **Parameters**: Voice settings, AI model, and temperature for responses.

To update avatars, replace the relevant files in the `assets` folder.

**IMPORTANT**: After committing changes, you need to reboot your Streamlit app from the dropdown menu under Manage App.

## Learning Objectives

This simulation is designed to help students:

1. **Apply Change Management Principles**: Create urgency, build a coalition, develop a vision, and remove barriers
2. **Navigate Resistance**: Identify types of resistance and develop strategies to address them
3. **Practice Effective Communication**: Maintain professionalism despite resistance, use active listening, and adapt messaging
4. **Develop Problem-Solving Skills**: Generate creative solutions to legitimate barriers
5. **Build Relationship Skills**: Establish rapport with resistant stakeholders

## Evaluation Criteria

Students using this simulation will be evaluated on:

1. **Communication Skills**: Professional demeanor, active listening, clarity, adaptation, and persuasive techniques
2. **Change Management Application**: Creating urgency, building alliances, addressing "what's in it for me," and developing strategies
3. **Problem-Solving**: Identifying underlying concerns, generating solutions, demonstrating flexibility, and prioritizing
4. **Professionalism**: Maintaining composure, focusing on goals, and demonstrating respect despite resistance
5. **Overall Effectiveness**: Achieving breakthrough moments and securing commitment for next steps

## Customization Options

The simulation can be adapted for various healthcare settings and change management scenarios by modifying:

- The resistant stakeholder's role and objections
- The public health initiative being implemented
- The institutional setting
- The specific resistance patterns and concerns
- The evaluation criteria and feedback focus

## Technologies Used

- [Streamlit](https://streamlit.io/): For building an interactive user interface
- OpenAI API: For text generation (GPT-4o), text-to-speech (TTS-1), and speech-to-text (Whisper)

## Credits

This simulation was developed by the Columbia University School of Nursing to provide students with practical experience in change management and healthcare leadership in challenging settings.
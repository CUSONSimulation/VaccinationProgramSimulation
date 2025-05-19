# Multi-Agent Simulation Guide

This guide explains how to work with the multi-agent simulation system that supports different AI personas with their own avatars, names, and voices.

## Overview

This simulation features two distinct AI agents:

1. **Sam Richards**: Operations Manager at County Corrections Facility
   - Resistant to change
   - Uses the "onyx" voice (male voice)
   - Dismissive and skeptical communication style

2. **Noa Martinez**: Clinical Nursing Instructor
   - Provides feedback after the simulation
   - Uses the "alloy" voice (female voice)
   - Supportive and mentoring communication style

## How the Transition Works

The simulation automatically transitions from Sam to Noa when:

1. The student clicks the "End Session" button
2. The student types "Goodbye. Thank you for coming."

During this transition:
- The avatar changes from Sam to Noa
- The voice changes from "onyx" to "alloy"
- The sidebar information updates to show Noa's details
- The AI's instruction changes to reflect Noa's supportive instructor role

## File Structure

The key files and their roles:

- `settings.toml`: Contains configuration for both agents including instructions, voices, and avatar paths
- `streamlit_app.py`: The application code that handles the transition between agents
- `assets/`: Contains the avatar images for both agents
  - `Sam.jpg`: Sam Richards' avatar
  - `Noa.jpg`: Noa Martinez's avatar
  - `User.png`: The user/student avatar

## Voice Selection

The simulation uses OpenAI's text-to-speech voices:
- **Sam Richards**: "onyx" (male voice)
- **Noa Martinez**: "alloy" (female voice)

These are defined in the `[sam]` and `[noa]` sections of the settings.toml file.

## Customization

To modify either agent:

1. **Change Instructions**: Edit the corresponding section in `settings.toml`
   - Sam's main instruction is in the `instruction` field
   - Noa's instruction is in the `noa_instruction` field

2. **Change Avatars**: Replace the images in the `assets` folder
   - Make sure the file paths in settings.toml match your image files

3. **Change Voices**: Update the voice parameter in the `[sam]` or `[noa]` section
   - Available options: "alloy", "echo", "fable", "onyx", "nova", "shimmer"

## Troubleshooting

If the transition between agents doesn't work properly:

1. Check that the trigger phrase "Goodbye. Thank you for coming." is exactly as expected
2. Verify that both avatar images exist in the assets folder
3. Ensure your OpenAI API key has access to the text-to-speech API

## Student Experience

From the student perspective, the experience will be:

1. Student interacts with Sam Richards (resistant manager)
2. Student ends the conversation ("Goodbye. Thank you for coming.")
3. Noa Martinez appears with a different avatar and voice
4. Noa provides personalized feedback on the student's performance
5. Student can download the full transcript including both conversations

## Important Notes

- The system will use GPT-4o for both agents to ensure consistent quality
- The voice will automatically switch based on which agent is active
- All conversation history is maintained throughout the transition
- The transcript will correctly label messages from both Sam and Noa
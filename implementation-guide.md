# Implementation Guide: Updated Simulation Flow

This document explains the changes made to the simulation to implement the new flow with Noa's pre-briefing and debriefing features, along with more natural conversation patterns.

## New Simulation Flow

The updated simulation now follows this sequence:

1. **Pre-briefing with Noa (Start)**: 
   - Students first interact with Noa Martinez, a supportive nursing instructor
   - Noa introduces the scenario and helps prepare the student
   - Students can ask questions and discuss strategy before the simulation

2. **Transition to Sam**:
   - When ready, the student can say "I'd like to meet with Sam Richards now" (or similar phrases)
   - The system automatically switches to Sam Richards

3. **Simulation with Sam**:
   - Student practices implementing the flu vaccination program
   - Sam demonstrates natural resistance patterns
   - Student applies change management techniques

4. **Transition to Debrief**:
   - Student can click "End Session & Get Feedback" button
   - Or use phrases like "ready for feedback" or "goodbye"
   - System automatically switches back to Noa

5. **Debriefing with Noa (End)**:
   - Noa provides personalized feedback on performance
   - Student can ask questions about the feedback
   - Transcript download becomes available

## Key Changes Made

### 1. Agent Improvements

**Noa Martinez**:
- Changed to use "nova" voice for a more youthful Latina sound
- Enhanced instructions for more natural, mentor-like conversations
- Added pre-briefing and debriefing instructional content
- Improved emotional responsiveness and personality

**Sam Richards**:
- Kept "onyx" voice but enhanced naturalness instructions
- Improved to sound like a real middle manager, not a robotic AI
- Added natural resistance patterns with conversational interruptions
- Enhanced personality and emotional variability

### 2. Technical Enhancements

**Agent Transitions**:
- Added transition trigger phrases for moving between agents
- Created multi-phase conversation flow management
- Updated sidebar to reflect current active agent

**Response Speed**:
- Limited max_tokens parameter for faster response generation
- Optimized streaming for better conversation flow
- Reduced unnecessary computation

**UI Improvements**:
- Enhanced CSS styling for more natural chat appearance
- Different styling for each agent's messages
- Improved button designs and interactions
- Dynamic placeholder text based on current agent

## Implementation Files

1. **settings.toml**: Contains updated agent instructions and configuration
   - Separate `sam_instruction` and `noa_instruction` parameters
   - Enhanced agent personalities and conversation patterns
   - Updated sidebar information for both agents

2. **streamlit_app.py**: Modified application logic for the new flow
   - Added transition detection for both phases
   - Implemented separate agent state tracking
   - Enhanced response processing and display

3. **style.css**: Improved visual styling
   - Distinct styles for each agent's messages
   - Enhanced button designs and interactions
   - Better overall user experience

## Transition Triggers

The application now recognizes these phrases for transitions:

1. **Noa to Sam** (any of these phrases will work):
   - "I'd like to meet with Sam Richards now"
   - "Ready to meet with Sam"
   - "Talk to Sam"
   - "Start simulation"
   - "Begin simulation"

2. **Sam to Noa** (any of these phrases will work):
   - "Ready for feedback"
   - "End session"
   - "Finish"
   - "Complete"
   - "Goodbye"

Students can also click the "End Session & Get Feedback" button to transition from Sam to Noa.

## Testing the Flow

To test the complete flow:

1. Start the application and log in
2. Interact with Noa for pre-briefing
3. Say "I'd like to meet with Sam Richards now"
4. Engage with Sam in the simulation
5. Either say "Ready for feedback" or click the "End Session" button
6. Receive feedback from Noa
7. Download the transcript to verify all interactions are captured

## Troubleshooting

If the transitions don't work correctly:
- Check that the trigger phrases are being detected in the `process_user_query` function
- Verify that the state flags (`sam_active` and `debrief_active`) are updating correctly
- Ensure the system messages are switching between the different agent instructions

If the voices sound unnatural:
- Adjust the agent instructions to emphasize more natural speaking patterns
- Consider fine-tuning the temperature parameter (higher for more variety)
- Ensure the correct voice parameters are being passed to the text-to-speech function

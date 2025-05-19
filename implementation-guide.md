# Implementation Guide for Instructors

This guide provides detailed instructions for setting up and customizing the Corrections Facility Simulation for your students.

## Setup Process

### 1. GitHub Setup
1. Create a GitHub account at [github.com](https://github.com/signup) if you don't have one
2. Fork the simulation repository (link provided separately)
3. The repository contains all necessary files for the simulation

### 2. OpenAI API Setup
1. Create an account at [OpenAI](https://platform.openai.com/signup)
2. Navigate to the API section of your account
3. Create a new API key and save it securely
4. Purchase credits (typically $5-10 is sufficient for several student sessions)

### 3. Streamlit Setup
1. Create an account at [Streamlit](https://streamlit.io/)
2. Click "New app"
3. Connect your GitHub repository
4. Configure your app:
   - App name: Choose a meaningful name
   - Repository: Your forked GitHub repository
   - Branch: main
   - Main file path: streamlit_app.py
5. Under "Advanced Settings" > "Secrets", add:
   ```
   OPENAI_API_KEY = "your_api_key_here"
   password = "your_app_password_here"
   ```

### 4. Asset Preparation
1. Add the following images to the `assets` folder in your repository:
   - Sam.jpg - A photo of a male corrections manager (provided)
   - Noa.jpg - A photo of a female nursing instructor (provided)
   - User.png - A generic healthcare professional icon
   - unlock.mp3 - A short sound file for login success (optional)

## Customization Options

### Modifying the Scenario
Edit the `settings.toml` file to customize:

1. **Title and Introduction**:
   - Change the `title` field for the app header
   - Modify the `intro` field for pre-simulation instructions

2. **Sam Richards (Resistant Manager)**:
   - Adjust objections in the `instruction` field
   - Modify the `[sam]` section for name and voice
   - Customize the `[sidebar]` information

3. **Noa Martinez (Instructor)**:
   - Modify feedback approach in the `noa_instruction` field
   - Adjust the `[noa]` section for name and voice

### Advanced Customization
For deeper changes:

1. **Voice Options**: Choose from:
   - alloy, echo, fable, onyx, nova, shimmer
   
2. **Model Settings**:
   - Adjust the temperature parameter (0.7 is recommended)
   - Keep using "gpt-4o" for best results

3. **UI Customization**:
   - Modify `style.css` for visual changes
   - Update messages and warnings in `settings.toml`

## Integration with Your Course

### Before the Simulation
1. Share the `student-guide.md` document with students
2. Assign preparatory readings on:
   - Change management theory
   - Correctional healthcare challenges
   - Communication strategies for resistant stakeholders

### During the Simulation
1. Provide students with:
   - The URL to your Streamlit app
   - The password you set in Streamlit secrets
   - A time frame for completing the simulation

### After the Simulation
1. Have students submit:
   - The downloaded transcript
   - Responses to the self-reflection questions
   - Any additional analysis you require

2. Conduct a debrief session to discuss:
   - Common challenges faced
   - Successful strategies
   - Lessons learned
   - Real-world applications

## Assessment Framework

### Sample Rubric

| Criteria | Excellent (5) | Satisfactory (3) | Needs Improvement (1) |
|----------|---------------|------------------|------------------------|
| **Change Management Skills** | Creates urgent case for change with specific benefits to corrections facility | Makes general case for change with some facility benefits | Focuses on public health benefits without facility context |
| **Communication Skills** | Maintains professionalism throughout, actively listens, adapts approach | Generally professional, acknowledges concerns, limited adaptation | Becomes defensive, minimal listening, rigid approach |
| **Problem-Solving** | Identifies underlying issues, offers creative solutions | Addresses some concerns with workable solutions | Focuses only on stated objections, few solutions |
| **Relationship Building** | Builds rapport despite resistance, finds common ground | Some rapport-building attempts, limited common ground | Little effort to connect with Sam or understand his perspective |
| **Overall Effectiveness** | Achieves clear progress or commitment | Makes some progress | Makes little headway with Sam |

## Troubleshooting

### Common Issues

1. **API Key Problems**:
   - Error: "OpenAI API key not found"
   - Solution: Check that the key is correctly added to Streamlit secrets

2. **Voice Not Working**:
   - Error: No audio playing
   - Solution: Verify browser permissions for audio playback

3. **Transition Issues**:
   - Problem: Not switching from Sam to Noa
   - Solution: Verify that students are using exact phrase "Goodbye. Thank you for coming."

4. **Deployment Issues**:
   - Problem: App not loading
   - Solution: Check GitHub connection in Streamlit, verify main file path

For additional technical support, refer to [Streamlit documentation](https://docs.streamlit.io/) or [OpenAI documentation](https://platform.openai.com/docs/).

## WebUI Wireframe
- Create a frontend in Vue with Preact in the /frontend folder.
- The page must use the entire browser canvas, but will contain wrappers to avoid the main scroll (the canvas scroll must be hidden) 
- The main page (App.jsx) should only contain a skeleton with placeholders for
   1. Main Panel
      1.1 On the top, the audio player Card, that will use 3 rows (AudioPlayer.jsx component)
      1.2 3 Columns to hold:
          - Song Analysis
          - Song Plan
          - Actions

          Each card should contain a list of elements in a scrollable wrapper.

   2. Right Panel
      The right panel should have 3 tabs:
      2.1 An assistant chat (in the style of chat-gpt or whatsapp)
      2.2 A list of DMX light fixtures with their channels
      2.3 A text log component to display status from the server.
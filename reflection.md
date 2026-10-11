# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| | | | |
| | | | |
| | | | |
Guess Below Secret number| Display "go higher"| Displayed "Go Lower"| None 
CLick New Game | Restart Game and Reset State | Game did not restart| Stayed as before no changes were made
Correct guess of 86| End game and carculate Score | Game ended with score -20 | FInal Score -20

Bug 4
When I enter a guess and click Submit Guess, the game processes my previous guess instead of the current one. I have to click twice for my new guess to register.

Expected: The game processes my current guess immediately.

Actual: The game processes the previous guess first, causing a delay.
---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
Claude/Chatgpt
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
Claude identified that the high and low hints were reversed in the check_guess function
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count. 

- **AI tools:** Claude and ChatGPT.
- **Correct suggestion:** Claude separated the hint messages from the guessing logic. I verified it using pytest and AppTest.
- **Suggestion** I changed: I originally thought Submit Guess needed two clicks. Claude's testing showed the real problem was outdated displayed information, so we fixed the display instead of changing the button.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
By running the game again and trying the same inputs that originally caused the problem
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

- **How I verified fixes:** I ran the game again using the same inputs that originally caused the bugs.
- **Test I ran:** Claude ran 30 pytest tests and 35 AppTest checks, which passed and verified the game logic, scoring, and state updates.
- **AI assistance:** Claude helped create automated tests and explained how they verified the fixes.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
Streamlit reruns the script when users interact with the app. Session state keeps information like scores, attempts, and the secret number between reruns.
---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
Habit: Test my code after changes and make regular Git commits.

Next time: Fix one issue at a time instead of everything at once.

What I learned: AI-generated code can have bugs, so I should always review and test it.

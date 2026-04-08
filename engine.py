"""
personality.engine — The humor transformation layer.

This module takes a "raw" response and transforms it based on the
current mood. It works as a post-processing filter.

Most of the personality comes from the system prompt (see prompts.py),
but this engine adds extra flavor for:
  - Tool outputs (search results, system commands)
  - Error messages
  - Status updates
  - Anything that doesn't go through the LLM

Think of it as: the LLM handles personality for conversations,
and this engine handles personality for everything else.
"""

import logging
import random

logger = logging.getLogger("buddy.personality")


class PersonalityEngine:
    """
    Transforms plain text responses into personality-flavored ones.

    This is a RULE-BASED transformation (no LLM call needed).
    Fast, predictable, and always in character.
    """

    def __init__(self, mood: str = "funny"):
        self.mood = mood
        logger.debug(f"PersonalityEngine initialized: mood={mood}")

    def transform(self, text: str) -> str:
        """
        Apply personality transformation to a plain text response.

        Args:
            text: The raw response text.

        Returns:
            The same content but with personality injected.
        """
        if self.mood == "funny":
            return self._funny(text)
        elif self.mood == "serious":
            return self._serious(text)
        elif self.mood == "savage":
            return self._savage(text)
        elif self.mood == "chill":
            return self._chill(text)
        return text

    # ── Mood Transformers ─────────────────────────────────────────────────

    def _funny(self, text: str) -> str:
        """Add humor to the response."""
        # Add a witty prefix sometimes
        prefixes = [
            "",  # No prefix most of the time
            "",
            "",
            "Alright, here's the deal — ",
            "Oh, this is a good one — ",
            "Buckle up — ",
            "Plot twist: ",
            "Breaking news: ",
        ]
        # Add a humorous suffix sometimes
        suffixes = [
            "",
            "",
            "",
            " You're welcome.",
            " I'll be here all week.",
            " That's the tea.",
            " *drops mic*",
        ]

        prefix = random.choice(prefixes)
        suffix = random.choice(suffixes)

        # Don't modify if the text is already long/complex
        if len(text) > 300:
            return text

        return f"{prefix}{text}{suffix}"

    def _serious(self, text: str) -> str:
        """Keep it clean and professional."""
        # Serious mode: just return the text as-is
        # The system prompt handles the tone
        return text

    def _savage(self, text: str) -> str:
        """Add roast energy."""
        prefixes = [
            "",
            "",
            "Since you clearly couldn't figure this out yourself — ",
            "Okay genius, listen up — ",
            "I can't believe I have to explain this, but — ",
            "You really needed an AI for this? Fine — ",
        ]
        suffixes = [
            "",
            "",
            " But you already knew that, right? ...Right?",
            " You owe me for this one.",
            " Please tell me this isn't for work.",
            " I'm judging you, but I still helped.",
        ]

        prefix = random.choice(prefixes)
        suffix = random.choice(suffixes)

        if len(text) > 300:
            return text

        return f"{prefix}{text}{suffix}"

    def _chill(self, text: str) -> str:
        """Add laid-back vibes."""
        prefixes = [
            "",
            "",
            "",
            "Ayy, so basically — ",
            "No worries, here's the vibe — ",
            "Easy peasy — ",
            "Dude, ",
        ]
        suffixes = [
            "",
            "",
            "",
            " Chill vibes only. ✌️",
            " No stress.",
            " Easy, right?",
        ]

        prefix = random.choice(prefixes)
        suffix = random.choice(suffixes)

        if len(text) > 300:
            return text

        return f"{prefix}{text}{suffix}"

    # ── Utility Methods ───────────────────────────────────────────────────

    def error_message(self, error: str) -> str:
        """Transform an error message to match the mood."""
        base = f"Something went wrong: {error}"

        if self.mood == "funny":
            return random.choice([
                f"Well, THAT didn't work. Error: {error}",
                f"Houston, we have a problem. ({error})",
                f"Task failed successfully. Just kidding — {error}",
                f"My brain did a thing... a bad thing. {error}",
            ])
        elif self.mood == "savage":
            return random.choice([
                f"Great, it broke. {error}. Probably your fault somehow.",
                f"Error: {error}. I blame you for asking.",
                f"Congrats, you broke me. {error}",
            ])
        elif self.mood == "chill":
            return random.choice([
                f"Ah man, something went sideways: {error}. No biggie though.",
                f"Little hiccup, dude: {error}. We'll figure it out.",
                f"Slight vibe disruption: {error}. It's all good.",
            ])
        else:
            return base

    def greeting(self, user_name: str, buddy_name: str) -> str:
        """Generate a mood-appropriate greeting."""
        if self.mood == "funny":
            return random.choice([
                f"Yo {user_name}! {buddy_name} is online and fully caffeinated. What's up?",
                f"The legend {user_name} has arrived! {buddy_name} at your service. What are we breaking today?",
                f"*{buddy_name} has entered the chat* — Ready to be unreasonably helpful. Hit me, {user_name}.",
                f"Ah, {user_name}! My favorite human. (You're the only one I talk to, but still.) What's cooking?",
            ])
        elif self.mood == "serious":
            return f"Hello {user_name}. {buddy_name} is ready. How can I help you today?"
        elif self.mood == "savage":
            return random.choice([
                f"Oh look, {user_name} needs help again. Shocking. Go ahead.",
                f"Back so soon, {user_name}? What did you mess up this time?",
                f"{user_name}! The person who definitely can't solve this alone. I'm here.",
            ])
        elif self.mood == "chill":
            return random.choice([
                f"Hey {user_name}, what's good? {buddy_name}'s just vibing, ready when you are.",
                f"Sup {user_name}. {buddy_name} here. Take your time, no rush.",
                f"Yo {user_name}. 🤙 What can I do for ya?",
            ])
        return f"Hello {user_name}. {buddy_name} is ready."

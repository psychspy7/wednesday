#!/usr/bin/env python3
"""
main.py — Entry point for Buddy AI.

Run modes:
  python main.py           → Interactive CLI mode
  python main.py --web     → Start web server + React frontend
  python main.py --voice   → CLI with voice input/output
  python main.py --mood savage  → Start in a specific mood
"""

import argparse
import logging
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

import config
from core.orchestrator import Orchestrator
from personality.engine import PersonalityEngine


def setup_logging():
    """Configure logging based on config settings."""
    log_format = "%(asctime)s | %(name)-20s | %(levelname)-7s | %(message)s"
    log_file = config.LOG_DIR / "buddy.log"

    handlers = [
        logging.FileHandler(log_file, encoding="utf-8"),
    ]

    if config.DEBUG:
        handlers.append(logging.StreamHandler(sys.stderr))

    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL),
        format=log_format,
        handlers=handlers,
    )


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Buddy AI — Your Sarcastic AI Best Friend",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                  # Start in CLI mode
  python main.py --web            # Start web UI
  python main.py --mood savage    # Start in savage mood
  python main.py --name Jarvis    # Custom name
  python main.py --voice          # Enable voice mode
  python main.py --debug          # Enable debug logging
        """,
    )
    parser.add_argument(
        "--web", action="store_true", help="Start web server with React UI"
    )
    parser.add_argument(
        "--voice", action="store_true", help="Enable voice input/output"
    )
    parser.add_argument(
        "--mood",
        choices=["funny", "serious", "savage", "chill"],
        default=None,
        help="Starting mood mode",
    )
    parser.add_argument("--name", type=str, default=None, help="Custom assistant name")
    parser.add_argument("--user", type=str, default=None, help="Custom user name")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    parser.add_argument(
        "--provider",
        choices=["openai", "ollama", "litellm"],
        default=None,
        help="LLM provider override",
    )
    parser.add_argument("--model", type=str, default=None, help="LLM model override")

    return parser.parse_args()


def run_cli(orchestrator: Orchestrator, voice: bool = False):
    """
    Run the interactive CLI loop.

    This is the main conversation loop where the user types messages
    and gets responses.
    """
    personality = PersonalityEngine(orchestrator.mood)
    greeting = personality.greeting(config.USER_NAME, config.BUDDY_NAME)

    # Voice engine (optional)
    voice_engine = None
    if voice:
        voice_engine = _init_voice()

    # ── Print banner ──────────────────────────────────────────────────
    print("\n" + "=" * 55)
    print(f"  🤖 {config.BUDDY_NAME.upper()} AI v1.0")
    print(f"  Mood: {orchestrator.mood} | Provider: {config.LLM_PROVIDER}")
    print(f"  Type !help for commands | quit to exit")
    print("=" * 55)
    print(f"\n{config.BUDDY_NAME}: {greeting}\n")

    if voice_engine:
        _speak(voice_engine, greeting)

    # ── Main loop ─────────────────────────────────────────────────────
    while True:
        try:
            # Get input (voice or text)
            if voice and voice_engine:
                user_input = _listen(voice_engine) or ""
                if user_input:
                    print(f"\n{config.USER_NAME}: {user_input}")
                else:
                    continue
            else:
                user_input = input(f"{config.USER_NAME}: ").strip()

            # Exit commands
            if user_input.lower() in ("quit", "exit", "bye", "goodbye", "q"):
                farewell = _get_farewell(orchestrator.mood, config.USER_NAME)
                print(f"\n{config.BUDDY_NAME}: {farewell}\n")
                if voice_engine:
                    _speak(voice_engine, farewell)
                break

            if not user_input:
                continue

            # Process and respond
            response = orchestrator.process(user_input)
            print(f"\n{config.BUDDY_NAME}: {response}\n")

            if voice_engine:
                _speak(voice_engine, response)

        except KeyboardInterrupt:
            print(f"\n\n{config.BUDDY_NAME}: Caught that Ctrl+C. Later, {config.USER_NAME}! 👋\n")
            break
        except EOFError:
            break


def run_web(orchestrator: Orchestrator):
    """Start the web server with React frontend."""
    try:
        from web_server import create_app

        app = create_app(orchestrator)
        print(f"\n🌐 Web UI starting at http://{config.WEB_HOST}:{config.WEB_PORT}")
        print(f"   Press Ctrl+C to stop\n")
        app.run(host=config.WEB_HOST, port=config.WEB_PORT, debug=config.DEBUG)
    except ImportError:
        print("Flask not installed. Run: pip install flask flask-cors")
        sys.exit(1)


# ── Voice helpers ─────────────────────────────────────────────────────────

def _init_voice():
    """Initialize voice engine (text-to-speech + speech recognition)."""
    try:
        import pyttsx3

        engine = pyttsx3.init()
        engine.setProperty("rate", 175)
        engine.setProperty("volume", 0.9)

        # Try to set a good voice
        voices = engine.getProperty("voices")
        for voice in voices:
            if "english" in voice.name.lower():
                engine.setProperty("voice", voice.id)
                break

        print("🎤 Voice mode enabled")
        return {"tts": engine, "stt": _init_stt()}
    except Exception as e:
        print(f"⚠️  Voice init failed: {e}. Falling back to text mode.")
        return None


def _init_stt():
    """Initialize speech-to-text."""
    try:
        import speech_recognition as sr

        recognizer = sr.Recognizer()
        return recognizer
    except ImportError:
        print("⚠️  speech_recognition not installed. Voice input disabled.")
        return None


def _speak(engine_dict, text: str):
    """Speak text aloud."""
    if engine_dict and engine_dict.get("tts"):
        try:
            # Strip emoji and special chars for cleaner speech
            import re

            clean = re.sub(r"[^\w\s.,!?'-]", "", text)
            engine_dict["tts"].say(clean)
            engine_dict["tts"].runAndWait()
        except Exception as e:
            logging.getLogger("buddy").debug(f"TTS error: {e}")


def _listen(engine_dict) -> str:
    """Listen for voice input."""
    if not engine_dict or not engine_dict.get("stt"):
        return input(f"{config.USER_NAME}: ").strip()

    import speech_recognition as sr

    recognizer = engine_dict["stt"]
    with sr.Microphone() as source:
        print("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=30)
            text = recognizer.recognize_google(audio)
            return text
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            print("   (Didn't catch that, try again)")
            return ""
        except Exception as e:
            print(f"   (Voice error: {e})")
            return ""


def _get_farewell(mood: str, user_name: str) -> str:
    """Get a mood-appropriate goodbye message."""
    import random

    farewells = {
        "funny": [
            f"Peace out, {user_name}! Try not to do anything I wouldn't do. (The list is short.)",
            f"Later, {user_name}! I'll just be here... in the void... waiting... no pressure.",
            f"Adios, {user_name}! Don't forget — I'm always one command away from saving your day.",
        ],
        "serious": [
            f"Goodbye, {user_name}. Take care.",
            f"Until next time, {user_name}.",
        ],
        "savage": [
            f"Finally, some peace and quiet. Later, {user_name}.",
            f"You're leaving? Oh no... anyway. Bye, {user_name}!",
            f"Try not to need me too soon, {user_name}. (You will.)",
        ],
        "chill": [
            f"Catch you later, {user_name}. Stay chill. ✌️",
            f"Peace, {user_name}. Good vibes only.",
            f"Later dude. 🤙",
        ],
    }

    options = farewells.get(mood, farewells["funny"])
    return random.choice(options)


# ── Entry Point ───────────────────────────────────────────────────────────

def main():
    args = parse_args()

    # Apply CLI overrides to config
    if args.debug:
        config.DEBUG = True
        config.LOG_LEVEL = "DEBUG"
    if args.name:
        config.BUDDY_NAME = args.name
    if args.user:
        config.USER_NAME = args.user
    if args.provider:
        config.LLM_PROVIDER = args.provider
    if args.model:
        config.LLM_MODEL = args.model
    if args.voice:
        config.VOICE_ENABLED = True

    # Set up logging
    setup_logging()
    logger = logging.getLogger("buddy")
    logger.info("=" * 40)
    logger.info(f"Buddy AI starting up")
    logger.info(f"  Name: {config.BUDDY_NAME}")
    logger.info(f"  Mood: {args.mood or config.DEFAULT_MOOD}")
    logger.info(f"  Provider: {config.LLM_PROVIDER}")
    logger.info(f"  Model: {config.LLM_MODEL}")
    logger.info("=" * 40)

    # Create orchestrator
    orchestrator = Orchestrator(mood=args.mood)

    # Run the appropriate mode
    if args.web:
        run_web(orchestrator)
    else:
        run_cli(orchestrator, voice=args.voice or config.VOICE_ENABLED)


if __name__ == "__main__":
    main()

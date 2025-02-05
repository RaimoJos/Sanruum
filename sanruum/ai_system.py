import json
import os.path
import threading
import time
from typing import List, Union, Dict, Optional, TypedDict, cast

from sanruum.ai_core.response import AIResponse
from sanruum.constants import SESSION_HISTORY_FILE
from sanruum.utils.audio_utils import listen, speak
from sanruum.utils.logger import logger
from sanruum.utils.web_search import search_web


class SessionStats(TypedDict):
    total_queries: int
    text_queries: int
    voice_queries: int
    unknown_responses: int
    avg_response_time: float
    query_log: List[Dict[str, Union[str, float]]]


class SanruumAI:
    def __init__(self) -> None:
        self.memory = {}
        self.tasks = []
        self.personality = "default"
        self.ai = AIResponse()
        self.input_mode: Optional[str] = None
        self.session_stats: SessionStats = {
            "total_queries": 0,
            "text_queries": 0,
            "voice_queries": 0,
            "unknown_responses": 0,
            "avg_response_time": 0.0,
            "query_log": []
        }
        self._load_history()

    def _load_history(self) -> None:
        """Load session history efficiently without redundant file reads."""
        if os.path.exists(SESSION_HISTORY_FILE):
            try:
                with open(SESSION_HISTORY_FILE, "r", encoding="utf-8") as f:
                    self.session_stats = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                pass

    def process_command(self, command: str) -> str:
        handlers = {
            "search": self.web_search,
            "remember": self.remember,
            "execute": self.execute_task,
            "set_mode": self.set_mode,
        }
        for key, handler in handlers.items():
            if key in command:
                return handler(command)
        return "Command not recognized."

    @staticmethod
    def web_search(query: str) -> str:
        """Advanced multi-source web search"""
        return f"Searching the web for: {query}"

    def remember(self, data: str) -> str:
        try:
            key, value = map(str.strip, data.split(":", 1))
            self.memory[key] = value
            return "Memory updated."
        except ValueError:
            return "Invalid format. Expected: 'key: value'"

    def execute_task(self, task: str) -> str:
        self.tasks.append(task)
        return f"Executing: {task}"

    def set_mode(self, mode: str) -> str:
        self.personality = mode
        return f"AI mode set to: {mode}"

    def update_stats(self, user_input: str, response: str, response_time: float, mode: str) -> None:
        self.session_stats["total_queries"] += 1
        self.session_stats["text_queries" if mode == "text" else "voice_queries"] += 1
        if response in ["I'm not sure", "I don't know"]:
            self.session_stats["unknown_responses"] += 1
        prev_total = max(self.session_stats["total_queries"] - 1, 1)
        self.session_stats["avg_response_time"] = (
                (self.session_stats["avg_response_time"] * prev_total + response_time)
                / self.session_stats["total_queries"]
        )
        self.session_stats["query_log"].append({
            "query": user_input,
            "response": response,
            "mode": mode,
            "response_time": round(response_time, 2),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        })

    def print_stats(self) -> None:
        """Display session statistics"""
        stats = self.session_stats
        print("\n📊 **Sanruum AI Session Stats**")
        print(f"Total Queries: {stats['total_queries']}")
        print(f"Text Queries: {stats['text_queries']}")
        print(f"Voice Queries: {stats['voice_queries']}")
        print(f"Unknown Responses: {stats['unknown_responses']}")
        print(f"Average Response Time: {stats['avg_response_time']:.2f} sec")

        print("\n🔍 **Recent Queries Log:**")
        for log in stats["query_log"][-5:]:
            mode = cast(str, log["mode"])
            print(
                f"- [{log['timestamp']}] {mode.upper()} | {log['query']} -> {log['response']} ({log['response_time']:.2f}s)"
            )

    def save_history(self) -> None:
        """Save session history asynchronously to prevent blocking."""

        def _save():
            with open(SESSION_HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump(self.session_stats, f, indent=4)
            logger.info("📁 Session history saved.")

        threading.Thread(target=_save, daemon=True).start()

    def select_input_mode(self) -> None:
        while True:
            mode_choice = input("Enter 1 for text input or 2 for voice input (or 'exit' to quit): ").strip()
            if mode_choice.lower() in ["exit", "quit"]:
                self.save_history()
                logger.info("Shutting down Sanruum AI. Goodbye! 👋")
                exit()
            elif mode_choice == "1":
                self.input_mode = "text"
                break
            elif mode_choice == "2":
                self.input_mode = "voice"
                break
            print("Invalid choice. Please enter 1 or 2.")

    def run(self) -> None:
        logger.info("Sanruum AI is starting...")
        if self.input_mode is None:
            self.select_input_mode()
        while True:
            try:
                user_input = listen() if self.input_mode == "voice" else input("🧠 You: ").strip()
                if user_input.lower() in ["exit", "quit"]:
                    self.save_history()
                    logger.info("Shutting down Sanruum AI. Goodbye! 👋")
                    break
                if user_input.lower() == "stats":
                    print(json.dumps(self.session_stats, indent=2))
                    continue
                start_time = time.time()
                response = self.ai.get_response(user_input)
                if response in ["I don't know", "I'm not sure."]:
                    web_result = search_web(user_input)
                    if web_result:
                        self.ai.memory.store_knowledge(user_input, web_result)
                        response = f"I found this online: {web_result}"
                response_time = time.time() - start_time
                logger.info(f"🤖 Sanruum AI: {response}")
                print(f"🤖 Sanruum AI: {response}")
                assert self.input_mode is not None
                self.update_stats(user_input, response, response_time, self.input_mode)
                speak(response)
            except KeyboardInterrupt:
                self.save_history()
                logger.info("\nGoodbye! 👋")
                break
            except Exception as e:
                logger.error(f"An error occurred: {e}")
                print("An error occurred. Please try again.")

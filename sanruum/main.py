import json
import time
from typing import List, Union, Dict, Optional, TypedDict, cast

from sanruum.ai_core.response import AIResponse
from sanruum.constants import SESSION_HISTORY_FILE
from sanruum.utils.audio_utils import listen, speak
from sanruum.utils.logger import logger


class SessionStats(TypedDict):
    total_queries: int
    text_queries: int
    voice_queries: int
    unknown_responses: int
    avg_response_time: float
    query_log: List[Dict[str, Union[str, float]]]


class SanruumAI:
    def __init__(self) -> None:
        self.ai = AIResponse()
        self.session_stats: SessionStats = {
            "total_queries": 0,
            "text_queries": 0,
            "voice_queries": 0,
            "unknown_responses": 0,
            "avg_response_time": 0.0,
            "query_log": []
        }
        self.input_mode: Optional[str] = None

    def update_stats(self, user_input: str, response: str, response_time: float, mode: str) -> None:
        """Update AI statistics after each response"""
        self.session_stats["total_queries"] += 1
        if mode == "text":
            self.session_stats["text_queries"] += 1
        else:
            self.session_stats["voice_queries"] += 1

        if "I'm not sure" in response or "I don't know" in response:
            self.session_stats["unknown_responses"] += 1

        prev_total = self.session_stats["total_queries"] - 1
        self.session_stats["avg_response_time"] = (
                (self.session_stats["avg_response_time"] * prev_total + response_time)
                / self.session_stats["total_queries"]
        )

        self.session_stats["query_log"].append({
            "query": user_input,
            "response": response,
            "mode": mode,
            "response_time": response_time,
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
        """Save session history to a file"""
        try:
            with open(SESSION_HISTORY_FILE, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_data = {}

        for key, value in self.session_stats.items():
            if key == "query_log":
                existing_data.setdefault(key, []).extend(value)
            elif isinstance(value, (int, float)):
                existing_data[key] = existing_data.get(key, 0) + value
            else:
                existing_data[key] = value

        with open(SESSION_HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, indent=4)

        logger.info("📁 Session history saved.")

    def select_input_mode(self) -> None:
        """Select input mode"""
        while True:
            mode_choice = input("Enter 1 for text input or 2 for voice input (or 'exit' to quit): ").strip()
            if mode_choice.lower() in ["exit", "quit"]:
                self.save_history()
                logger.info("Shutting down Sanruum AI. Goodbye! 👋")
                exit()
            elif mode_choice in ["1", "2"]:
                self.input_mode = "text" if mode_choice == "1" else "voice"
                break
            else:
                print("Invalid choice. Please enter 1 or 2.")

    def run(self) -> None:
        logger.info("Sanruum AI is starting...")

        if self.input_mode is None:
            self.select_input_mode()

        while True:
            try:
                if self.input_mode == "voice":
                    print("[DEBUG] - Listening...")
                    user_input = listen()
                    if not user_input:
                        print("Sorry, I did not catch that. Please try again.")
                        continue
                    print(f"You (via voice): {user_input}")
                else:
                    user_input = input("🧠 You: ").strip()

                if user_input.lower() in ["exit", "quit"]:
                    self.save_history()
                    logger.info("Shutting down Sanruum AI. Goodbye! 👋")
                    break

                if user_input.lower() == "stats":
                    self.print_stats()
                    continue

                if user_input.lower() == "history":
                    print(json.dumps(self.session_stats["query_log"], indent=2))
                    continue

                start_time = time.time()
                response = self.ai.get_response(user_input)
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


if __name__ == "__main__":
    ai_system = SanruumAI()
    ai_system.run()

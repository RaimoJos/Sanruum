from sanruum.ai_core.response import AIResponse
from sanruum.utils.logger import logger
from sanruum.utils.voice import listen, speak


def main() -> None:
    logger.info("Sanruum AI is starting...🚀")
    ai = AIResponse()

    while True:
        try:
            # Ask user to choose input mode
            mode = input("Enter 1 for text input or 2 for voice input (or 'exit' to quit): ").strip().lower()
            if mode in ["exit", "quit"]:
                logger.info("Shutting down Sanruum AI. Goodbye!")
                break

            if mode == "2":
                # Get voice input
                user_input = listen()
                if not user_input:
                    print("Sorry, I did not catch that. Please try again.")
                    continue
                print(f"You (via voice): {user_input}")
            else:
                user_input = input("🧠 You: ")

            if user_input.lower() in ["exit", "quit"]:
                logger.info("Shutting down Sanruum AI. Goodbye!")
                break

            response = ai.get_response(user_input)
            logger.info(f"🤖 Sanruum AI: {response}")

            # Speak the response (voice output)
            speak(response)
        except KeyboardInterrupt:
            logger.info("\nGoodbye!")
            break


if __name__ == "__main__":
    main()

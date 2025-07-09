from echopost import main
from echopost import load_settings

if __name__ == "__main__":
    settings = load_settings()
    main(settings)
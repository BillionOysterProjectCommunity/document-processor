from theia.drive.client import Client
from theia.settings.config import Config

def main():
    client = Client(Config())

    client.show_initial_files()

if __name__ == "__main__":
  main()
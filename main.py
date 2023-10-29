from document import DocumentProcessor
from config import Config



def main():

    config = Config()

    processor = DocumentProcessor(config)
    df = processor.process_document('training_data/training_10.jpg')
    print(df)

if __name__ == '__main__':
    main()
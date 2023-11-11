from document import DocumentProcessor
from config import Config

def main():

    config = Config()

    document_processor = DocumentProcessor(config)
    df = document_processor.process_document('training_data/training_7.jpg')
    print(df)

if __name__ == '__main__':
    main()


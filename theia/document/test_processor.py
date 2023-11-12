from theia.settings.config import Config
from theia.document.processor import DocumentProcessor
from theia.models.metadata import MetaData

def main():

    conf = Config()

    document_processor = DocumentProcessor(conf)
    df = document_processor.process_document('training_data/training_7.jpg')
    print(df)

    print(df.values)
    for value in df.values:
        print(value[0], value[1])

if __name__ == '__main__':
    main()
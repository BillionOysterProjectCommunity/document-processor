from theia.settings.config import Config
from theia.document.processor import DocumentProcessor
from theia.models.metadata import MetaData

def main():

    conf = Config()

    document_processor = DocumentProcessor(conf)
    df = document_processor.process_document('training_data/training_7.jpg')
    print(df)

if __name__ == '__main__':
    main()
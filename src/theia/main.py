import config.configuration as config
import document.processor as processor

def main():

    conf = config.Config()

    document_processor = processor.DocumentProcessor(conf)
    df = document_processor.process_document('training_data/training_7.jpg')
    print(df)

if __name__ == '__main__':
    main()

